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


# context, NER, att
# Tom,  PERSON, book
# 3, CARDINAL, people
def dealArg(arg):
	if arg is None:
		return None, None, None
	doc = nlp(arg)
	# only one sent.
	for sent in doc.sents:
		root_loc = sent.root.i
		root_token = doc[root_loc]

		for ent in doc.ents:
			if root_token.text_with_ws not in ent.text:
				return ent.text, ent.label_, root_token.text_with_ws
			else:
				return ent.text, ent.label_, None  # No attribute
	return None, None, None


# # find an answer from sorted relevant_records
# def answerArg1(question_type, ranked_records):
# 	for record, sorce in ranked_records:
# 		if record.arg1 == '':
# 			continue
#
# 		sub, ner, att = dealArg(record.arg1)
# 		if question_type == WHType.WHO and ner in ['PERSON']:
# 			return sub
# 		elif question_type == WHType.WHOSE and ner in ['PERSON']:
# 			return sub
# 	return None



# def answerArg3(question_type, ranked_records):
# 	for record, score in ranked_records:
# 		if record.arg3 == '':
# 			continue
#
# 		context, ner, _ = dealArg(record.arg3)
# 		if question_type == WHType.WHERE and ner in ['LOC']:
# 			return context # or return arg3?
# 		elif question_type == WHType.WHEN and ner in ['DATE']:
# 			return context
# 		elif question_type == WHType.WHOM and ner in ['PERSON']: # Need to and this in questionGen
# 			return context
# 		elif question_type == WHType.HOW:
# 			return 'None.something'
# 		elif question_type == WHType.HOWLONG:
# 			return 'None.something'
# 		elif question_type == WHType.HOWOFTEN:
# 			return 'None.something'
# 	return None
#
# # return score, answer???
# def answerArg123(question_type, ranked_records):
#
# 	for record, score in ranked_records:
# 		args = []
# 		if record.arg1 != '':
# 			args.append(record.arg1)
# 		elif record.arg2 != '':
# 			args.append(record.arg2)
# 		elif record.arg3 != '':
# 			args.append(record.arg3)
# 		else:
# 			continue
#
# 		for arg in args:
# 			context, ner, att = dealArg(arg)
# 			if question_type == WHType.HOWMANY and ner in ['CARDINAL']:
# 				return context
# 			elif question_type == WHType.WHAT:
# 				return context  # or None.something
# 	return 'None.something'

def test():
	listRecords = [Record('had been watching', 'Tom', 'the ball', ''),
				   Record('watched', 'Tom', 'the ball', ''),
				   Record('is', "Tom's book", 'opening', ''),
				   Record('attended', '3 people', 'the meeting', ''),
				   Record('was born', 'he', '', 'at Woolsthorpe Manor'),
				   Record('died', 'he', 'March 1727', 'on 31 .')]
	print(answerArg1(WHType.WHO, listRecords))
	print(answerArg1(WHType.WHOSE, listRecords))
	print(answerArg1(WHType.HOWMANY, listRecords))
	print(answerArg3(WHType.WHERE, listRecords))
	print(answerArg3(WHType.WHEN, listRecords))



# def answerWH(question_type, ranked_records):
# 	if question_type in [WHType.WHO, WHType.WHOSE, WHType.HOWMANY]:
#
# 		return answerArg1(question_type, ranked_records)
# 	elif question_type in [WHType.WHERE, WHType.WHEN]:
# 		return answerArg3(question_type, ranked_records)
# 	elif question_type in [WHType.WHAT, WHType.HOWMANY]:
# 		return answerArg123(question_type, ranked_records)
# 	return None


def extract_answer_by_not(sent, not_list):
	for w in sent:
		if w in not_list:
			return ["No"]
	return ["Yes"]


def answerBIN(question_type, relevant_sents):
	not_list = []
	if question_type in [BINType.AM]:
		not_list = ["not"]
	elif question_type in [BINType.IS]:
		not_list = ["not", "isn't"]
	elif question_type in [BINType.ARE]:
		not_list = ["not", "aren't"]
	elif question_type in [BINType.WERE]:
		not_list = ["not", "weren't"]
	elif question_type in [BINType.HAD]:
		not_list = ["not", "hadn't"]
	elif question_type in [BINType.HAS]:
		not_list = ["not", "hasn't"]
	elif question_type in [BINType.HAVE]:
		not_list = ["not", "haven't"]
	elif question_type in [BINType.DO]:
		not_list = ["not", "don't"]
	elif question_type in [BINType.DID]:
		not_list = ["not", "didn't"]
	elif question_type in [BINType.WILL]:
		not_list = ["not", "won't"]
	elif question_type in [BINType.WOULD]:
		not_list = ["not", "wouldn't"]
	elif question_type in [BINType.CAN]:
		not_list = ["not", "cann't"]
	elif question_type in [BINType.COULD]:
		not_list = ["not", "couldn't"]

	# answers = []
	for sent in relevant_sents:
		answer = extract_answer_by_not(sent, not_list)
		# answers.append(answer)
	return answer



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
			context, ner, att = dealArg(arg)
			if question_type == WHType.WHO and ner in ['PERSON']:
				return context
			elif question_type == WHType.WHOSE and ner in ['PERSON']:
				return context
			elif question_type == WHType.WHERE and ner in ['LOC']:
				return context  # or return arg3?

			elif question_type == WHType.WHEN and ner in ['DATE']:
				return context
			elif question_type == WHType.WHOM and ner in ['PERSON']:  # Need to and this in questionGen
				return context
			elif question_type == WHType.HOW:
				return 'None.something'
			elif question_type == WHType.HOWLONG:
				return 'None.something'
			elif question_type == WHType.HOWOFTEN:
				return 'None.something'

			elif question_type == WHType.HOWMANY and ner in ['CARDINAL']:
				return context
			elif question_type == WHType.WHAT:
				return context  # or None.something
	return None

#'Who is the presentend?'
def answer_question(dict_records, question):
	keywords = keywords_generation(question)
	ranked_records = find_relevant_records(dict_records, keywords)
	for i in range(10):
		print(str(ranked_records[i][1]))
		ranked_records[i][0].print_record()

	question_type = detect_type(question)
	if isinstance(question_type, WHType):
		return answerWH(question_type, ranked_records, keywords)
	elif isinstance(question_type, BINType):
		return 'Yes.'
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
	# question_file = '../resources/question_Alessandro_Volta.txt'
	# questions = read_data(question_file)

	questions = ['When did Volta retire?',
				'Who did Alessandro Volta marry?',
				 # 'What did Alessandro Volta invent in 1800?',
				 'When did Alessandro Volta improve  and popularize the electrophorus?',
				 # 'How long was Alessandro Volta a professor at the University of Pavia?',
				 'Where was Volta born?']

	dict_records = readRecordDict(records_file)

	answer_list = []
	for q in questions:
		print(q)
		answer = answer_question(dict_records, q)
		if answer is None:
			answer = 'Woops, no answer.'
		print(answer)

