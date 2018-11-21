from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

def switch_language_code(CODE):
	"""
		Switches language codes from ISO 639-1 to ISO 639-2.

		>>> switch_language_code("no")
		"nob"

	"""
	try:
		return oahpa_module.settings.OLD_NEW_ISO_CODES[CODE]
	except:
		# logger.warning("*** Unidentified language code %s." % CODE)
		# print >> sys.stdout, "*** Unidentified language code %s." % CODE
		return oahpa_module.settings.LANGUAGE_CODE
