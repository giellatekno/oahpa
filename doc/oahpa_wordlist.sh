DATO=`date`

echo "Dato: $DATO" > nudoc/gen/finsme_nounlist.txt
cat ../sme/finsme/n_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/n_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos="n" stat="pref"/fasihtta:       /' | sed 's/>l pos="n"/€lemma:/' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/ - /' | sed 's/^ //' >> nudoc/gen/finsme_nounlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/finsme_adjlist.txt
cat ../sme/finsme/a_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/a_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>l pos="a"/€lemma:/' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/ - /' | sed 's/^ //' >> nudoc/gen/finsme_adjlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/finsme_advlist.txt
cat ../sme/finsme/adv_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/adv_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>l pos="adv"/€lemma:/' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/ - /' | sed 's/^ //' >> nudoc/gen/finsme_advlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/finsme_vlist.txt
cat ../sme/finsme/v_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/v_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>l pos="v"/€lemma:/' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/ - /' | sed 's/^ //' >> nudoc/gen/finsme_vlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/finsme_mwelist.txt
cat ../sme/finsme/mwe_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/mwe_finsme.xml | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>l pos=".*"/€lemma:/' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 |  sed 's/_/ - /' | sed 's/^ //' | tr "€" "\n" >> nudoc/gen/finsme_mwelist.txt
rm oassi* 
