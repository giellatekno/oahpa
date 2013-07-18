#!/usr/bin/perl -w
use utf8 ;

# Simple script to convert csv to xml
# For input/output examples, see below.


print STDOUT "<r xml:lang=\"ru\">\n";

while (<>) 
{
	chomp ;
	my ($lemma, $lemma_stressed, $pos, $zaliznjak, $book, $chapter, $transl_eng, $transl_dan, $transl_nob, $semclasses, $aspect, $motion) = split /;/ ;
	my @semclasses = split /, /, $semclasses ;
	my @transl_eng = split /, /, $transl_eng ;
	my @transl_dan = split /, /, $transl_dan ;
	my @transl_nob = split /, /, $transl_nob ;
	print STDOUT "  <e>\n";
	print STDOUT "    <lg>\n";
	print STDOUT "      <l pos=\"$pos\" zaliznjak=\"$zaliznjak\">$lemma</l>\n";
	print STDOUT "      <lemma_stressed>$lemma_stressed</lemma_stressed>\n";
	print STDOUT "    </lg>\n";
	print STDOUT "    <sources>\n";
	print STDOUT "      <book name=\"$book\" chapter=\"$chapter\"/>\n";
	print STDOUT "    </sources>\n";
    print STDOUT "    <mg>\n";
    if ($semclasses) {
    print STDOUT "      <semantics>\n";
	foreach $sem (@semclasses) {
		print STDOUT "        <sem class=\"$sem\"/>\n";
	}
	print STDOUT "      </semantics>\n";
	}
	$i = 0;
	print STDOUT "      <tg xml:lang=\"eng\">\n";
	foreach $tr (@transl_eng)
	{
		if ($i == 0) {
		  print STDOUT "        <t stat=\"pref\">$tr</t>\n";
        }
		else {
		  print STDOUT "        <t>$tr</t>\n";
        }
		$i++;
	}
	print STDOUT "      </tg>\n";
	$i = 0;
	print STDOUT "      <tg xml:lang=\"dan\">\n";
	foreach $tr (@transl_dan)
	{
		if ($i == 0) {		  
		  print STDOUT "        <t stat=\"pref\">$tr</t>\n";
        }
		else {
		  print STDOUT "        <t>$tr</t>\n";
        }
		$i++;
	}
	print STDOUT "      </tg>\n";
	$i = 0;
    print STDOUT "      <tg xml:lang=\"nob\">\n";
	foreach $tr (@transl_nob)
	{
		if ($i == 0) {
		  print STDOUT "        <t stat=\"pref\">$tr</t>\n";
        }
		else {
		  print STDOUT "        <t>$tr</t>\n";
        }
		$i++;
	}
	print STDOUT "      </tg>\n";
    print STDOUT "    </mg>\n";
    if ($aspect) {
	   print STDOUT "    <aspect>$aspect</aspect>\n";
	}
	if ($motion) {
	   print STDOUT "    <motion>$motion</motion>\n";
    }	
	print STDOUT "  </e>\n";
}

print STDOUT "</r>\n";




# Example input:
#
# читать;читáть;v; 1a;MiP;L9;read;læse;lese;;прочита́ть;


#Target output:
#
# <e>
#      <lg>
#         <l pos="v" zaliznjak="1a">читать</l>
#         <lemma_stressed>читáть=<lemma_stressed/>
#      </lg>
#      <sources>
#         <book name="MiP" chapter="L9"/>
#      </sources>
#      <mg>
#         <semantics>
#            <sem class=""/>
#         </semantics>
#         <tg xml:lang="eng">
#            <t stat="pref">read</t>
#         </tg>
#         <tg xml:lang="dan">
#            <t stat="pref">læse</t>
#         </tg>
#         <tg xml:lang="nob">
#            <t pos="n" stat="pref">lese</t>
#         </tg>
#      </mg>
#       <aspect>прочита́ть</aspect>
#   </e>


