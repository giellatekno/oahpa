This is the folder in svn that was named 'ped', and contains the
oahpa.no Forrest site, as well as all the oahpa.no programs for
each language. That app is a django on python 2 app.



Hosting oahpa.no on gtoahpa-02.uit.no (new server as of 2024):

oahpa.no is a static site served directly from the host nginx.
The built files are in /var/www/html


Building oahpa.no on oahpa-02:

The script /home/services/build-oahpa-no.sh
- pulls the git repo
- then builds it using forrest inside a container
- and finally copies the built page to /var/www/html

It runs every third hour-ish, using a systemd timer
- see /etc/systemd/system/build-oahpa-no.(service|timer)

(the timer runs that service, which runs the sh script)


(notes on gtoahpa-01):

This is the `crontab -l` on gtoahpa-01:

30 13 * * * source $HOME/.bashrc && cd $HOME/repos/giellalt/giella-core && git pull && cd $GTHOME && svn -q up && static-divvun.py --sitehome $GTHOME/ped --destination ~/public_html/ --verbosity warning en





==========================================================
OLD README BELOW
==========================================================






Overall goal: transfer and install all oahpa instances on the new oahpa server

TODO:
 - update django to the latest version: ongoing work for sms_oahpa locally
  ==> DONE (both locally and on the new server)
 - update the db feeding scripts: ongoing work
  ==> DONE
 - define a oahpa_prefix variable for all instances
  ==> DONE


Bugs (as for 2018.07.30):
 (1) interface language does not work 
  Test:
 - go to 
http://gtoahpa-01.uit.no/nuorti/
http://gtoahpa-01.uit.no/aarjel/
 - try to change interface language
 ==> landing on

http://gtoahpa-01.uit.no/

 (2) grammar explanation links do not work for sma_oahpa:
 Test:
 - go to
http://gtoahpa-01.uit.no/aarjel/
 - try to get some explanation from the list offered by the combobox (Grammar explanations) 

http://giellatekno.uit.no/oahpa/sma/gramm/substantiv.nob.html#Akkusativ



