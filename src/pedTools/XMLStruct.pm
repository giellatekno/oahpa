
package pedTools::XMLStruct;

use utf8;
use warnings;
use strict;

use XML::Twig;
use Carp qw(cluck);

use Exporter;
our ($VERSION, @ISA, @EXPORT, @EXPORT_OK);

#$VERSION = sprintf "%d.%03d", q$Revision$ =~ /(\d+)/g;
@ISA         = qw(Exporter);

@EXPORT = qw(&parse_dialogue &parse_topics);

#our (%topic);


sub parse_dialogue {
	my ($name, $file, $topics_aref) = @_;

	print "$file\n";
	my $document = XML::Twig->new(twig_handlers => {  
		'dialogue[@name="visit"]' => sub { get_topics(@_, $topics_aref); }
	});

	if (! $document->safe_parsefile ($file)) {
		cluck("Couldn't parse xml: $@");
		return Carp::longmess("Could not parse xml");
	}
	
}

sub get_topics {
	my ($twig, $dialogue, $topics_aref) = @_;

	my @topics = $dialogue->children('topic');
	for my $t (@topics) { push (@$topics_aref, $t->{'att'}->{'name'}); }	
}


sub parse_topics {
	my ($name, $file, $topic_href, $topics_aref, $opening) = @_;
	
	my $document = XML::Twig->new(twig_handlers => {  
		'topic' => sub { parse_topic(@_, $topic_href, $topics_aref); },
		'opening' => sub { $$opening = $_[1]->first_child_text('utt'); }
	});
	
	if (! $document->safe_parsefile ($file)) {
		cluck("Couldn't parse xml: $@");
		return Carp::longmess("Could not parse xml");
	}
	
}

sub parse_topic {
	my ($twig, $topic, $topic_href, $topics_aref) = @_;

	my $t = $topic->{'att'}->{'name'};
	push (@$topics_aref, $t);

	my $op = $topic->first_child('opening');
	if ($op) { $$topic_href{$t}{opening} = $op->text; }

	my $cl = $topic->first_child('closing');
	if ($cl) { $$topic_href{$t}{closing} = $cl->text;}

	for my $q ($topic->children('question')) {
		my $qname = $q->{'att'}->{'name'};
		if (! $$topic_href{$t}{first}) { $$topic_href{$t}{first} = $qname; }
		my $aff = $q->first_child('aff');
		my $neg = $q->first_child('neg');
		my $pos = $q->first_child('pos');
		my $default = $q->first_child('default');

		for my $el ($aff,$neg,$default,$pos) {
			next if (! $el );
			my $elname = $el->name;
			my $qlink = $el->{'att'}->{'qlink'};
			my @utt;
			for my $u ($el->children('utt')) { 
				my $utt_text=$u->text;
				if ($utt_text) { push (@utt, $utt_text);}
				if ($u->{'att'}->{'link'}) { push (@utt, $u->{'att'}->{'link'});}
			}
			if ($qlink) { $$topic_href{$t}{$qname}{$elname}{qlink} = $qlink; }
			#if ($ulink) { $$topic_href{$t}{$qname}{$elname}{ulink} = $ulink; }
			if (@utt) { $$topic_href{$t}{$qname}{$elname}{utt} = [ @utt ]; }
		}
	}
}
