
class AppConf(object):
    """ An object for exposing the settings in app.config.yaml in a nice
    objecty way, and validating some of the contents.
    """
    @property
    def baseforms(self):
        if self._baseforms:
            return self._baseforms

        lang_baseforms = self.opts.get('Baseforms')

        self._baseforms = lang_baseforms
        return self._baseforms

    @property
    def paradigms(self):
        if self._paradigms:
            return self._paradigms

        lang_paradigms = self.opts.get('Paradigms')

        self._paradigms = lang_paradigms
        return self._paradigms
        
    @property
    def reversable_dictionaries(self):
        if self._reversable_dictionaries:
            return self._reversable_dictionaries

        def isReversable(d):
            if d.get('reversable', False):
                return d

        dicts = filter(isReversable, self.opts.get('Dictionaries'))
        language_pairs = {}
        for item in dicts:
            
            source = item.get('source')
            target = item.get('target')
            path = item.get('path')
            language_pairs[(source, target)] = path

        self._reversable_dictionaries = language_pairs
        return language_pairs

    @property
    def dictionaries(self):
        if self._dictionaries:
            return self._dictionaries

        dicts = self.opts.get('Dictionaries')
        language_pairs = {}
        for item in dicts:
            source = item.get('source')
            target = item.get('target')
            path = item.get('path')
            language_pairs[(source, target)] = path

        self._dictionaries = language_pairs
        return language_pairs

    @property
    def morphologies(self):
        if self._morphologies:
            return self._morphologies

        self._morphologies = {}

        from morphology import XFST, OBT, Morphology
        formats = {
            'xfst': XFST,
            'obt': OBT,
        }

        for iso, _kwargs_in in self.opts.get('Morphology').iteritems():
            conf_format = _kwargs_in.get('format', False)
            kwargs = {}

            if not conf_format:
                print "No format specified"
                sys.exit()

            m_format = formats.get(conf_format, False)
            if not m_format:
                print "Undefined format"
                sys.exit()

            if 'tool' in _kwargs_in:
                kwargs['lookup_tool'] = _kwargs_in['tool']
            else:
                print "Lookup tool missing"
                sys.exit()

            if 'file' in _kwargs_in:
                kwargs['fst_file'] = _kwargs_in['file']
            
            if 'inverse_file' in _kwargs_in:
                kwargs['ifst_file'] = _kwargs_in['inverse_file']

            try:
                self._morphologies[iso] = m_format(**kwargs) >> Morphology(iso)
            except:
                print "Error initializing morphology"
                print iso
                print kwargs
                print _in_kwargs

        return self._morphologies

    @property
    def lookup_command(self):
        """ Check that the lookup command is executable and user has
        permissions to execute. """
        import os
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        
        apps = self.opts.get('Utilities')
        cmd = apps.get('lookup_path')
        
        if not is_exe(cmd):
            sys.exit('Lookup utility (%s) does not exist, \
                      or you have no exec permissions' % cmd)
        cmd_opts = apps.get('lookup_opts', False)
        if cmd_opts:
            cmd += ' ' + cmd_opts
        return cmd

    def __init__(self):
        self._dictionaries            = False
        self._reversable_dictionaries = False
        self._paradigms               = False
        self._baseforms               = False
        self._morphologies            = False

        import yaml
        with open('app.config.yaml', 'r') as F:
            config = yaml.load(F)
        self.opts = config
        
settings = AppConf()

if __name__ == "__main__":
    settings = AppConf()
    print settings.morphologies
