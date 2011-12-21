DATO=`date`

echo "Dato: $DATO" > nudoc/gen/finsme_nounlist.txt
cat ../sme/finsme/n_finsme.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/n_finsme.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:/' | sed 's/>l /€lemma:/' | sed 's/>t/:/' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/finsme_nounlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/finsme_adjlist.txt
cat ../sme/finsme/a_finsme.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/a_finsme.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:/' | sed 's/>l /€lemma:/' | sed 's/>t/:/' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/finsme_adjlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/finsme_advlist.txt
cat ../sme/finsme/adv_finsme.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/adv_finsme.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>l /€lemma:   /' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/finsme_advlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/finsme_vlist.txt
cat ../sme/finsme/v_finsme.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/v_finsme.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>l /€lemma:   /' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/finsme_vlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/finsme_mwelist.txt
cat ../sme/finsme/mwe_finsme.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/finsme/mwe_finsme.xml |  sed 's/ </$</' | tr "\n" " " | tr "$" "\n" |egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>l /€lemma:   /' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/finsme_mwelist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/smefin_nounlist.txt
cat ../sme/src/n_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/src/n_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t .*stat="pref"/fasihtta:       /' | sed 's/>t .* tcomm="yes"/tcomm:       /' | sed 's/>l /€lemma:   /' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/smefin_nounlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/smefin_adjlist.txt
cat ../sme/src/a_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/src/a_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>t .* tcomm="yes"/tcomm:       /' |  sed 's/>l /€lemma:   /' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/smefin_adjlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/smefin_advlist.txt
cat ../sme/src/adv_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/src/adv_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>t .* tcomm="yes"/tcomm:       /' |  sed 's/>l /€lemma:   /' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/smefin_advlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/smefin_vlist.txt
cat ../sme/src/v_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/src/v_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' |  sed 's/>t .* tcomm="yes"/tcomm:       /' | sed 's/>l /€lemma:   /' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/smefin_vlist.txt
rm oassi* 

echo "Dato: $DATO" > nudoc/gen/smefin_mwelist.txt
cat ../sme/src/multiword_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f3 > oassi2
cat ../sme/src/multiword_smenob.xml | sed 's/ </$</' | tr "\n" " " | tr "$" "\n" | sed 's/<tg/$<tg/' | sed 's/<l/$<l/' | tr "\n" "€" | tr "$" "\n" | egrep '(<l |"fin")' | tr "€" "\n" | egrep '(<l |<t)' | grep -v '<tg' | tr -s " " | tr "<" ">" | cut -d ">" -f1,2 > oassi1
cat oassi1 | sed 's/>t pos=".*" stat="pref"/fasihtta:       /' | sed 's/>t .* tcomm="yes"/tcomm:       /' |  sed 's/>l /€lemma:   /' | sed 's/>t/:   /' | cut -d ":" -f1 > oassinew1
paste -d "_" oassinew1 oassi2 | tr "€" "\n" |  sed 's/_/: /' | sed 's/lemma:/lemma:   /' | sed 's/^ //' | sed 's/^:/   -     /' >> nudoc/gen/smefin_mwelist.txt
rm oassi* 

