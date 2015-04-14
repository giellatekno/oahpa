# -*- coding: utf-8 -*-
"""

 * XML Structure
 * Install script structure
 * Future?

FEEDBACK AND XML-SOURCE
-------- --- ----------

Feedback message files have the following structure:

    <?xml version="1.0" encoding="utf-8"?>
    <messages xml:lang="fin"> 
        <message order="A" id="case1">WORDFORM has ... </message>  
        <message order="A" id="case2">WORDFORM has ... </message>  
        <message order="A" id="case3">WORDFORM has ... </message>  
        <message order="A" id="case4">WORDFORM has ... </message>  
        <message order="B" id="number1"> and is in singular.</message>  
        <message order="B" id="number2"> and is in plural.</message>  
    </messages>

In this case the id attribute corresponds to the message id, and the
order attribute corresponds to the order that the message will appear
in in the user interface. Orders are specified with the letters A-Z,
and if an order is not specified, it is assumed that this message will
come first, before A.

Nouns: attributes required: pos, soggi, stem, case/case2, number

    <l> nodes in messages.xml and n_smanob must match for
        pos, soggi, stem
    
    Remaining inflectional items, case and number, come from the tag.
                
    feedback_nouns.xml: 
    
    <feedback pos="N">
      <stems>
        <l stem="2syll">
          <msg pos="n">bisyllabic_stem</msg>
        </l>
        <l stem="3syll">
          <msg pos="n">trisyllabic_stem</msg>
        </l>

        <l stem="3syll" soggi="a">
          <msg case="Ill">soggi_a</msg>
          <msg case="Ine">soggi_a</msg>
          <msg case="Ela">soggi_a</msg>
          <msg case="Com" number="Sg">soggi_a</msg>
          <msg case="Ess">soggi_a</msg>
          <note>daktarasse, vuanavasse, e/o > a</note>
        </l>
     </stems>
    </feedback>
    
    
    n_smanob.xml:
    
    <e>
      <lg>
         <l margo="e" pos="n" soggi="e" stem="3syll">aagkele</l>
      </lg>
      { ... SNIP ... }
    </e>
    
Verbs: Mostly the same. <l/>s match for class, stem, pos
inflectional information from Tag object pertaining to mood, tense, personnumber.

FEEDBACK DATA STRUCTURE

Remember that this code runs once per word, and not on a huge set of words,
so it should ideally be returning only one Feedback object.

Feedback objects are then linked to Feedbackmsg objects, which contain
message IDs, such as soggi_o, class_1, which then link to Feedbacktext objects
which contain the corresponding messages in other languages.

Feedback objects should be linked to multiple Feedbackmsg items (typically, 3)
which individually contain class, syllable and umlaut information.

Feedback.messages.all()

INSTALL PROCESS
------- -------

The install process is invoked with a lexicon file and a feedback file: 

    python feedback_install.py -f word_file.xml --feedbackfile feedback_file.xml

The outcome of the install process is currently such that there is a Feedback
object in the database for each possible permutation of morphosyntactic
features, which correspond to both Word object attributes (morphophonology
mostly, rime, stem type, inflectional class, etc.) and Tag object attributes
(morphosyntactic mostly, person tense, number, etc.)

This results in many objects being generated, and as such the process may take
a long time depending on the kind of data being installed. There are several
optimizations in place, however: inserts are run in batch, not by the typical
Model.objects.create() method, and before this, all objects and database
relationships that need to be represented in these batch inserts are fetched,
with every query cached in python objects. At best, the script will run in 2
minutes, at worst, 30 minutes.

EDITING
-------

In order to add new morphosyntactic classes, there are several places that may
need to be checked. Usually it's a good idea to pick a feature that is similar
to the one being implemented, and search through the file. 

Some comments are marked with #NEW_ATTRIBUTES, so search through the file for
these for a hint at where to start.


FUTURE
------

Enterprising individuals who are willing to optimize more may consider altering
the model structure, such that Feedbackmsg objects are associated directly with
Form objects, saving the need to create tons of Feedback objects with all the
various permutations of morphosyntactic features.


"""

from settings import *
from univ_drill.models import Feedbackmsg,Feedbacktext,Dialect,Comment,Tag
from xml.dom import minidom as _dom
from django.db.models import Q
import sys
import re
import string
import codecs
import operator

