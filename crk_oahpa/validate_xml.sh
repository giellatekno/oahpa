ls -c1 ../crk/src/*.xml ../crk/meta/*.xml ../crk/meta/verb_questions/*.xml | xargs xmllint --format 1>err.tmp
rm err.tmp
