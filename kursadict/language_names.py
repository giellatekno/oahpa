# -*- encoding: utf-8 -*-
# This is a temporary solution until I figure out the right way of 
# getting Babel to compile strings out of app.config.yaml

# Here are all the names of the languages used in dictionaries, for
# internationalization.
from flaskext.babel import lazy_gettext as _
NAMES = dict([
    ('sme', _(u"North Sámi")),
    ('SoMe', _(u"North Sámi (#SoMe)")),
    ('fin', _(u"Finnish")),
    ('nob', _(u"Norwegian")),
    ('sma', _(u"South Sámi")),
    #
    ('kpv', _(u"Komi")),
    ('liv', _(u"Livonian")),
    ('olo', _(u"Olonetsian")),

    ('myv', _(u"Erzya Mordvin")),

])
