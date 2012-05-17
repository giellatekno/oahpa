P="python2.6"
DATA=../sjd
SJD="$DATA/src"
RUS="$DATA/russjd"
$P install.py -f $SJD/a_sjdrus.xml
$P install.py -f $SJD/adv_sjdrus.xml
$P install.py -f $SJD/cs_sjdrus.xml
$P install.py -f $SJD/mwe_sjdrus.xml
$P install.py -f $SJD/n_sjdrus.xml
$P install.py -f $SJD/num_sjdrus.xml
$P install.py -f $SJD/pron_sjdrus.xml
$P install.py -f $SJD/prop_sjdrus.xml
$P install.py -f $SJD/v_sjdrus.xml
$P install.py -f $RUS/a_russjd.xml
$P install.py -f $RUS/adv_russjd.xml
$P install.py -f $RUS/cs_russjd.xml
$P install.py -f $RUS/mwe_russjd.xml
$P install.py -f $RUS/n_russjd.xml
$P install.py -f $RUS/num_russjd.xml
$P install.py -f $RUS/pron_russjd.xml
$P install.py -f $RUS/prop_russjd.xml
$P install.py -f $RUS/v_russjd.xml

$P install.py --sem $DATA/meta-data/semantical_sets.xml

