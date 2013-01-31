#!/opt/local/bin/perl -w
# Perl script to test question-answers pairs for sahka and vasta,
# however this is a special version only for vastas
# Lene should decide upon using the same new structure for both vastas and rest
# or whether not.
# usage:
#  perl qa-test_dialogue_vasta-changes.pl vasta_test.xml
# output in tmp_data.txt

use File::Spec;
use XML::Twig;

my $infile = '';
my $mode = 'vastas';
if ($ARGV[0] eq "")
  {
    die "Cannot open file input file!";
  } else {
    $infile = $ARGV[0];
  }
#my $twig = XML::Twig->new(keep_encoding => 1);
my $twig = XML::Twig->new();

my $s = '^'.$mode;

my $lon = 'lookup -flags mbTT -utf8 ~/errortag-gt/gt/sme/bin/ped-sme.fst';
my $tmp_file = "tmp_data.txt";
my $out_file = "final_data.txt";
my $command0 = "rm $tmp_file $out_file" ;
system ($command0) ;

$twig->parsefile($infile);
my $root = $twig->root;

foreach my $test ($root->children('test')){
  my $i =  $test->att('name');
  $i = "QDL ".$i;
  print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
  print "processing =>ID: $i\n";
  my $q = $test->first_child_text('q');
  foreach my $r ($test->children('ag')){
    foreach my $a ($r->children('a')){
      my $a_txt = $a->text();
      print "question: $q \n s: $s \n answer: $a_txt\n";
      my $command1 = "echo '$q $s $a_txt' | preprocess --abbr=../../gt/sme/bin/abbr.txt | $lon | lookup2cg | " ;
      open (TMPFILE, ">>$tmp_file");
      open (CMD1, $command1);
      while (<CMD1>){
	if ($_ !~ m/^(\s+\"\^vastas\"\s+)(.*)$/)
	  {
	    print TMPFILE;
	  }
	if ($_ =~ m/^(\s+\"\^vastas\"\s+)(\?.*)$/){
	  s/^(\s+\"\^vastas\"\s+)(\?.*)$/$1$i/;
	  print TMPFILE;
	  foreach my $l ($r->children('l')){
	    print TMPFILE "\t \"$l->{'att'}->{'base'}\" $l->{'att'}->{'pos'}\n";
	  }
	}
      }
      print TMPFILE "\"<\.>\"\n\n";
      print "=========================================================\n";
      close CMD1;
    }
    close (TMPFILE);
  }
  print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
}

 my $command2 = "cat $tmp_file | vislcg3 -g ../sme/src/sme-ped.cg3  |" ;

 #    print "$command2\n";

 open (ENDFILE, ">>$out_file");

 open (CMD2, $command2);
 while (<CMD2>){
   print ENDFILE;
 }
 close CMD2;
 close (ENDFILE);     

__END__

