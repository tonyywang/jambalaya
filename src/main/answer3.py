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
from graphene_extraction import readRecordDict

TOP_K = 10

# python -m spacy download en_core_web_lg
# nlp = spacy.load('en_core_web_lg')
nlp = spacy.load('en')


def read_data(file):
    with open(file) as f:
        data = f.readlines()
    return data

# isinstance(obj, WHType)
def detect_type(sentence):
	sentence = sentence.lower()
	for w_type in WHType:
		if sentence.startswith(w_type.value):
			return w_type

	for b_type in BINType:
		if sentence.startswith(b_type.value):
			return b_type

	return 'Unknown answer type'



# Generate keywords for quetion
def keywords_generation(question):
	r = Rake()
	r.extract_keywords_from_text(question)
	keywords = r.get_ranked_phrases()
	return keywords

print(keywords_generation('Volta was not born in Como.'))

# topK Most Relevant Sentences
def find_relevant_sentences(keywords, article):
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

def find_answer(keywords, article):
	article_dict = collections.Counter()
	for sentence in article:
		tokens = keywords_generation(sentence)
		matched_words = set(filter(set(keywords).__contains__, tokens))
		if (len(tokens) == 0):
			article_dict[sentence] = 0
		article_dict[sentence] = len(matched_words) / len(tokens)

	# relevant_sents = []
	# for (sentence, num_matchwords) in article_dict.most_common(TOP_K):
	# 	relevant_sents.append(sentence)
	#
	#
	# if article_dict.most_common(1)[0][1] < 0.1:
	# 	answer = None
	# answer = article_dict.most_common(1)[0][0]
	# return answer

# Parse sentence dependency parser
def extract_answer_by_NER(relevant_sents, ner_list):
	answers = []
	for sent in relevant_sents:
		doc = nlp(sent)
		# answer = set()
		for ent in doc.ents:
			if ent.label_ in ner_list:
				# answer.add(ent.text)
				answers.append(ent.text)
	return answers



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


# find an answer from sorted relevant_records
def answerArg1(question_type, ranked_records):
	for record in ranked_records:
		if record.arg1 == '':
			continue

		sub, ner, att = dealArg(record.arg1)
		if question_type == WHType.WHO and ner in ['PERSON']:
			return sub
		elif question_type == WHType.WHOSE and ner in ['PERSON']:
			return sub
	return None

def answerArg3(question_type, ranked_records):
	for record in ranked_records:
		if record.arg3 == '':
			continue

		context, ner, _ = dealArg(record.arg3)
		if question_type == WHType.WHERE and ner in ['LOC']:
			return context # or return arg3?
		elif question_type == WHType.WHEN and ner in ['DATE']:
			return context
		elif question_type == WHType.WHOM and ner in ['PERSON']: # Need to and this in questionGen
			return context
		elif question_type == WHType.HOW:
			return 'None.something'
		elif question_type == WHType.HOWLONG:
			return 'None.something'
		elif question_type == WHType.HOWOFTEN:
			return 'None.something'
	return None

# return score, answer???
def answerArg123(question_type, ranked_records):

	for record in ranked_records:
		args = []
		if record.arg1 != '':
			args.append(record.arg1)
		elif record.arg2 != '':
			args.append(record.arg2)
		elif record.arg3 != '':
			args.append(record.arg3)
		else:
			continue

		for arg in args:
			context, ner, att = dealArg(arg)
			if question_type == WHType.HOWMANY and ner in ['CARDINAL']:
				return context
			elif question_type == WHType.WHAT:
				return context  # or None.something
	return 'None.something'

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


def extract_dobj(relevant_sents):
	# He has finished his homework.
	answers = []
	for sent in relevant_sents:
		doc = nlp(sent)
		for doc_sen in doc.sents:
			for chunk in doc_sen.noun_chunks:
				if chunk.root.dep_ == 'dobj':
					answers.append(chunk.text)
	return answers

def answerWH(question_type, relevant_records):
	if question_type in [WHType.WHO, WHType.WHOSE, WHType.HOWMANY]:
		return answerArg1(question_type, relevant_records)
	elif question_type in [WHType.WHERE, WHType.WHEN]:
		return answerArg3(question_type, relevant_records)
	elif question_type in [WHType.WHAT, WHType.HOWMANY]:
		return answerArg123(question_type, relevant_records)
	return None


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
	relevant_records = []
	for rel, list_records in dict_records.items():
		for record in list_records:
			if len(set(keywords).intersection(set(record.getKeywords()))) != 0:
				relevant_records.append(record)
				record.print_record()
	return relevant_records


#'Who is the presentend?'
def answer_question(dict_records, question):
	keywords = keywords_generation(question)
	relevant_records = find_relevant_records(dict_records, keywords)
	question_type = detect_type(question)
	if isinstance(question_type, WHType):
		return answerWH(question_type, relevant_records)
	elif isinstance(question_type, BINType):
		return answerBIN(question_type, relevant_records)
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

	dict_records = readRecordDict(records_file)

	answer_list = []
	for q in questions:
		print(q)
		answer = answer_question(dict_records, q)
		if answer is None:
			answer = 'Woops, no answer.'
		print(answer)

