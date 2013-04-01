#!/opt/local/bin/python
# -*- coding: utf-8 -*-

import lxml.html
from lxml import etree
import StringIO
import re

case_labels = {u'именительный': 'Nom',
               u'родительный': 'Gen',
               u'дательный': 'Dat',
               u'винительный': 'Acc',
               u'творительный': 'Ins',
               u'предложный': 'Loc',
               u'разделительный падеж': 'Gen2'}


def get_html_source(word, filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except IOError:
        import mechanize
        import time
        print unicode("Waiting to scrape %s" % word)
        time.sleep(3) # don't be evil, and anyway ideally we only have to do this every once in a while
        url = unicode('http://ru.wiktionary.org/wiki/%s' % word)
        req = mechanize.Request(url.encode('utf-8'))
        req.add_header('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.57 Safari/537.1')
        r = mechanize.urlopen(req)
        scraped = r.read()
        with open(filename, 'w') as f:
            f.write(scraped)
        return scraped

def strip_empty(item):
    raw = item.text_content()
    r = re.compile('[\w\u0301]', re.U)
    if r.search(raw):
        return raw.split(',')[0] # if multiple forms given as in Inst Sg, only give the first one
    else:
        return None

s = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet title="Dictionary view" media="screen,tv,projection" href="../../../words/dicts/scripts/gt_dictionary.css" type="text/css"?>
<?xml-stylesheet alternate="yes" title="Hierarchical view" media="screen,tv,projection" href="../../../words/dicts/scripts/gt_dictionary_alt.css" type="text/css"?>
<!DOCTYPE r PUBLIC "-//DivvunGiellatekno//DTD Dictionaries//Multilingual"
"../../../words/dicts/scripts/gt_dictionary.dtd">
<r xml:lang='ru'></r>"""

def parse_htmlfile_noun(srcfile):
    """Take an input file and return an XML node which you can
    append. For readability this should eventually be broken down into
    more bits."""
    srcroot = lxml.html.fromstring(srcfile)

    # create the dict with case forms
    data = dict()
    for tr in srcroot.cssselect("table[rules='all'] tr"):
        tds = tr.cssselect("td")
        if len(tds) == 3:
            row_label = tds[0].cssselect('a')[0].get('title')
            row_case = case_labels[row_label]
            if row_case == 'Nom':
                data['lemma'] = tds[1].text_content().replace(u'\u0301', '') # remove the stress mark
            sg = strip_empty(tds[1])
            pl = strip_empty(tds[2])
            if row_case not in data: # This assumes that Russian always comes first! Potential breakage
                kvlist = [('Sg', sg), ('Pl', pl)]
                update_list = [(key, value) for key, value in kvlist if value]
                data[row_case] = dict(update_list)

    # scrape the gender and animacy.
    paragraph_finder = re.compile(u'тип склонения', re.U)
    # this is a bit ugly
    for paragraph in [node.text_content() for node in srcroot.cssselect('p')]:
        if paragraph_finder.search(paragraph):
            grammar_text = paragraph
            break

    decl_re = re.compile(u'(\d)-е', re.U)
    decl_match = re.search(decl_re, grammar_text)
    declension = decl_match.group(1)

    inanimate_re = re.compile(u'неодуш', re.U)
    inanimate_match = re.search(inanimate_re, grammar_text)
    if inanimate_match:
        animate = 'inanim'
    else:
        animate = 'anim'

    gender_table = { u'мужской': 'masc',
                     u'женский': 'fem',
                     u'средний': 'neut' }
    gender_re = re.compile(u'(\w+)\ род', re.U)
    gender_match = re.search(gender_re, grammar_text)
    gender = gender_table[gender_match.group(1)]

    e = etree.Element('e')
    lg = etree.SubElement(e, 'lg')
    l = etree.SubElement(lg, 'l')
    l.attrib.update({'pos': 'n',
                     'gender': gender,
                     'animate': animate,
                     'declension': declension})
    l.text = data['lemma']
    analysis = etree.SubElement(lg, 'analysis')
    analysis.text = 'N_Sg_Nom'
    mp = etree.SubElement(lg, 'mini_paradigm')

    for case in [x for x in data.keys() if x != 'lemma']:
        for number in data[case].keys():
            if data[case][number]:
                mini_analysis = etree.SubElement(mp, 'analysis')
                analysis_string = 'N_%s_%s' % (number, case)
                mini_analysis.set('ms', analysis_string)
                wf = etree.SubElement(mini_analysis, 'wordform')
                wf.text = data[case][number]

    return e

tree = etree.parse(StringIO.StringIO(s))
root = tree.getroot()

entry_list = ([u'окно', 'windowsrc.xml'],
              [u'компот', 'kompotsrc.xml'],
              [u'мышь', 'mousesrc.xml'],
              [u'мальчик', 'boysrc.xml'],
              [u'девочка', 'girlsrc.xml'],)



for entry in entry_list:
    root.append(parse_htmlfile_noun(get_html_source(*entry)))

def print_tree():
    return etree.tostring(tree, xml_declaration=True,
                         encoding='utf-8',pretty_print=True)

with open('n_rus.xml', 'w') as f:
    f.write(print_tree())
