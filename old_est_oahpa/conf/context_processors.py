import est_oahpa.settings

try:
	default = est_oahpa.settings.DEFAULT_DIALECT
except:
	default = 'GG'

def dialect(request):
    if not request.session.get('dialect'):
    	request.session['dialect'] = default
    return {'dialect': request.session.get('dialect')}

def site_root(request):
	return {'URL_PREFIX': est_oahpa.settings.URL_PREFIX}

def grammarlinks(request):
	from est_drill.models import Grammarlinks
	from conf.tools import switch_language_code
	
	default_lang = 'nob'
	
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

