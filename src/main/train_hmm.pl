#!/usr/bin/perl

# Noah A. Smith
# 2/21/08
# Code for maximum likelihood estimation of a bigram HMM from 
# column-formatted training data.

# Usage:  train_hmm.pl tags text > hmm-file

# The training data should consist of one line per sequence, with
# states or symbols separated by whitespace and no trailing whitespace.
# The initial and final states should not be mentioned; they are 
# implied.  
# The output format is the HMM file format as described in viterbi.pl.

use bytes;

$init_state = "init";
$final_state = "final";
$OOV_symbol = "OOV";

$tagsfile = shift;
$textfile = shift;
open(TGS, "<$tagsfile") or die "can't open file $tagsfile";
open(TXT, "<$textfile") or die "can't open file $textfile";

while($tags = <TGS> and $text = <TXT>) { # read a sent.'s tags & words
    $prev_tag = $init_state; # we started in the start state (init)
    @T = split /\s+/, $tags;
    @X = split /\s+/, $text;
    for($i = 0; $i < scalar(@T); ++$i) {
	($word, $tag) = ($X[$i], $T[$i]);

	# this block is a little trick to help with out-of-vocabulary (OOV)
	# words.  the first time we see *any* word token, we pretend it
	# is an OOV.  this lets our model decide the rate at which new
	# words of each POS-type should be expected (e.g., high for nouns,
	# low for determiners).
	unless(defined $Voc{$word}) {
	    $Voc{$word} = 1;
	    $word = $OOV_symbol;
	}

	# increment counts
	++$emissions{$tag}{$word};
	++$emissions_den{$tag};
	++$transitions{$prev_tag}{$tag};
	++$transitions_den{$prev_tag};
	$prev_tag = $tag;
    } 
    ++$transitions{$prev_tag}{$final_state};
    ++$transitions_den{$prev_tag};
}

# the rest of the code simply prints out the model in the HMM format

foreach $prev_tag (keys %transitions_den) {
    $d = $transitions_den{$prev_tag};
    foreach $tag (keys %{$transitions{$prev_tag}}) {
	print "trans $prev_tag $tag ", $transitions{$prev_tag}{$tag} / $d, "\n";
    }
}
foreach $tag (keys %emissions_den) {
    $d = $emissions_den{$tag};
    foreach $word (keys %{$emissions{$tag}}) {
	print "emit $tag $word ", $emissions{$tag}{$word} / $d, "\n";
    }
}
