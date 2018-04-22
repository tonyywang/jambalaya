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

TOP_K = 10

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

	if article_dict.most_common(1)[0][1] < 0.1:
		answer = None
	answer = article_dict.most_common(1)[0][0]
	return answer

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


# find an answer from sorted relevant_records
def answerSub(question_type, relevant_records):
	for record in relevant_records:
		sub, ner, att = record.dealArg1()
		if question_type == WHType.WHO and ner in ['PERSON']:
			return sub
		elif question_type == WHType.WHOSE and ner in ['PERSON']:
			return sub
		elif question_type == WHType.HOWMANY and ner in ['CARDINAL']:
			return sub
		elif question_type == WHType.WHAT:
			return sub
	return None

def test():
	listRecords = [Record('had been watching', 'Tom', 'the ball', ''),
				   Record('watched', 'Tom', 'the ball', ''),
				   Record('is', "Tom's book", 'opening', ''),
				   Record('attended', '3 people', 'the meeting', '')]
	print(answerSub(WHType.WHO, listRecords))
	print(answerSub(WHType.WHOSE, listRecords))
	print(answerSub(WHType.HOWMANY, listRecords))
test()

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

def answerWH(question_type, relevant_sents):
	answers = []
	if question_type == WHType.WHAT:
		answers = extract_dobj(relevant_sents)
		return answers

	ner_list = []
	if question_type in [WHType.WHO, WHType.WHOSE, WHType.WHOM]:
		ner_list = ["PERSON"]
	elif question_type == WHType.WHERE:
		ner_list = ["LOC", "ORG", "GPE"]
	elif question_type == WHType.WHEN:
		ner_list = ["DATE", "TIME"]
	elif question_type == WHType.WHERE:
		ner_list = ["ORG", "GPE", "LOC"]



	# for sent in relevant_sents:
	# 	answer = extract_answer_by_NER(sent, ner_list)
	# 	answers.append(answer)
	answers = extract_answer_by_NER(relevant_sents, ner_list)
	return answers


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

#'Who is the presentend?'
def answer_question(article, question):
	keywords = keywords_generation(question)
	question_type = detect_type(question)

	relevant_sents = find_relevant_sentences(keywords, article)

	answer = None
	if isinstance(question_type, WHType):
		answer = find_answer(keywords,article)
		#answers = answerWH(question_type, relevant_sents)
	elif isinstance(question_type, BINType):
		answer = answerBIN(question_type, relevant_sents)
	return answer


def write_file(filename, sent_list):
	with open(filename, 'w') as f:
		for sent in sent_list:
			f.write(sent[0] + '\n')
			# f.write('\n'.join(sent)+'\r\n')


def main(input_file_article, question):
	#replaced_file = input_file_article + '.replaced'
	#coreference.coreference(input_file_article, replaced_file)
	replaced_file = input_file_article
	question = read_data(question)
	article = read_data(replaced_file)

	answer_list = []
	out_file = '../resources/answers.txt'

	for q in question:
		print(q)
		answer = answer_question(article, q)
		# if len(answer) == 0:
		if answer is None:
			answer = ["Woops, no answer."]
		print(answer)
		answer_list.append(answer)
	write_file(out_file, answer_list)


# if __name__ == "__main__":
# 	article = sys.argv[1]
# 	question = sys.argv[2]
# 	main(article, question)