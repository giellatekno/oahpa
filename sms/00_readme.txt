sms db update 20130114:

src>comm -12 new_sms-db.txt old_sms-db.txt | wc -l
      51
src>comm -23 new_sms-db.txt old_sms-db.txt | wc -l
     218
src>comm -13 new_sms-db.txt old_sms-db.txt | wc -l
      47
Ergo: There are 47 entries in the old db that are not covered by the new one.
    ==> merging the two dbs.

