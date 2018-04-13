#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Decide the named entity type(person, place) of the answer


from rake_nltk import Rake
import spacy
import collections
from enum import Enum

TOP_K = 10
class WHType(Enum):
	WHO = 'who'
	WHOSE = 'whose'
	WHOM = 'whom'
	WHAT = 'what'
	WHERE = 'where'
	WHEN = 'when'
#Binary type
class BINType(Enum):
	AM = 'am'
	IS = 'is'
	ARE = 'are'
	WAS = 'was'
	WERE = 'were'
	HAD = 'had'
	HAS = 'has'
	HAVE = 'have'
	DO = 'do'
	DID = 'did'
	WILL = 'will'
	WOULD = 'would'
	CAN = 'can'
	COULD = 'could'

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

# Parse sentence dependency parser
def extract_answer_by_NER(sentence, ner_list):
	nlp = spacy.load('en')
	doc = nlp(sentence)
	answers = set()
	for ent in doc.ents:
		if ent.label_ in ner_list:
			return ent.text
			#answers.add(ent.text)
	return None
	#return answers


def answerWH(question_type, relevant_sents):
	ner_list = []
	if question_type in [WHType.WHO, WHType.WHOSE, WHType.WHOM]:
		ner_list = ["PERSON"]
	elif question_type == WHType.WHERE:
		ner_list = ["LOC", "ORG"]
	elif question_type == WHType.WHEN:
		ner_list = ["DATE", "TIME"]
	elif question_type == WHType.WHICH:
		ner_list = ["ORG", "GPE", "LOC"]
	elif question_type == WHType.WHAT:
		ner_list = ["ORG", "PRODUCT"]

	answers = []
	for sent in relevant_sents:
		answer = extract_answer_by_NER(sent, ner_list)
		answers.append(answer)
	return answers

def answerBIN(relevant_sents):
	pass

#'Who is the presentend?'
def answer(question, article):
	keywords = keywords_generation(question)
	question_type = detect_type(question)

	relevant_sents = find_relevant_sentences(keywords, article)

	answers = []
	if isinstance(question_type, WHType):
		answers = answerWH(question_type, relevant_sents)
	elif isinstance(question_type, BINType):
		answerBIN(relevant_sents)
	return answers

if __name__ == "__main__":
	question = "Who is the presentend?"
	article = ["Donald Trump is the presentend."]

	print(question)
	print(answer(question, article))