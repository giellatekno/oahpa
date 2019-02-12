from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)
from ling import Paradigm
from words_install import Words
from extra_install import Extra
from feedback_install import Feedback_install
from questions_install import Questions

from optparse import make_option

import sys

def WordGeneration(conf, install_summary, options):
	
	for item in conf['WordGeneration']:
		linginfo = Paradigm()
		words = Words()
		
		kwargs = {'delete': None}
		kwargs['infile'] = fname = item['file']
		
		try:
			try:
				open(kwargs['infile'], 'r')
			except IOError:
				errmsg = " * File %s not found." % kwargs['infile']
				print >> sys.stderr, errmsg
				raise Exception(errmsg)

			if item.has_key('tagfile'):
				linginfo.handle_tags(item['tagfile'], False)

			if item.has_key('paradigmfile'):
				linginfo.read_paradigms(item['paradigmfile'], item['tagfile'], False)
				kwargs['paradigmfile'] = item['paradigmfile']
			kwargs['linginfo'] = linginfo
			if options.has_key('verbose'):
				kwargs['verbose'] = options['verbose']
			words.install_lexicon(**kwargs)

			print "%s done processing." % fname
			install_summary[fname] = ("Success", "")
		except Exception, e:
			install_summary[fname] = ("Fail", e)

	return install_summary

