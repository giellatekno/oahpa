#!/usr/bin/perl -w
use strict;
use utf8;

# These definitions ensure that the script works 
# also in environments, where PERL_UNICODE is not set.
binmode( STDIN, ':utf8' );
binmode( STDOUT, ':utf8' );
binmode( STDERR, ':utf8' );
use open 'utf8';

my @aff_ans=("verb", "pron verb", "pron verb obj");
my @neg_ans=("neg conneg", "neg conneg obj");
my %aff;
my %neg;
my %buorre;

my $verb="juhkat";
my $obj="gáffe";

my $conneg="V+Ind+Prs+ConNeg";
my $neg="ii+V+Neg+Ind";

my $mainv_obj="verb+MV_GRAM+go noun+N+Sg+Acc";

my $mv_gram="V+Ind+Prs";

my %pairs = (
			 "Sg1" => "Sg2",
			 "Sg2" => "Sg1",
			 "Sg3" => "Sg3",
			 "Du1" => "Du2",
			 "Du2" => "Du1",
			 "Du3" => "Du3",
			 "Pl1" => "Pl2",
			 "Pl2" => "Pl1",
			 "Pl3" => "Pl3",
			 );

my %pron = (
				"Sg1" => "mun",
				"Sg2" => "don",
				"Sg3" => "son",
				"Du1" => "moai",
				"Du2" => "doai",
				"Du3" => "soai",
				"Pl1" => "mii",
				"Pl2" => "dii",
				"Pl3" => "sii",
			 );


my $lang="sme";
my $preprocess="preprocess --abbr=/opt/smi/$lang/bin/abbr.txt";
my $lookup="lookup -flags mbTT -utf8 /opt/smi/$lang/bin/$lang.fst";
my $generate="lookup -flags mbTT -utf8 /opt/smi/$lang/bin/i$lang.fst";
my $disamb="lookup2cg | vislcg --grammar=/opt/smi/$lang/bin/$lang-dis.rle";
my $all="$preprocess | $lookup | $disamb";

print "Type exit if you want to quit\n";

my $line="";

while($line !~ /(exit|quit)/) {
	
	print "What do you want to practice?: Sg1, Sg2, Sg3, Du1, Du2, Du3, Pl1, Pl2 or Pl3\n";
	$line = <>;
	chomp $line;
	my $person;
	my $ans_person;
	if ($line !~ /(exit|quit)/ && $pairs{$line}) { 
		$person = $pairs{$line};
		$ans_person = $line;
	}
	else { last; }
	format_answers($ans_person, $verb, $obj, \%aff, \%neg, \%buorre);
	#for my $k (keys %aff) {
	#	print "$ans_person JEE $k\n";
	#}
	my $gen_v= $verb . "+" . $mv_gram . "+" . $person . "+Qst";
	my $ans=`echo $gen_v | $generate 2>/dev/null`;
	$ans =~ s/\n//g;
    my $analysis;
    my $v_form;
	($analysis, $v_form) = split("\t", $ans);

	my $gen_o= $obj . "+N+Sg+Acc";
	$ans=`echo $gen_o | $generate 2>/dev/null`;
	$ans =~ s/\n//g;
    my $o_form;
	($analysis, $o_form) = split("\t", $ans);
	print ucfirst($v_form), " $o_form" . "?\n";

	$line = <>;
	chomp $line;
	while($line !~ /(exit|quit)/) {
         $line =~ s/^(De|Juo)\s*//g;
         $line =~ s/[\.\,\!]//g;
         #print "OK $line\n";
         if( $aff{$line} || $aff{lcfirst($line)} ) { print ucfirst($buorre{leage}), " $buorre{buorre}!\n"; print "***\n"; last; }
         elsif($neg{lcfirst($line)}) { print "$v_form maidege?\n"; }
         else { print "Error, try again, or type exit to quit.\n"; }
         $line = <>;
         chomp $line;
	}
}


sub format_answers {
	my ($ans_person, $verb, $object, $aff_href, $neg_href, $buorre_href) = @_;

	my %forms;

	my $gen_v= $verb . "+" . $mv_gram . "+" . $ans_person;
	my $v_form = generate($gen_v);
	$forms{verb} = $v_form;

	$gen_v= $neg . "+" . $ans_person;
	$v_form = generate($gen_v);
	$forms{neg} = $v_form;

	$gen_v= $verb . "+" . $conneg;
	$v_form = generate($gen_v);
	$forms{conneg} = $v_form;

	$gen_v= $object . "+N+Sg+Acc";
	$v_form = generate($gen_v);
	$forms{obj} = $v_form;

	$gen_v= "leat+V+Imprt+Prs+" . $pairs{$ans_person};
	$v_form = generate($gen_v);
	$$buorre_href{leage} = $v_form;

	(my $number = $pairs{$ans_person}) =~ s/\d//g;
	if ($number eq "Du") { $number = "Pl"; }
	$gen_v= "buorre+A+" . $number . "+Nom";
	$v_form = generate($gen_v);
	$$buorre_href{buorre} = $v_form;

	return if (! $ans_person);
	for my $a (@aff_ans) {
		my $ans="";
		my @forms= split(/\s+/, $a);
		for my $f (@forms) {
			if ($ans) { $ans .= " "; }
			if ($f eq "pron") {
				$ans .= $pron{$ans_person};
			}
			else { $ans .= $forms{$f}; }		
		}
		$$aff_href{$ans} = 1;
	}
	for my $a (@neg_ans) {
		my $ans="";
		my @forms= split(/\s+/, $a);
		for my $f (@forms) {
			if ($ans) { $ans .= " "; }
			if ($f eq "pron") {
				$ans .= $pron{$ans_person};
			}
			else { $ans .= $forms{$f}; }		
		}
		$$neg_href{$ans} = 1;
	}
}

sub generate {
	my $gen_v = shift;
	
	my $generated=`echo $gen_v | $generate 2>/dev/null`;
	($generated) = split(/\n/, $generated);
	my ($analysis, $v_form) = split("\t", $generated);
	return $v_form;
}
