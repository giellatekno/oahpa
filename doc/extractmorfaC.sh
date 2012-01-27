# list of command making jspwiki document

DATO=`date`

# Printing headers:
echo "!!!Oversikt over Morfa-C oppgaver" > nudoc/morfac_questions.jspwiki
echo "" >> nudoc/morfac_questions.jspwiki
echo "Testdato: $DATO" >> nudoc/morfac_questions.jspwiki
echo "" >> nudoc/morfac_questions.jspwiki
echo "Oppgavene lagres i sme/meta/*_question.xml" >> nudoc/morfac_questions.jspwiki
echo "!!Verb" >> nudoc/morfac_questions.jspwiki
cat ../sme/meta/verb_questions.xml | egrep '(text|<q |<id>|<sem c)' | tr -s "\t " | tr "\t" " " | sed 's/^</ </' | sed 's/^ <q /\! <q /' |  sed 's/^ <\!-- <q /\! <\!-- <q /' |  sed 's/^ /* /' >> nudoc/morfac_questions.jspwiki
echo "" >> nudoc/morfac_questions.jspwiki
echo "!!Substantiv" >> nudoc/morfac_questions.jspwiki
cat ../sme/meta/noun_questions.xml | egrep '(text|<q |<id>|<sem c)' | tr -s "\t " | tr "\t" " " | sed 's/^</ </' | sed 's/^ <q /\! <q /' |  sed 's/^ <\!-- <q /\! <\!-- <q /' |  sed 's/^ /* /' >> nudoc/morfac_questions.jspwiki
echo "" >> nudoc/morfac_questions.jspwiki
echo "!!Adjektiv" >> nudoc/morfac_questions.jspwiki
cat ../sme/meta/adjective_questions.xml | egrep '(text|<q |<id>|<sem c)' | tr -s "\t " | tr "\t" " " | sed 's/^</ </' | sed 's/^ <q /\! <q /' |  sed 's/^ <\!-- <q /\! <\!-- <q /' |  sed 's/^ /* /' >> nudoc/morfac_questions.jspwiki
echo "" >> nudoc/morfac_questions.jspwiki
echo "!!Numeraler" >> nudoc/morfac_questions.jspwiki
cat ../sme/meta/numeral_questions.xml | egrep '(text|<q |<id>|<sem c)' | tr -s "\t " | tr "\t" " " | sed 's/^</ </' | sed 's/^ <q /\! <q /' |  sed 's/^ <\!-- <q /\! <\!-- <q /' |  sed 's/^ /* /' >> nudoc/morfac_questions.jspwiki
echo "" >> nudoc/morfac_questions.jspwiki
echo "!!Pronomener" >> nudoc/morfac_questions.jspwiki
cat ../sme/meta/pron_questions.xml | egrep '(text|<q |<id>|<sem c)' | tr -s "\t " | tr "\t" " " | sed 's/^</ </' | sed 's/^ <q /\! <q /' |  sed 's/^ <\!-- <q /\! <\!-- <q /' |  sed 's/^ /* /' >> nudoc/morfac_questions.jspwiki





