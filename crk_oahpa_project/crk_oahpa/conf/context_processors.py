from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

try:
	default = oahpa_module.settings.DEFAULT_DIALECT
except:
	default = 'GG'

def dialect(request):
    if not request.session.get('dialect'):
    	request.session['dialect'] = default
    return {'dialect': request.session.get('dialect')}

def site_root(request):
	return {'URL_PREFIX': oahpa_module.settings.URL_PREFIX}

def grammarlinks(request):
	Grammarlinks = oahpa_module.drill.models.Grammarlinks
	from tools import switch_language_code

	default_lang = 'eng' # was: nob

	try:
		lang = switch_language_code(request.session.get('django_language'))
	except:
		lang = default_lang

	if lang == 'fin':
		lang = 'sme'  # If interface language is Finnish then the grammar explanations will be in North Sami.
	links = Grammarlinks.objects.filter(language=lang).order_by('name')

	if links.count() == 0:
		lang = default_lang
		links = Grammarlinks.objects.filter(language=lang).order_by('name')

	if links.count () > 0:
		return {'grammarlinks': links, 'cache_language': lang}
	else:
		return {'grammarlinks': False, 'cache_language': 'x'}
