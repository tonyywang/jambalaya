#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Decide the named entity type(person, place) of the answer
from __future__ import division

import spacy
import collections

import sys
import io
from questionTypes import WHType
from questionTypes import BINType
from questionTypes import detect_type
from questionTypes import TAGList
from relationRecord import Record
from relationRecord import keywords_generation
from graphene_extraction import readRecordDict
from nltk.corpus import wordnet as wn

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
	word_tag_list = set()

	# only one sent.
	for sent in doc.sents:
		root_loc = sent.root.i
		root_token = doc[root_loc] # not being used? -Tony

		for ent in doc.ents:
			word_tag_list.add((ent.text, ent.label_))

	for token in doc:
		# lexicalTags = set()
		if token.dep_ == 'nsubj' or token.dep_ == 'dobj' or token.dep_ == 'pobj':
			if token.ent_type_ == "":
				if token.tag_ != 'NNP' and token.tag_ != '-PRON-':
					for synset in wn.synsets(token.text):
						# word_tag_list.add((token.text, synset.lexname))
						if synset.lexname() == 'noun.person':
							print(token.text)
							word_tag_list.add((token.text, 'noun.person'))
						elif synset.lexname() == 'noun.group':
							print(token.text)
							word_tag_list.add((token.text, 'noun.group'))
						elif synset.lexname() == 'noun.location':
							print(token.text)
							word_tag_list.add((token.text, 'noun.location'))
						elif synset.lexname() == 'noun.time':
							print(token.text)
							word_tag_list.add((token.text, 'noun.time'))
						elif synset.lexname() == 'noun.quantity':
							print(token.text)
							word_tag_list.add((token.text, 'noun.quantity'))

		# word_tag_list.append([tagset for tagset in lexicalTags])

	# for token in tokens, do word_tag_list.append((word, tag))

	# print(word_tag_list)

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
		if question_type != WHType.WHAT:
			cands = record.findMissingArg(keywords)
			if len(cands) == 0:
				return None
			for arg in cands:
				word_tag_list = dealArg(arg)
				for word, tag in word_tag_list:
					when_list = [WHType.WHEN, WHType.WHATTIME, WHType.WHATYEAR, WHType.WHATMONTH, WHType.WHATDAY]
					if (question_type == WHType.WHO or question_type == WHType.WHOSE or question_type == WHType.WHOM) \
						and tag in TAGList.WHO_TAGS.value:
						return word
					elif question_type == WHType.WHERE and tag in TAGList.WHERE_TAGS.value:
						return word  # or return arg3?
					elif question_type in when_list and tag in TAGList.WHEN_TAGS.value:
						return word
					elif question_type == WHType.HOW and tag in TAGList.HOW_TAGS.value:
						return word
					elif question_type == WHType.HOWLONG and tag in TAGList.HOWLONG_TAGS.value:
						return word
					elif question_type == WHType.HOWOFTEN and tag in TAGList.HOWOFTEN_TAGS.value:
						return word
					elif question_type == WHType.HOWMANY and tag in TAGList.HOWMANY_TAGS.value:
						return word
					elif question_type == WHType.HOWMUCH and tag in TAGList.HOWMUCH_TAGS.value:
						return word
					elif question_type == WHType.HOWOLD and tag in TAGList.HOWOLD_TAGS.value:
						return word
		else:
			ans = record.isMissingArg2(keywords)
			if ans is not None:
				return ans

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
		answer_wh = answerWH(question_type, ranked_records, keywords)
		if answer_wh is not None:
			return answer_wh
		elif len(ranked_records) != 0:
			# return best relevant sentence
			answer_record, score = ranked_records[0]
			return answer_record.getArg123()

	elif isinstance(question_type, BINType):
		if len(ranked_records) != 0:
			answer_record, score = ranked_records[0]
			if score/len(keywords) > 0.5:
				return answer_record.getArg123()
			else:
				return 'No.'
		else:
			return 'No.'

	# return best relevant sentence
	if len(ranked_records) != 0:
		answer_record, score = ranked_records[0]
		return answer_record.getArg123()

	return None


def write_file(filename, sent_list):
	with open(filename, 'w') as f:
		for sent in sent_list:
			f.write(sent[0] + '\n')
			# f.write('\n'.join(sent)+'\r\n')






if __name__ == "__main__":
	records_file = sys.argv[1]
	question_file = sys.argv[2]
	questions = read_data(question_file)

	# records_file = '../resources/records_Alessandro_Volta.txt'
	# question_file = '../resources/question_Alessandro_Volta.txt'
	# questions = read_data(question_file)

	# records_file = '../resources/records_Cougar.txt'
	# questions = ["How long are cougar adult males (from nose to tail)?"]
	# questions = ['What did Alessandro Volta invent in 1800?',
	# 			 'When did Volta retire?',
	# 			'Who did Alessandro Volta marry?',
	# 			 'When did Alessandro Volta improve  and popularize the electrophorus?',
	# 			 # 'How long was Alessandro Volta a professor at the University of Pavia?',
	# 			 'Where was Volta born?']

	dict_records = readRecordDict(records_file)

	answer_list = []
	for q in questions:
		# print(q)
		answer = answer_question(dict_records, q)
		if answer is None:
			answer = 'No answer in this article.'
		# print(answer + '\n\n')
		print(answer[0].upper() + answer[1:])

