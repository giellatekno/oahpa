#!/bin/perl -w
# Perl script to test question-answers pairs for sahka and vasta

use File::Spec;

my $word_pos_list = $ARGV[0];
# to extend for vasta, too
my $s = '\^sahka';
my $lon = 'lookup -flags mbTT -utf8 ~/gtsvn/gt/sme/bin/sme-norm.fst';
my $tmp_file = "tmp_data.txt";
my $out_file = "final_data.txt";

open FILE, $word_pos_list or die $!;

while ( <FILE> ) {
  chomp;
  if (/^\s.*$/) {
    next;
  } else {
    my ($q, $a, $i) = split(/$s/, $_);
    print "question: $q\n";
    print "answer: $a\n";
    print "id: $i\n";
    $i = "QDL ".$i;
    $s = '^sahka';
    my $command1 = "echo '$q $s $a' | preprocess | $lon | lookup2cg |" ;

#    print "$command1\n";

    open (MYFILE1, ">>$tmp_file");
    open (CMD1, $command1);
    while (<CMD1>){
      s/^(\s+\"\^sahka\"\s+)(\?.*)$/$1$i/;
      print MYFILE1;
    }
    print MYFILE1 "\n=========================================================\n\n";
    print "\n=========================================================\n\n";

    close CMD1;
    close (MYFILE1);     

    $s = '\^sahka';
  }    
}

my $command2 = "cat $tmp_file | vislcg3 -g ../sme/src/sme-ped.cg3 |" ;

#    print "$command2\n";

open (MYFILE2, ">>$out_file");

open (CMD2, $command2);
while (<CMD2>){
  print MYFILE2;
}
close CMD2;
close (MYFILE2);     

