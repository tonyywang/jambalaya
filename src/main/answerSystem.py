#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Wei Wang
# Created: 4/17/2018




from rake_nltk import Rake
import spacy
import collections

import sys
import io

from questionTypes import WHType
from questionTypes import BINType
from questionTypes import detect_type

from relationRecord import Record

TOP_K = 10


def read_data(file):
    with open(file) as f:
        data = f.readlines()
    return data





# Generate keywords for quetion
def keywords_generation(question):
	r = Rake()
	r.extract_keywords_from_text(question)
	keywords = r.get_ranked_phrases()
	return keywords



def find_relevant_record(keywords, records):
	for record in records:
		matched = record.match_keywords(keywords)
		print(matched)

keywords = keywords_generation('Who gave the ball to Jim?')
records = [Record('gave', 'John', 'the ball', 'to Jim')]
find_relevant_record(keywords, records)


# topK Most Relevant Sentences
def find_relevant_sentences(keywords, article):
	nlp = spacy.load('en')
	article_dict = collections.Counter()
	for sentence in article:
		tokens = set()
		doc = nlp(sentence)
		for token in doc:
			tokens.add(str(token))
		matched_words = set(filter(set(keywords).__contains__, tokens))
		article_dict[sentence] = len(matched_words)

	relevant_sents = []
	for (sentence, num_matchwords) in article_dict.most_common(TOP_K):
		relevant_sents.append(sentence)

	return relevant_sents