class Command(BaseCommand):
	args = '<config_file ...>'
	help = 'Installs data'
	option_list = BaseCommand.option_list + (
		make_option('--config',
			  dest='config', 
			  default=False,
			  help='Configuration file to use for installation'),
		make_option('--skip-generation',
			  dest='skip_generation',
			  action='store_true',
			  default=False,
			  help='Skip word generation'),
		make_option('--skip-semantics',
			  dest='skip_semantics',
			  action='store_true',
			  default=False,
			  help='Skip adding semantic tags',),
		make_option('--skip-feedback',
			  dest='skip_feedback',
			  action='store_true',
			  default=False,
			  help='Skip adding feedback',),
		make_option('--skip-questions',
			  dest='skip_questions',
			  action='store_true',
			  default=False,
			  help='Skip adding questions',),

		make_option('--verbose',
			  dest='verbose',
			  action='store_true',
			  default=True,
			  help="Verbose",),

		make_option('--fst-dir',
			  dest='fst_dir',
			  help='Specify directory containing FSTs',),
		make_option("-b", "--db", dest="add_db",
						  action="store_true", default=False,
						  help="Used for adding tag infoformation to database"),
		make_option("-c", "--comments", dest="commentfile",
						  help="XML-file for comments"),
		make_option("-d", "--delete", dest="delete",
						  action="store_true", default=False,
						  help="delete words that do not appear in the lexicon file of certain pos"),
		make_option("-e", "--feedbackfile", dest="feedbackfile",
						  help="XML-file for feedback"),
		make_option("-f", "--file", dest="infile",
						  help="lexicon file name"),
		make_option("-g", "--grammarfile", dest="grammarfile",
						  help="XML-file for grammar defaults for questions"),
		make_option("-s", "--sem", dest="semtypefile",
						  help="XML-file semantic subclasses"),
		make_option("-t", "--tagfile", dest="tagfile",
						  help="List of tags and tagsets"),
		make_option("-m", "--messagefile", dest="messagefile",
	                  help="XML-file for feedback messages"),
		make_option("-q", "--questionfile", dest="questionfile",
		              help="XML-file that contains questions"),
		make_option("-w", "--wid", dest="wordid",
						  help="delete word using id or lemma"),
		make_option("-p", "--pos", dest="pos",
						  help="pos of the deleted word"),
		make_option("-r", "--paradigmfile", dest="paradigmfile",
						  help="Generate paradigms"),
	)

	def installConfig(self, args, options, config_data):
		
		install_summary = {}

		# Install words and generate
		if not options.get('skip_generation'):
			install_summary = WordGeneration(config_data, install_summary, options)
		else:
			print >> sys.stderr, "*** Skipping word generation"
		
		# Install semantics
		if options.get('skip_semantics'):
			print >> sys.stderr, "*** Skipping processing of semantics"
		else:
			if config_data.has_key('Supersets'):
				fname = config_data['Supersets']
				extra = Extra()
				for f in fname:
					install_summary[f] = 'In progress...'
					try:
						extra.read_semtypes(f)
						install_summary[f] = ("Success", "")
					except Exception, e:
						install_summary[f] = ("Fail", str(e))

		
		# Install feedback

		if options.get('skip_feedback'):
			print >> sys.stderr, "*** Skipping feedback"
		else:
			if config_data.has_key('Feedback'):
				feedback = Feedback_install()
				
				# Read messagefiles
				for mfile in config_data['Feedback']['messagefiles']:
					try:
						feedback.read_messages(mfile)
						install_summary[mfile] = ("Success", '')
					except Exception, e:
						install_summary[mfile] = ("Fail", e)

				# Read feedbacks
				for items in config_data['Feedback']['feedbacks']:
					try:
						feedback.read_feedback(items['feedbackfile'],
												items['wordfile'])
						install_summary[items['feedbackfile'] + ', ' + items['wordfile']] = ("Success", '')
					except Exception, e:
						install_summary[items['feedbackfile'] + ', ' + items['wordfile']] = ("Fail", e)

		# Install questions
		if options.get('skip_questions'):
			print >> sys.stderr, "*** Skipping questions"
		else:
			for question_set in config_data['MorfaC_Install']['questionfiles']:
				qfile = question_set['questions']
				gfile = question_set['grammar']
				questions = Questions()
				try:
					questions.read_questions(qfile, gfile)
					install_summary[qfile] = ("Success", '')
				except Exception, e:
					install_summary[qfile] = ("Fail", e)
		
		print >> sys.stderr, " === Install summary === "
		for k, v in install_summary.items():
			print >> sys.stderr, "%s\t\t%s\t\t%s" % (v[0], k, v[1])

	def handle(self, *args, **options):
		# TODO: specify install yaml file 
		# TODO: actually use Config.FSTs, currently the install processed
		# TODO: error handling if process does not complete somehow
		# TODO: install ordering, need to be able to define ordering of
		# install steps, since there are some that depend on eachother
		# grabs these from settings.py 

		# TODO: option to specify filename without path, and
		# automatically grab that line from the config and install.

		import os, sys
		import yaml
		
		if options['config']:
			conf_fname = options['config']

			cur_path = os.getcwd()
			parent_path = '/' + '/'.join([a for a in cur_path.split('/') if a][0:-1]) + '/'
			sys.path.insert(0, parent_path)

			with open(conf_fname, 'r') as F:
				data = F.read()

			config_data = yaml.load(data)

			self.installConfig(args, options, config_data)
		

		# More options go here.
		linginfo = Paradigm()
		words = Words()
		# Options from install.py
		if options['tagfile']:
			linginfo.handle_tags(options['tagfile'], options['add_db'])
	
		if options['paradigmfile']:
			linginfo.read_paradigms(options['paradigmfile'], options['tagfile'], options['add_db'])
	
		if options['wordid']:
			words.delete_word(options['wordid'],options['pos'])
			sys.exit()
	
		if options['questionfile'] and options['grammarfile']:
		    questions.read_questions(options['questionfile'],options['grammarfile'])
		    sys.exit()
		
		if options['semtypefile']:
			extra.read_semtypes(options['semtypefile'])
			sys.exit()
		
		if options['messagefile']:
		    feedback.read_messages(options['messagefile'])
		    sys.exit()
	
		if options['feedbackfile'] and options['infile']:
		    feedback.read_feedback(options['feedbackfile'],options['infile'])
		    sys.exit()
		
		if options['infile']:
			words.install_lexicon(infile=options['infile'],linginfo=linginfo,delete=options['delete'],paradigmfile=options['paradigmfile'])
			sys.exit()