from univ_drill.models import Form

from django.db import transaction
from itertools import product

from django.utils.encoding import force_unicode

def fix_encoding(s):
    try:
        s = s.decode('utf-8')
    except:
        pass
    
    return force_unicode(s)

try:
    from collections import OrderedDict
except ImportError:
    from conf.ordereddict import OrderedDict

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def get_attrs(item, attr_names):
    """ For an object, get attributes from a list of attributes.
    """
    vals = []
    for attr in attr_names:
        val = item.__getattribute__(attr)
        if val:
            vals.append(fix_encoding(val))
        else:
            vals.append('')
    return vals

def render_kwargs(D):
    lines = []
    for k, vs in D.iteritems():
        line = ' %s = %s ' % (k, ', '.join(vs))
        lines.append(line)
    
    return '\n'.join(lines).encode('utf-8')

def get_attrs_with_defaults(element, attr_list, defaults):
    """ Collect attributes from an XML element node, if there is no
    value, use a default value supplied from a defaults dictionary,
    return an OrderedDict of the attr_list and values. """
    # TODO: Pos, Comp, Superl, currently only returns Comp, Superl
    vals = []
    for attr in attr_list:
        val = element.getAttribute(attr)

        if not val:
            val = defaults.get(attr)

        if isinstance(val, list):
            val = [fix_encoding(s) for s in val]
        elif isinstance(val, set):
            val = [fix_encoding(s) for s in list(val)]
        else:
            val = [fix_encoding(val)]
        vals.append(val)
            
    x = OrderedDict(zip(attr_list, vals))
    grade = x.get('grade', False)
    if grade:
        if x['grade'] == ['Pos']:
            x['grade'] == ['']

    subclass = x.get('subclass', False)
    if subclass:
        if x['subclass'] == ['Active']:
            x['subclass'] == ['']
    
    return x


class Entry(object):

    def __init__(self, word, tag):

        self.word_kwargs = word
        self.tag_kwargs = tag
    
    @property
    def permutations(self):
        from itertools import product

        args = []
        self.kwarg_ordering = []
        for attr, arg in self.word_kwargs.iteritems():
            self.kwarg_ordering.append(attr)
            if isinstance(arg, list) or isinstance(arg, set):
                args.append(list(arg))
            else:
                args.append([arg])

        for attr, arg in self.tag_kwargs.iteritems():
            self.kwarg_ordering.append(attr)
            if isinstance(arg, list) or isinstance(arg, set):
                args.append(list(arg))
            else:
                args.append([arg])
        
        
        return product(*args)


