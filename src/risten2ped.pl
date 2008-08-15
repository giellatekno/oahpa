  
  
#!/usr/bin/perl -w

# Minimalistic perl script to move from risten input to 
# ped xml output.
#  <entry>
#    <lemma>Skánit</lemma>
#	<pos class="N"/>
#    <translations>
#      <tr xml:lang="nob">Skånland</tr>
#    </translations>
#    <semantics>
#      <sem class="PLACE-NAME-PL"/>
#    </semantics>
#    <stem class="bisyllabic" diphthong="no" gradation="no"/>
#    <dialect class=""/>
#    <sources>
#    </sources>
#  </entry>

use encoding 'utf-8';

while ($line = <> ) {
    chomp $line;
    ($sme,
     $nob)
	= split /\t/, $line ;
#    print "samisk: $sme\n";
#    print "pos: $smepos\n";
    print "  <entry>\n    <lg>\n      <lemma>$sme</lemma>\n    <pos class=\"N\"/>\n    <translations>\n      <tr xml:lang=\"nob\">$nob</tr>\n    </translations>\n    <semantics>\n      <sem class=\"PLACE-NAME\"/>\n    </semantics>\n      <stem class=\"bisyllabic\" diphthong=\"no\" gradation=\"yes\" rime=\"\"/>\n    <dialect class=\"\"/>\n    <sources>\n    </sources>\n  </entry>\n\n" ;

}
  