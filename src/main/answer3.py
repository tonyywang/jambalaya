#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Decide the named entity type(person, place) of the answer
from __future__ import division

from rake_nltk import Rake
import spacy
import collections

import sys
import io
from questionTypes import WHType
from questionTypes import BINType
from questionTypes import detect_type
from relationRecord import Record
from relationRecord import keywords_generation
from graphene_extraction import readRecordDict

TOP_K = 10

# python -m spacy download en_core_web_lg
# nlp = spacy.load('en_core_web_lg')
nlp = spacy.load('en')


def read_data(file):
    with open(file) as f:
        data = f.readlines()
    return data


# word, NER, att
# Tom,  PERSON, book
# 3, CARDINAL, people
def dealArg(arg):
	if arg == '':
		return None

	doc = nlp(arg)
	word_tag_list = []

	for token in doc:
		lexicalTags = []
	    if token.dep_ == 'dobj' and token.tag_ != 'NNP' and token.tag_ != '-PRON-':
			for synset in wn.synsets(token):
				lexicalTags.append(synset.lexname())
			for tag in lexicalTags:
				if synset.lexname == noun.location:
					return WHType.WHERE
				if synset.lexname == noun.time:
					return WHType.WHEN
				# if synset.lexname == noun.quantity:
				# 	return WHType.HOWMUCH?
				else:
					sysnet.lexname == noun.location:
					return WHTYPE.WHAT

	    if token.dep_ == 'pobj' and token.tag_ != 'NNP' and token.tag_ != '-PRON-':
	        print(wn.synset(token.lemma_ + '.n.01').lexname)
	        # for synset in list(wn.all_synsets('n'))[:3]:
	        #     print(token.text)
	        #     print(synset)

	# only one sent.
	for sent in doc.sents:
		root_loc = sent.root.i
		root_token = doc[root_loc]
		for ent in doc.ents:
			word_tag_list.append((ent.text, ent.label_))

	# for token in tokens, do word_tag_list.append((word, tag))

	return word_tag_list




def find_relevant_records(dict_records, keywords):
	freq_counter = collections.Counter()
	for rel, list_records in dict_records.items():
		for record in list_records:
			sent, recordKeywords = record.getKeywords()
			matched_words = set(filter(keywords.__contains__, recordKeywords))
			if len(matched_words) != 0:
				freq_counter[record] = len(matched_words)
			# if len(set(keywords).intersection(set(record.getKeywords()))) != 0:

	ranked_records = []
	for record, num_matchwords in freq_counter.most_common():
		ranked_records.append((record, num_matchwords))
	return ranked_records # pair of (record,score)



def answerWH(question_type, ranked_records, keywords):
	for record, score in ranked_records:
		cands = record.findMissingArg(keywords)
		for arg in cands:
			word_tag_list = dealArg(arg)
			for word, tag in word_tag_list:
				if question_type == WHType.WHO:
					if tag in ['PERSON', 'noun.person']:
						return word
				elif question_type == WHType.WHOSE and tag in ['PERSON', 'noun.person']:
					return word
				elif question_type == WHType.WHERE and tag in \
					['LOC', 'FACILITY', 'ORG', 'GPE', 'noun.location']:
						return word  # or return arg3?
				elif question_type == WHType.WHEN and tag in ['DATE', 'noun.time']:
					return word
				elif question_type == WHType.WHOM and tag in ['PERSON', 'noun.person']:  # Need to and this in questionGen
					return word
				elif question_type == WHType.HOW:
					return 'None.something'
				elif question_type == WHType.HOWLONG:
					return 'None.something'
				elif question_type == WHType.HOWOFTEN:
					return 'None.something'

				elif question_type == WHType.HOWMANY and tag in ['CARDINAL', 'noun.quantity']:
					return word
				elif question_type == WHType.WHAT:
					return word  # or None.something
	return None





#'Who is the presentend?'
def answer_question(dict_records, question):
	keywords = keywords_generation(question)
	ranked_records = find_relevant_records(dict_records, keywords)
	# for i in range(10):
	# 	print(str(ranked_records[i][1]))
	# 	ranked_records[i][0].print_record()

	question_type = detect_type(question)
	if isinstance(question_type, WHType):
		return answerWH(question_type, ranked_records, keywords)
	elif isinstance(question_type, BINType):
		if len(ranked_records) != 0:
			answer_record, score = ranked_records[0]
			if score/len(keywords) > 0.5:
				return answer_record.getArg123()
			else:
				return 'No.'
		else:
			return 'No.'
		#return answerBIN(question_type, ranked_records)
	return None


def write_file(filename, sent_list):
	with open(filename, 'w') as f:
		for sent in sent_list:
			f.write(sent[0] + '\n')
			# f.write('\n'.join(sent)+'\r\n')






if __name__ == "__main__":
	# article = sys.argv[1]
	# question_file = sys.argv[2]



	records_file = '../resources/records.txt'
	question_file = '../resources/question_Alessandro_Volta.txt'
	questions = read_data(question_file)

	# questions = ['When did Volta retire?',
	# 			'Who did Alessandro Volta marry?',
	# 			 # 'What did Alessandro Volta invent in 1800?',
	# 			 'When did Alessandro Volta improve  and popularize the electrophorus?',
	# 			 # 'How long was Alessandro Volta a professor at the University of Pavia?',
	# 			 'Where was Volta born?']

	dict_records = readRecordDict(records_file)

	answer_list = []
	for q in questions:
		print(q)
		answer = answer_question(dict_records, q)
		if answer is None:
			answer = 'Woops, no answer.'
		print(answer + '\n\n')

