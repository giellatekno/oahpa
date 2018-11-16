#java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main old-sjdoahpa2new-sjdoahpa.xsl inDir=src


java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main revert_sjd-data.xsl inDir=src

java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main merge_pos-split-data.xsl inFile=___rus2sjd/a_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main merge_pos-split-data.xsl inFile=___rus2sjd/adv_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main merge_pos-split-data.xsl inFile=___rus2sjd/cs_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main merge_pos-split-data.xsl inFile=___rus2sjd/mwe_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main merge_pos-split-data.xsl inFile=___rus2sjd/n_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main merge_pos-split-data.xsl inFile=___rus2sjd/num_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main merge_pos-split-data.xsl inFile=___rus2sjd/pron_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main merge_pos-split-data.xsl inFile=___rus2sjd/prop_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main merge_pos-split-data.xsl inFile=___rus2sjd/v_russjd.xml 

java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main stat-filter_merged-data.xsl inFile=to_filter_rus/a_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main stat-filter_merged-data.xsl inFile=to_filter_rus/adv_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main stat-filter_merged-data.xsl inFile=to_filter_rus/cs_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main stat-filter_merged-data.xsl inFile=to_filter_rus/mwe_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main stat-filter_merged-data.xsl inFile=to_filter_rus/n_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main stat-filter_merged-data.xsl inFile=to_filter_rus/num_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main stat-filter_merged-data.xsl inFile=to_filter_rus/pron_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main stat-filter_merged-data.xsl inFile=to_filter_rus/prop_russjd.xml 
java -Dfile.encoding=UTF8 net.sf.saxon.Transform -it main stat-filter_merged-data.xsl inFile=to_filter_rus/v_russjd.xml 


