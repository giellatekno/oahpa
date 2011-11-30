import univ_oahpa.settings

try:
	default = univ_oahpa.settings.DEFAULT_DIALECT
except:
	default = 'GG'

def dialect(request):
    if not request.session.get('dialect'):
    	request.session['dialect'] = default
    return {'dialect': request.session.get('dialect')}

def site_root(request):
	return {'URL_PREFIX': univ_oahpa.settings.URL_PREFIX}

def grammarlinks(request):
	from univ_drill.models import Grammarlinks
	from conf.tools import switch_language_code
	
	default_lang = 'nob'
	
	try:
		lang = switch_language_code(request.session.get('django_language'))
	except:
		lang = default_lang
	
	links = Grammarlinks.objects.filter(language=lang)
	
	if links.count() == 0:
		lang = default_lang
		links = Grammarlinks.objects.filter(language=lang)
	
	if links.count () > 0:
		return {'grammarlinks': links, 'cache_language': lang}
	else:
		return {'grammarlinks': False, 'cache_language': 'x'}

