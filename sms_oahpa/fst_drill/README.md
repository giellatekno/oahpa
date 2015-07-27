# fst_drill: using FSTs for correction

Thinking that the goal here should be a drop-in module that can just replace
`sms_drill` on the urls level, with the least amount of changes to the
`sms_drill` codebase. Will be best if all admins have to do is tweak the urls.

## Summary of contents

* `lookup_client.py` - functions for communicating with the new lookupserv, and
  returning database objects

* `forms.py` - modified copy of sms_drill `forms.py`, where I'm figuring out
  how to insert FST functionality
