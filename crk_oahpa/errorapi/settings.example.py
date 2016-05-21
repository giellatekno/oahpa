
# Imagine this is in settings.py, thus all paths should be relative to
# that.

_join_path = lambda x: os.path.join(os.getcwd(), x)

ERROR_FST_SETTINGS = {
	'lookup_tool': '/usr/local/bin/lookup -flags mbTT',
	'fst_path': '/opt/smi/sme/bin/ped-errortag-sme.fst',
	'error_log_path': _join_path('error_fst_log.txt'),
	'error_message_files': {
		'nob': _join_path('../meta/morfaerrorfstmessages.xml'),
    }
}