class Feedback_install(object):

    # All dialects (except for NG and main)
    dialects = ['KJ', 'GG']

    # Each part of speech followed by relevant word/lemma attributes
    word_attribute_names = OrderedDict([
        ("N", ['stem', 'gradation', 'diphthong', 'rime', 'soggi',]),
        ("A", ['stem', 'gradation', 'diphthong', 'rime', 'soggi', 
                                        'attrsuffix', 'compsuffix',]),
        ("Num", ['stem', 'gradation', 'diphthong', 'rime', 'soggi',]),
        ("V", ['stem', 'gradation', 'diphthong', 'rime', 'soggi',]),
    ])

    # Each part of speech followed by relevant tag/wordform attributes
    tag_attribute_names = OrderedDict([
        ("N", ('case', 'number', 'possessive')),
        ("A", ('case', 'number', 'grade', 'attributive', )),
        ("Num", ('case', 'number',)),
        ("V", ('subclass', 'infinite', 'mood', 'tense', 'personnumber', )),
    ])

    # NOTE: processing of dialects and lemma exclusions is not something that
    # is available here, see below for ideas for adding similar things


    def __init__(self):
        self.tagset = {}
        self.paradigms = {}
        self.obj_count = 0
        self.duplicate_count = 0
        # self.dialects = ["KJ","GG"]
        self.created_objects_cache = {}

        self._file_pos = False
        self._wordtree = False
        self._word_elements = False
        self._feedbacktree = False
        self._feedback_elements = False
        self._feedback_msg_elements = False
        self._form_objects = False
        self._global_form_filter = False

        self._lexicon_dialects = False # TODO: this
        self._feedback_global_dialect = False # TODO: this

    def read_messages(self,infile):

        xmlfile = file(infile)
        tree = _dom.parse(infile)
        lex = tree.getElementsByTagName("messages")[0]
        lang = lex.getAttribute("xml:lang")     

        for el in tree.getElementsByTagName("message"):
            mid=el.getAttribute("id")
            order = ""
            order = el.getAttribute("order")
            # _user_lvl = el.getAttribute("user_level")
            # if _user_lvl is not None:
            #     user_level = int(_user_lvl)
            # else:
            #     user_level = 1
            # message = ""
            # When XML contains <![CDATA[]]> there is no need to treat the data
            # differently, as <a /> nodes will be treated as text
            message = el.firstChild.data  
            # links = []
            # for node in el.childNodes:
                # if node.nodeType == node.TEXT_NODE:
                    # message = message + node.data
                # else:
                    # link = node.toxml(encoding="utf-8") # in case the feedback contains a link
                    # message = message + link  
            print >> sys.stdout, message.encode('utf-8')
            fm, created = Feedbackmsg.objects.get_or_create(msgid=mid)
            fm.save()

            fmtext, created=Feedbacktext.objects.get_or_create(language=lang,feedbackmsg=fm,order=order,)
            fmtext.message=message
            fmtext.save()


    @property
    def feedbacktree(self):
        if not self._feedbacktree:
            self._feedbacktree = _dom.parse(self.feedbackfilename)
        return self._feedbacktree

    @property
    def feedback_elements(self):
        if not self._feedback_elements:
            stems = self.feedbacktree.getElementsByTagName("stems")[0]
            self._feedback_elements = stems.getElementsByTagName("l")
        return self._feedback_elements

    @property
    def feedback_msg_elements(self):
        if not self._feedback_msg_elements:
            stems = self.feedbacktree.getElementsByTagName("stems")[0]
            self._feedback_msg_elements = stems.getElementsByTagName("msg")
        return self._feedback_msg_elements
    
    @property
    def wordtree(self):
        if not self._wordtree:
            self._wordtree = _dom.parse(self.wordfilename)
        return self._wordtree

    @property
    def lexicon_word_elements(self):
        if not self._word_elements:
            self._word_elements = self.wordtree.getElementsByTagName("l")
        return self._word_elements
    
    @property
    def file_pos(self):
        if not self._file_pos:
            root = self.feedbacktree.getElementsByTagName("feedback")[0]
            self._file_pos = root.getAttribute("pos").capitalize()
        return self._file_pos
    
    @property
    def global_form_filter(self):
        if not self._global_form_filter:
            root = self.feedbacktree.getElementsByTagName("feedback")[0]
            if root.hasAttribute("tag__possessive"):  # filter for nouns without possessive suffix
                global_filter = root.getAttribute("tag__possessive").strip()
            else:
                global_filter = root.getAttribute("tag__string__contains").strip() # filter for nouns with possessive suffix and derivational verb forms
            if global_filter:
                self._global_form_filter = global_filter
            else:
                self._global_form_filter = False
        return self._global_form_filter
    
    @property
    def feedback_global_dialect(self):
        if not self._feedback_global_dialect:
            root = self.feedbacktree.getElementsByTagName("feedback")[0]
            self._feedback_global_dialect = root.getAttribute("dialect")
        return self._feedback_global_dialect

    @property
    def form_objects(self):
        if not self._form_objects:
            self._form_objects = Form.objects.filter(tag__pos=self.file_pos)
        return self._form_objects
    
    @property
    def word_attr_names(self):
        return self.word_attribute_names.get(self.file_pos)

    @property
    def tag_attr_names(self):
        return self.tag_attribute_names.get(self.file_pos)
    

    def find_intersection(self):
        """ Find the intersection of lexicon and feedback attribute values,
        return intersection, but also print it """

        def get_word_argument_and_lemma(el, attr_names_list=self.word_attr_names):
            " For a lexicon word element, get all of the morphological attributes " 
            vals = [el.getAttribute(attr) for attr in attr_names_list]
            # attributes and lemma
            return (OrderedDict(zip(attr_names_list, vals)), el.firstChild.data)

        def get_word_argument(el):
            return get_word_argument_and_lemma(el)[0]

        def get_msg_argument(el):
            " For a lexicon word element, get all of the morphological attributes " 
            vals = [el.getAttribute(attr) for attr in self.tag_attr_names]
            # attributes and lemma
            return OrderedDict(zip(self.tag_attr_names, vals))
        
        def get_tag_argument(attr_):
            " For a Tag object, get all of the morphological attributes "
            vals = list(set(Tag.objects.filter(pos=self.file_pos).values_list(attr_, flat=True)))
            if vals[0] != '':
                vals = sorted([''] + vals) # empty value necessary
            else:
                vals = sorted(vals)
            # attributes and lemma
            return (attr_, vals)

        # Fetch all word attributes for all entries in the lexicon
        word_attributes = map(get_word_argument_and_lemma, self.lexicon_word_elements)
        
        # Collate all the possible values in a dictionary
        # {'rime': ['a', 'e', 'i', 'o', 'u', etc ... ], 
        #  'soggi': ['a', 'b', 'c', etc ..]}
        #
        self.word_possible_values = OrderedDict([
            (attr_name, list(set([''] + [word_attr.get(attr_name, None) for word_attr, lemma in word_attributes])))
            for attr_name in self.word_attr_names
        ])

        # Do the same for Tag objects.
        # 
        self.tag_possible_values = OrderedDict(map(get_tag_argument, self.tag_attr_names))

        # Collect Feedback <l /> attributes
        feedback_attributes = map(get_word_argument, self.feedback_elements)
        self.feedback_possible_values = OrderedDict([
            (attr_name, list(set([''] + [word_attr.get(attr_name, None) for word_attr in feedback_attributes])))
            for attr_name in self.word_attr_names
        ])

        # Collect Feedback <msg /> attributes
        feedback_msg_attributes = map(get_msg_argument, self.feedback_msg_elements)
        self.feedback_msg_possible_values = OrderedDict([
            (attr_name, list(set([''] + [tag_attr.get(attr_name, None) for tag_attr in feedback_msg_attributes])))
            for attr_name in self.tag_attr_names
        ])

        # TODO: msg attributes and Tag comparison

        # Get the intersection of feedback word attributes and lexicon word
        # attributes
        # 
        def diff(attribute):
            return set(self.feedback_possible_values.get(attribute)) | \
                    set(self.word_possible_values.get(attribute))

        self.attributes_intersection = OrderedDict([
            (attr_name, diff(attr_name))
            for attr_name in self.word_attr_names
        ])

        def tag_diff(attribute):
            d = set(self.feedback_msg_possible_values.get(attribute)) | \
                    set(self.tag_possible_values.get(attribute))
            return d
            
        self.tag_attributes_intersection = OrderedDict([
            (attr_name, tag_diff(attr_name))
            for attr_name in self.tag_attr_names
        ])

        self.default_attributes = OrderedDict(
            list(self.attributes_intersection.iteritems()) + 
            list(self.tag_attributes_intersection.iteritems())
        )
        
        return self.attributes_intersection

    def print_intersection(self):

        def fmt_dict(D):
            lines = []
            for k, v in D.iteritems():
                vs = ', '.join(sorted(v))
                line = "        %s: %s" % (k, vs)
                lines.append(line)
            try:
                return fix_encoding('\n'.join(lines))
            except:
                return '\n'.join(lines)


        print >> sys.stdout, "\n  LEXICON"
        print >> sys.stdout, "    Attributes in word file:"
        print >> sys.stdout, fmt_dict(self.word_possible_values).encode('utf-8')

        print >> sys.stdout, "    Tag attributes in lexicon for %s:" % self.file_pos 
        print >> sys.stdout, fmt_dict(self.tag_possible_values)

        print >> sys.stdout, "\n  FEEDBACK"
        print >> sys.stdout, "    Attributes in feedback file:"
        print >> sys.stdout, fmt_dict(self.feedback_possible_values)

        print >> sys.stdout, "    <msg />  attributes in feedback file:"
        print >> sys.stdout, fmt_dict(self.feedback_msg_possible_values)


        print >> sys.stdout, "\n  COMPARISON"
        print >> sys.stdout, "    Symmetric difference between lexicon and feedback:"

        for attribute_name, lexicon_attribute_values in self.word_possible_values.iteritems():
            fb_attr_vals = self.feedback_possible_values.get(attribute_name, False)
            missing = []
            if fb_attr_vals:
                missing.extend(list(set(fb_attr_vals) ^ set(lexicon_attribute_values)))
            _str = "        %s: %s" % (attribute_name, ', '.join(missing))
            try:
                print >> sys.stdout, _str.encode('utf-8')
            except:
                print >> sys.stdout, _str


        print >> sys.stdout, '\n'

        print >> sys.stdout, "    Symmetric difference between Tag and <msg />:"

        for attribute_name, lexicon_attribute_values in self.tag_possible_values.iteritems():
            fb_attr_vals = self.feedback_msg_possible_values.get(attribute_name, False)
            missing = []
            if fb_attr_vals:
                missing.extend(list(set(fb_attr_vals) ^ set(lexicon_attribute_values)))
            print >> sys.stdout, "        %s: %s" % (attribute_name, ', '.join(missing))

        print >> sys.stdout, '\n'


    def read_feedback(self, feedbackfile, wordfile, append):
        """
            TODO: update this.
        """

        if Feedbackmsg.objects.count() == 0:
            print >> sys.stderr, "No message strings have been installed (messages.sme.xml, etc)."
            sys.exit()
        self.feedbackfilename = feedbackfile
        self.wordfilename = wordfile

        print >> sys.stdout, self.feedbackfilename
        print >> sys.stdout, self.wordfilename

        if not append:
            print >> sys.stdout, " * Deleting existing feedbacks"
            Form.objects.bulk_remove_form_messages(self.form_objects)

        # Get intersection of elements and tags
        self.attributes_intersection = self.find_intersection()
        self.print_intersection()

        # collect all form attributes to lessen size of permutation objects
        def word_and_tag_keys(f):
            vals = tuple(get_attrs(f.word, self.word_attr_names) + \
                            get_attrs(f.tag, self.tag_attr_names))
            keys = list(self.word_attr_names) + list(self.tag_attr_names)
            return OrderedDict(zip(keys, vals))

        values = ['word__' + w_attr for w_attr in self.word_attr_names] + \
                    ['tag__' + t_attr for t_attr in self.tag_attr_names] + \
                    ['dialects__dialect', 'id', 'word__lemma', 'tag__string']

        print >> sys.stdout, "Fetching wordform attributes."
        
        forms = self.form_objects.only(*values) # Get only the things we need.
        if self.global_form_filter:
            forms = forms.filter(tag__string__contains=self.global_form_filter)
        total = forms.count()
        form_keys = {}

        # Since this isn't really in the database, it won't be included in iteration later
        if self.file_pos == 'A':
            self.default_attributes['grade'].add('Pos')
            # self.default_attributes['grade'].remove("")

        if self.file_pos == 'V':
            self.default_attributes['subclass'].add('Active')

        # TODO: test this.
        # if self.file_pos == 'N':
            # self.default_attributes['rime'].add('0')

        # .iterator() necessary because QuerySet is very large.
        for f in forms.iterator():
            total -= 1
            w_key_vals = word_and_tag_keys(f)

            # Exception here because there is no 'Pos' in the db, but 'Pos' in
            # feedback. TODO: make a generaelized version of this for a class
            # setting
            if self.file_pos == 'A':
                if not w_key_vals['grade'] in ['Comp', 'Superl']:
                    w_key_vals['grade'] = 'Pos'

            if self.file_pos == 'V':
                if not w_key_vals['subclass'] in ['Der/PassL', 'Der/PassS', 'Der/AV']:
                    w_key_vals['subclass'] = 'Active'
                    
            w_keys = tuple(w_key_vals.values())

            dialects = [''] + [d.dialect for d in f.dialects.all() 
                        if d.dialect in self.dialects]

            # TODO: global dialects?

            w_vals = [f.id, fix_encoding(f.word.lemma), f.tag.string, dialects]

            if w_keys in form_keys:
                form_keys[w_keys].append(w_vals)
            else:
                form_keys[w_keys] = [w_vals]

            if total%1000 == 0:
                print "  Fetching wordform attributes: %d left" % total 

        form_keys_key_set = set(form_keys.keys())
        # print list(form_keys_key_set)[0:20]
        # raw_input()

        # Here we check through all of the feedback elements and figure out
        # whether:
        #
        #   (a) the permutation of attributes is attested in the lexicon, if
        #       not, skip
        #   (b) dialects (if available) in each <msg /> element match up with
        #       the words in the lexicon that match up with the other
        #       attributes
        #   (c) if a lemma is specified in <l />, then a similar pattern is
        #       used to dialect filtering to remove words not matching the
        #       lemma.
        # 
        # Feedback attribute permutations are defined as such: 
        # 
        # Each feedback <l /> has some attributes which correspond to
        # attributes of Word objects, and <msg /> elements if they exist have
        # attributes which correspond to attributes of Form objects. For either
        # of these sets of possible attributes, some are not defined, and these
        # can be anything: e.g., if tense is defined as Prs, then tense
        # permutations will only include Prs, if it is undefined, it could
        # include Prs Prt, etc. Those attributes which are not defined instead
        # take their values from the set of possible values in the lexicon.
        #
        # In order to match Feedback elements to Form objects, the product of
        # all of these potential feedback values must be generated, which is
        # more or less depending on which attributes have and have not been
        # defined. Each permutation is then associated with a message id
        # (n-suffix, etc.)
        # 
        print >> sys.stdout, "Compiling word/tag attribute permutations and msg names"
        attrs_and_messages = {}
        # collect form and msg ids here
        form_infos = []
        for el in self.feedback_elements:
            kwargs = get_attrs_with_defaults(el, 
                                            self.word_attr_names, 
                                            self.default_attributes)
            
            msgs = el.getElementsByTagName("msg")

            lemma = el.getAttribute("lemma")
            if not lemma.strip():
                form_lemma = False
            else:
                form_lemma = lemma.strip()

            for msg in msgs:
                m = msg.firstChild.data
                tagkwargs = get_attrs_with_defaults(msg, 
                                                    self.tag_attr_names, 
                                                    self.default_attributes)

                # Px_all denotes all possible Px tags. This is to avoid writing the same thing 9 times in the feedback file.
                # Px_Sg - possessive singular 1-3
                # Px_DuPl - possessive dual 1-3 and plural 1-3
                if 'possessive' in tagkwargs:
                    if tagkwargs['possessive'][0] == 'Px_all':
                        tagkwargs['possessive'] = [u'PxSg1', u'PxSg2', u'PxSg3', u'PxDu1', u'PxDu2', u'PxDu3', u'PxPl1', u'PxPl2', u'PxPl3']
                    if tagkwargs['possessive'][0] == 'Px_Sg':
                        tagkwargs['possessive'] = [u'PxSg1', u'PxSg2', u'PxSg3']
                    if tagkwargs['possessive'][0] == 'Px_DuPl':
                        tagkwargs['possessive'] = [u'PxDu1', u'PxDu2', u'PxDu3', u'PxPl1', u'PxPl2', u'PxPl3']
            
                # TODO: global dialects
                dial = msg.getAttribute("dialect")

                if dial and not self.feedback_global_dialect:
                    if dial.startswith('NOT-'):
                        # Get all other dialects 
                        feedback_dialects = [
                            d 
                            for d in self.dialects 
                            if d != dial.replace('NOT-', '')
                        ]
                    else:
                        feedback_dialects = [dial]
                else:
                    feedback_dialects = False

                if self.feedback_global_dialect:
                    feedback_dialects = [self.feedback_global_dialect]

                print >> sys.stderr, "\nSearching for Wordforms matching ... " 
                print >> sys.stderr, render_kwargs(kwargs)
                print >> sys.stderr, render_kwargs(tagkwargs)

                prod_count = reduce(
                    operator.mul, 
                    [len(a) for a in kwargs.values() + tagkwargs.values()]
                )
                
                def intersect_param_set(param_set):
                    print >> sys.stderr, "Intersecting..."

                    intersection = form_keys_key_set & param_set

                    for item in intersection:
                        if lemma:
                            form_keys[item] = [
                                [a, word_lemma, c, d]
                                for a, word_lemma, c, d in form_keys[item][:]
                                if word_lemma == form_lemma
                            ]

                        if dial:
                            # Filter out entries not matching the dialect, these
                            # will not be inserted later.
                            form_keys[item] = [
                                [a, b, c, d] 
                                for a, b, c, d in form_keys[item][:]
                                if len(set(d) & set(feedback_dialects)) > 0
                            ]

                        # Then for a set of attributes, append the message id
                        for f_id, f_lem, f_tag, f_dial in form_keys[item]:
                            # Collect IDs and msgs
                            form_infos.append((f_id, f_lem, f_tag, m))

                        if item in attrs_and_messages:
                            attrs_and_messages[item].append(m)
                        else:
                            attrs_and_messages[item] = [m]

                    print >> sys.stdout, "Identified %d\n" % len(intersection)
                    del param_set
                
                param_set_ = set()
                print >> sys.stderr, "Permutation count: %d" % prod_count
                perm_count = 0
                for perm in Entry(kwargs, tagkwargs).permutations:
                    # p, e, r, m, i, n, a = perm
                    # if [p, e, r] == [u'2syll', u'yes', u'no']:
                        # print perm
                    param_set_.add(tuple(perm))

                    perm_count += 1
                    if prod_count > 100000:
                        if perm_count%100000 == 0:
                            print "  %s processed." % perm_count

                    if len(param_set_) > 1000000:
                        intersect_param_set(param_set_)
                        param_set_ = set()

                intersect_param_set(param_set_)

                # Set intersections work much faster, rather than iterating and
                # doing a series of if statements.
                # TODO: intersect in chunks for much biggger sets, probs intersect in 1mil?



        # TODO: store words with no matches somewhere?

        # Prefetch all feedback ids and msgids: {'bisyllabic_stem': 4, etc ...}
        feedbackmsg_ids = dict([(fix_encoding(msg.msgid), msg.id) 
                                for msg in Feedbackmsg.objects.iterator()])

        total_forms = self.form_objects.count()


        # Now we iterate through the prefetched form attributes and form IDs,
        # etc., and collect the message ids (n-suffix, t-suffix, etc.) for each
        # set of form attributes. Some of this does not really need to be here,
        # but is left for debugging purposes, so it is easy to run through the
        # attribute sets that have made it through previous iterations.
        # 
        # Form ID and message IDs will later be expanded and used to insert
        # into the database in bulk.
        #

        print >> sys.stdout, "Collecting for insert."

        form_id_msg_id = []
        for f_id, f_lemma, f_tag, f_msg in form_infos:
            msg_id = feedbackmsg_ids.get(f_msg)
            form_id_msg_id.append((f_id, msg_id))


        # Expand (id, [msgid, msgid, msgid]) into 
        #        [(id, msgid), (id, msgid), (id, msgid)]
        # Produce a set to avoid duplicates for bulk insert.
        # 
        # form_id_msg_ids = list(set([
            # (id, msgid) 
            # for _, _, _, id, msgids in form_to_msgs
            # for msgid in msgids
        # ]))

        form_id_msg_ids = [(a, b) for a, b in list(set(form_id_msg_id)) if a and b]

        total_objs = len(form_id_msg_ids)

        # Chunk the data up into reasonable sizes for bulk insert, kind of
        # arbitrary, but main constraint is avoiding inserting too much SQL
        #
        chunk_size = 10000
        arg_chunks = chunks(form_id_msg_ids, chunk_size)

        # All of the Feedback objects are inserted chunk by chunk
        progress = 0
        print >> sys.stdout, " * Bulk inserting... "
        for chunk in arg_chunks:
            try:
                Form.objects.bulk_add_form_messages(chunk)
            except Exception, e:
                print >> sys.stderr, Exception, e
                print >> sys.stderr, repr(chunk[0:10]) + " ... " 
                print >> sys.stderr, "Chunk contains null values, are messages.xml files installed?"
                print >> sys.stderr, "Removing null values and inserting..."
                chunk = [(a, b) for a, b in chunk if a and b]
                Form.objects.bulk_add_form_messages(chunk)
            progress += chunk_size
            if progress%10000 == 0:
                print '%d/%d Form-Feedbackmsg relations' % (progress, total_objs)

        print >> sys.stdout, "Done!"

