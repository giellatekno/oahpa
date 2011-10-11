echo "Installing lexical and grammatical resources for nu_oahpa (North Sámi)"
echo "======================================================================"
echo "Installing words. Be patient. It can take up to three hours. "
python2.6 install.py --file /home/oahpa/ped/sme/xml/nouns.xml --tagfile /home/oahpa/ped/sme/src/tags.txt --paradigmfile /home/oahpa/ped/sme/src/n_paradigms.txt
echo "Done."
echo "Installing proper nouns... "
python2.6 install.py --file /home/oahpa/ped/sme/xml/propernouns.xml --tagfile /home/oahpa/ped/sme/src/tags.txt --paradigmfile /home/oahpa/ped/sme/src/prop_paradigms.txt
echo "Done."
echo "Installing numerals... "
python2.6 install.py --file /home/oahpa/ped/sme/xml/numerals.xml --tagfile /home/oahpa/ped/sme/src/tags.txt --paradigmfile /home/oahpa/ped/sme/src/num_paradigms.txt
echo "Done."
echo "Installing adjectives... "
python2.6 install.py --file /home/oahpa/ped/sme/xml/adjectives.xml --tagfile /home/oahpa/ped/sme/src/tags.txt --paradigmfile /home/oahpa/ped/sme/src/a_paradigms.txt
echo "Done."
echo "Installing verbs... "
python2.6 install.py --file /home/oahpa/ped/sme/xml/verbs.xml --tagfile /home/oahpa/ped/sme/src/tags.txt --paradigmfile /home/oahpa/ped/sme/src/v_paradigms.txt
echo "Done."

echo "Installing pronouns... "
python2.6 install.py --file /home/oahpa/ped/sme/xml/perspron.xml --tagfile /home/oahpa/ped/sme/src/tags.txt
echo "Done."
echo "Installing adverbs... "
python2.6 install.py --file /home/oahpa/ped/sme/xml/adv_smenob.xml
echo "Done."
echo "Installing multi-word units... "
python2.6 install.py --file /home/oahpa/ped/sme/xml/multiword_smenob.xml
echo "Done."
echo "Installing words from remaining word classes... "
python2.6 install.py --file /home/oahpa/ped/sme/xml/fillings.xml --paradigmfile /home/oahpa/ped/sme/src/paradigms.txt --tagfile /home/oahpa/ped/sme/src/tags.txt
echo "Done."
echo "======================================================================"
echo "Installing the lexicons for nobsme (Norwegian bokmål -> North Sámi)... "
python2.6 install.py --file /home/oahpa/ped/nob/xml/adjectives.xml
python2.6 install.py --file /home/oahpa/ped/nob/xml/nouns.xml
python2.6 install.py --file /home/oahpa/ped/nob/xml/verbs.xml
python2.6 install.py --file /home/oahpa/ped/nob/xml/adverbs.xml
python2.6 install.py --file /home/oahpa/ped/nob/xml/propernouns.xml
echo "Done."
echo "Installing the lexicons for Finnish... "
python2.6 install.py --file /home/oahpa/ped/fin/xml/adjectives.xml
python2.6 install.py --file /home/oahpa/ped/fin/xml/nouns.xml
python2.6 install.py --file /home/oahpa/ped/fin/xml/verbs.xml
python2.6 install.py --file /home/oahpa/ped/fin/xml/propernouns.xml

echo "Done."
echo "Installing the lexicons for Swedish... "
python2.6 install.py --file /home/oahpa/ped/swe/xml/adjectives.xml
python2.6 install.py --file /home/oahpa/ped/swe/xml/nouns.xml
python2.6 install.py --file /home/oahpa/ped/swe/xml/verbs.xml

echo "Done."
echo "======================================================================"
echo "Installing the semantic sets:"
python2.6 install.py --sem /home/oahpa/ped/sme/xml/semantic_sets.xml
echo "Done."
echo " Installing messages... "
python2.6 install.py --messagefile /home/oahpa/ped/sme/xml/messages.xml
echo "Done."
echo "Database nu_oahpa fed with language data."
