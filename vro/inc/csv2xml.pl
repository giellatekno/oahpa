#!/usr/bin/perl -w
use utf8 ;

# Simple script to convert a lexicon in csv format to Oahpa xml
# For input/output examples, see below.


print STDOUT "<r xml:lang=\"vro\">\n";

while (<>) 
{
	chomp ;
	my ($lemma, $pos, $transl_est) = split /\|/ ;
    #my @semclasses = split /, /, $semclasses ;
	#my @transl_eng = split /[,;\?\!]+\s*/, $transl_eng ;
	#my @transl_rus = split /[,;\?\!]+\s*/, $transl_rus ;
	#my @transl_deu = split /[,;\?\!]+\s*/, $transl_deu ;
	my @transl_est = split /[,;\?\!]+\s*/, $transl_est ;
	print STDOUT "  <e>\n";
	print STDOUT "    <lg>\n";
	print STDOUT "      <l pos=\"$pos\">$lemma</l>\n";
	print STDOUT "    </lg>\n";
	print STDOUT "    <sources>\n";
	print STDOUT "      <book name=\"\" />\n";
	print STDOUT "    </sources>\n";
    print STDOUT "    <mg>\n";
    
    print STDOUT "      <semantics>\n";
    #if ($semclasses) {
     #   foreach $sem (@semclasses) {
      #      print STDOUT "        <sem class=\"$sem\"/>\n";
       # }
    #}
    #else { 
    print STDOUT "        <sem class=\"YYY\"/>\n";  # placeholder for semantic class if there is no semantic class given in the csv file
    #}
	print STDOUT "      </semantics>\n";
	$i = 0;
	print STDOUT "      <tg xml:lang=\"est\">\n";
	foreach $tr (@transl_est)
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
	#$i = 0;
	#print STDOUT "      <tg xml:lang=\"rus\">\n";
	#foreach $tr (@transl_rus)
	#{
	#	if ($i == 0) {		  
	#	  print STDOUT "        <t stat=\"pref\">$tr</t>\n";
     #   }
	#	else {
	#	  print STDOUT "        <t>$tr</t>\n";
     #   }
	#	$i++;
	#}
	#print STDOUT "      </tg>\n";
	
	#$i = 0;
	#print STDOUT "      <tg xml:lang=\"fin\">\n";
	#foreach $tr (@transl_fin)
	#{
	#	if ($i == 0) {
	#	  print STDOUT "        <t stat=\"pref\">$tr</t>\n";
     #   }
	#	else {
	#	  print STDOUT "        <t>$tr</t>\n";
     #   }
	#	$i++;
	#}
	#print STDOUT "      </tg>\n";
    print STDOUT "    </mg>\n";
    print STDOUT "  </e>\n";
}

print STDOUT "</r>\n";




# Example input:
#
# tüü|n|töö
# kuldnõ|a|kuldne


#Target output:
#
# <e>
#    
#   </e>


