COLLECT_PARTS := script/sms-Extract-oahpa-mg-xml-from-langs-sms-xml-source.xsl

SAXON := java -Xmx2048m -cp ~/lib/saxon9.jar \
		 -Dfile.encoding=UTF8 net.sf.saxon.Transform \
		 -it:main 

TRANSFORM := java -Xmx2048m -cp ~/lib/saxon9.jar net.sf.saxon.Transform 

XML_SOURCES := proc/A_sms2x.xml \
               proc/Adp_sms2x.xml \
               proc/Adv_sms2x.xml \
               proc/CC_sms2x.xml \
               proc/CS_sms2x.xml \
               proc/Det_sms2x.xml \
               proc/Interj_sms2x.xml \
               proc/N_Prop_sms2x.xml \
               proc/N_sms2x.xml \
               proc/Num_sms2x.xml \
               proc/Pcle_sms2x.xml \
               proc/Pron_sms2x.xml \
               proc/V_sms2x.xml


proc/%.xml: $(GTHOME)/langs/sms/src/morphology/stems/%.xml
	$(TRANSFORM) -s:$< -xsl:$(COLLECT_PARTS) -o:$@

init:
	@mkdir -p proc/

all: init \
	 $(XML_SOURCES)

