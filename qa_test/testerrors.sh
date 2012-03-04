# finner fram de svarene som ikke gir error-tag etter å ha kjørt qa-test_dialogue.pl på errortest-fil

cat final_data.txt | grep -v "^;" | sed 's/^$/¥/' | sed 's/\^.a.*"/¢/' | tr "\n" "€" | tr "¥" "\n" | cut -d "¢" -f2- | egrep -v "&" | egrep '[a-zA-Z]' | less


