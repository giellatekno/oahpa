# -*- coding: utf-8 -*-

import lxml.html
from lxml import etree
import StringIO
import re

case_labels = {u'именительный': 'nom',
               u'родительный': 'gen',
               u'дательный': 'dat',
               u'винительный': 'acc',
               u'творительный': 'ins',
               u'предложный': 'loc',
               u'разделительный падеж': 'gen2'}


try:
    with open('kompot.txt', 'r') as f:
        html = f.read()
except IOError:
    import mechanize
    req = mechanize.Request('http://ru.wiktionary.org/wiki/компот')
    req.add_header('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.57 Safari/537.1')
    r = mechanize.urlopen(req)
    with open('kompot.txt', 'w') as f:
        f.write(r.read())


root = lxml.html.fromstring(html)

data = dict()

def strip_empty(item):
    raw = item.text_content()
    r = re.compile('[\w\u0301]', re.U)
    if r.search(raw):
        return raw
    else:
        return None


for tr in root.cssselect("table[rules='all'] tr"):
    tds = tr.cssselect("td")
    if len(tds) == 3:
        row_label = tds[0].cssselect('a')[0].get('title')
        row_case = case_labels[row_label]
        if row_case == 'nom':
            data.update({'lemma': tds[1].text_content().replace(u'\u0301', '')}) # remove the stress mark
        sg = strip_empty(tds[1])
        pl = strip_empty(tds[2])
        if sg or pl:
            data[row_case] = dict()
        if sg:
            data[row_case]['sg'] = sg
        if pl:
            data[row_case]['pl'] = pl



        # data.update({row_case: { 'sg': tds[1].text_content(),
        #                          'pl': tds[2].text_content()}})


s = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet title="Dictionary view" media="screen,tv,projection" href="../../../words/dicts/scripts/gt_dictionary.css" type="text/css"?>
<?xml-stylesheet alternate="yes" title="Hierarchical view" media="screen,tv,projection" href="../../../words/dicts/scripts/gt_dictionary_alt.css" type="text/css"?>
<!DOCTYPE r PUBLIC "-//DivvunGiellatekno//DTD Dictionaries//Multilingual"
"../../../words/dicts/scripts/gt_dictionary.dtd">
<r xml:lang='ru'></r>"""

tree = etree.parse(StringIO.StringIO(s))
root = tree.getroot()
e = etree.SubElement(root, 'e')
lg = etree.SubElement(e, 'lg')
l = etree.SubElement(lg, 'l')
attributes = l.attrib
l.attrib.update({'pos': 'n',
                 'type': 'mi'})
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

def print_tree():
    return etree.tostring(tree, xml_declaration=True,
                         encoding='utf-8',pretty_print=True)

with open('kompot.xml', 'w') as f:
    f.write(print_tree())
