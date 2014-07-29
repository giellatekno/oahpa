#!/usr/bin/perl -w
#
# Perl script for generating dialogues froma the
# file dialogue_theme.xml
#
# Usage: generate_dialogue.pl [OPTIONS] dialogue_theme.xml
#
# $Id: generate_dialogue.pl 25426 2009-04-21 09:48:21Z boerre $

use utf8;

# These definitions ensure that the script works 
# also in environments, where PERL_UNICODE is not set.
binmode( STDIN, ':utf8' );
binmode( STDOUT, ':utf8' );
binmode( STDERR, ':utf8' );
use open 'utf8';

use Carp;
use pedTools::XMLStruct;

my $diafile;
my $topicfile;
my $tree;
my $interactive;
my $help;

use Getopt::Long;
Getopt::Long::Configure ("bundling");
GetOptions ("dialogues|d=s" => \$diafile,
			"full|f" => \$full,
			"tree|t" => \$tree,
			"interactive|i" => \$interactive,
			"help|h" => \$help,
			);

if ($help) { print_help(); }

my @topic_list;
my %topics;
$topicfile = $ARGV[$#ARGV];

#parse_dialogue("cafe", $diafile, \@topic_list);

parse_topics("cafe", $topicfile, \%topics, \@topic_list, \$opening);
if ($opening) { print "$opening\n"; }

if ($full) { print_all_questions(); }
if ($tree) { print_tree(); }

if (! $interactive) { exit; }

for my $t (@topic_list) {
	if ($topics{$t}{opening}) { print "$topics{$t}{opening}\n"; }
	my $q = $topics{$t}{first};
	process_question($q, $t);
	if ($topics{$t}{closing}) { print "$topics{$t}{closing}\n"; }
}

sub process_question {
	my ($q, $t) = @_;

	return if (! $q);
	(my $qstring = $q) =~ s/_/ /g;
	print "$qstring?\n";
	print ": ";

	my $ans=<STDIN>;
	chomp $ans;
	my $action;

	if ($ans eq "y") { $action = "aff"; }
	elsif ($ans eq "n") { $action = "neg";}
	elsif ($ans eq "1") { $action = "alt1";}
	elsif ($ans eq "2") { $action = "alt2";}
	if (! $topics{$t}{$q}{$action}) { $action = "default"; }
	if (! $topics{$t}{$q}{$action}) { print "No actions, moving to next topic.\n"; return; }

	if ($topics{$t}{$q}{$action}{utt}) { 
		for my $u ( @{$topics{$t}{$q}{$action}{utt}}) { 
			$u =~ s/_/ /g;
			print "$u\n"; 
		}
	}
#	elsif ($topics{$t}{$q}{$action}{ulink}) { 
#		(my $utt = $topics{$t}{$q}{$action}{ulink}) =~ s/_/ /g;
#		print "$utt\n";
#	}
	if ($topics{$t}{$q}{$action}{qlink}) {
		process_question($topics{$t}{$q}{$action}{qlink}, $t);
	}
	else {print "(End of question)\n"; }

}


sub print_tree {

	for my $t (@topic_list) {
		if ($topics{$t}{opening}) { print "$topics{$t}{opening}\n"; }
		my $q = $topics{$t}{first};
		my $embed="";
		print_question($q, $t, $embed);
		if ($topics{$t}{closing}) { print "$topics{$t}{closing}\n"; }
		print "\n";
	}

}
sub print_question {
	my ($q, $t, $embed) = @_;

	return if (! $q);
	(my $qstring = $q) =~ s/_/ /g;
	print "$embed Q: $qstring?\n";
	$embed .= "    ";
	my $action;
	for my $action ("alt1","alt2","aff","pos","neg","default") {
		if ($topics{$t}{$q}{$action}) {
			print "$embed $action:\n";
			for my $u ( @{$topics{$t}{$q}{$action}{utt}}) { 
				$u =~ s/_/ /g;
				print "$embed U: $u\n";
			}
#			if ($topics{$t}{$q}{$action}{ulink}) { 
#				(my $utt = $topics{$t}{$q}{$action}{ulink}) =~ s/_/ /g;
#				print "$embed U: $u.\n";
#			}
			if ($topics{$t}{$q}{$action}{qlink}) { 
				print_question($topics{$t}{$q}{$action}{qlink}, $t, $embed);
			}
		}
	}
}

sub print_all_questions {

	for my $t (@topic_list) { 
		print "TOPIC $t\n";
		if ($topics{$t}{opening}) { print "OPENING $topics{$t}{opening}\n"; }
		for my $k2 (keys %{$topics{$t}}) {
			next if ($k2 eq "opening" || $k2 eq "closing" || $k2 eq "first");
			print "  QUESTION $k2\n";
			for my $k3 (keys %{$topics{$t}{$k2}}) {
				print "    ACTION $k3\n";
				for my $k4 (keys %{$topics{$t}{$k2}{$k3}}) {
					print "      TYPE $k4\n";
					if ($k4 eq "utt") {
						print "        $topics{$t}{$k2}{$k3}{$k4}\n";
					}
					else { print "        LINK $topics{$t}{$k2}{$k3}{$k4}\n"; }
				}
			}
		}
		if ($topics{$t}{closing}) { print "CLOSING $topics{$t}{closing}\n"; }
		print "\n";
	}
}

sub print_help {
	print <<END;
Usage: generate_dialogue.pl [OPTIONS] FILE
The available options:
    --dialogues=<file> name of the main dialogue file
    -d <file>
    --full             print all the questions and utterances unordered
    -f
    --tree             generate full dialogue tree with all the branches
    -t
    --interactive      conversation with the program
    -i 
    --help             this help and exit
END
};

