#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Wei Wang
# Created: 4/17/2018

from questionTypes import WHType
from questionTypes import BINType

from relationRecord import Record






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

#Who
def whoTemplate(record):
	q = ['Who']
	q.append(record.relation)
	q.append(record.arg2)
	q.append(record.arg3)
	return ' '.join(q) + '?'

print (whoTemplate(Record('gave', 'John', 'the ball', 'to Jim')))