#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Wei Wang
# Created: 4/21/2018

from spacy.symbols import nsubj, VERB
import spacy
# python -m spacy download en
# nlp = spacy.load('en')
import sys
import io
import rank
import extract_json
import generate_hmm

from questionTypes import BINType
from questionTypes import WHType
from relationRecord import Record

from graphene_extraction import readRecordDict

# python -m spacy download en_core_web_lg
#nlp = spacy.load('en_core_web_lg')
nlp = spacy.load('en')

def findSub(sent):
	for chunk in sent.noun_chunks:
		if chunk.root.dep_ == 'nsubj':
			return chunk.root.text
	return None


# he travelled Pitt -> Pitt dobj
def findDobj(sent):
	for chunk in sent.noun_chunks:
		if chunk.root.dep_ == 'dobj':
			return chunk.root.text
	return None




def read_data(filename):
	sentences = []
	with io.open(filename, 'r', encoding='utf-8') as f:
		for line in f:
			sents = line.strip().split('.')
			for sent in sents:
				sentences.append(sent)
	return sentences


def write_file(filename, sent_list):
	with io.open(filename, 'w', encoding='utf-8') as wf:
		for sent in sent_list:
			wf.write(sent + '\r\n')
	# wf.write(unicode(sent +'\r\n'))


# If the verb in a sentence is a Modal Verb or Auxiliary Verb.
def getAux(verb):
	verb = verb.lower()
	for b_type in BINType:
		if verb == b_type.value:
			return b_type.value
	return None


# aux, verb_lemma
# did, give
def dealVerbTense(relation):
	doc = nlp(relation)
	# only one sent.
	for sent in doc.sents:
		root_loc = sent.root.i
		root_token = doc[root_loc]

		if root_token.tag_ == 'VBZ':
			return 'does', root_token.lemma_
		elif root_token.tag_ == 'VBP':
			return 'do', root_token.lemma_
		elif root_token.tag_ == 'VBD':
			return 'did', root_token.lemma_
		elif root_token.tag_ == 'VBN':
			aux_loc = -1
			for left in root_token.lefts:
				# print(left.text, left.dep_)
				if left.dep_ == 'aux':  # has
					aux_loc = left.i
					return doc[aux_loc].text, doc[aux_loc + 1:].text_with_ws  # has   watched
			return 'did', root_token.lemma_
		elif root_token.tag_ == 'VBG':
			aux_loc = -1
			for left in root_token.lefts:
				if left.dep_ == 'aux':  # had
					aux_loc = left.i
					return doc[aux_loc].text, doc[aux_loc + 1:].text_with_ws  # had  been watching
			return 'did', root_token.lemma_
		elif root_token.tag_ == 'VB':
			aux_loc = -1
			for left in root_token.lefts:
				if left.dep_ == 'aux':  # will
					aux_loc = left.i
					return doc[aux_loc].text, root_token.lemma_  # will  clam
			return 'does', root_token.lemma_
		else:
			return 'does', root_token.lemma_
	return None, None

# He is a boy --> is    he    a boy?
def genAuxQuestion(b_type, listRecords):
	q_list = []
	for record in listRecords:
		q_list.append(b_type + ' ' + record.arg1 + '?')  # is he?
		if record.arg2 != '':
			q_list.append(b_type + ' ' + record.arg1 + ' ' + record.arg2 + '?')  # is he a boy?

			context, ner, _ = dealArg(record.arg2)
			if ner in ['DATE']:
				q_list.append(WHType.WHEN.value + ' ' + b_type + ' ' + record.arg1 + '?')
			else:
				q_list.append(WHType.WHAT.value + ' ' + b_type + ' ' + record.arg1 + '?')

		if record.arg3 != '':
			q_list.append(b_type + ' ' + record.arg1 + ' ' + record.arg2 + ' ' + record.arg3 + '?')

			loc, ner, _ = dealArg(record.arg3)  # He was born at Woolsthorpe Manor. --arg2='', arg3 = 'at Woolsthorpe Manor'
			if ner in ['LOC']:
				q_list.append(WHType.WHERE.value + ' ' + b_type + ' ' + record.arg1 + '?')
			else:
				q_list.append(WHType.WHAT.value + ' ' + b_type + ' ' + record.arg1 + '?')


	if len(q_list) == 0:
		return None

	# wh_list = []
	# for w_type in WHType:
	# 	for q in q_list:
	# 		wh_list.append(w_type.value + ' ' + q)
	#
	# q_list.extend(wh_list)
	return q_list



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


# had been watching  ( he, TV)    --> aux_verb = had, verb = been watching
def genRealVerbQuestion(relation, listRecords):
	q_list = []
	aux_verb, verb = dealVerbTense(relation)
	if aux_verb is None or verb is None:
		print(relation)
		return q_list

	for record in listRecords:
		q_list.append(aux_verb + ' ' + record.arg1 + ' ' + verb + '?')
		if record.arg2 != '':
			q_list.append(aux_verb + ' ' + record.arg1 + ' ' + verb + ' ' + record.arg2 + '?')

			context, ner, _ = dealArg(record.arg2)
			if ner in ['DATE']:
				q_list.append(WHType.WHEN.value + ' ' + aux_verb + ' ' + record.arg1 + ' ' + verb + '?')
			else:
				q_list.append(WHType.WHAT.value + ' ' + aux_verb + ' ' + record.arg1 + ' ' + verb + '?')

		if record.arg3 != '':
			q_list.append(aux_verb + ' ' + record.arg1 + ' ' + verb + ' ' + record.arg2 + ' ' + record.arg3 + '?')

			loc, ner, _ = dealArg(record.arg3)  # He was born at Woolsthorpe Manor. --arg2='', arg3 = 'at Woolsthorpe Manor'
			if ner in ['LOC']:
				q_list.append(WHType.WHERE.value + ' ' + aux_verb + ' ' + record.arg1 + ' ' + verb + '?')
			else:
				q_list.append(WHType.WHAT.value + ' ' + aux_verb + ' ' + record.arg1 + ' ' + verb + '?')
	if len(q_list) == 0:
		return None


	# wh_list = []
	# for w_type in WHType:
	# 	for q in q_list:
	# 		wh_list.append(w_type.value + ' ' + q)
	# q_list.extend(wh_list)
	return q_list



# replace the subject with wh-words
def askSub(listRecords):
	wh_list = []
	for record in listRecords:
		q_list = []
		q_list.append(record.relation + '?')
		if record.arg2 != '':
			q_list.append(record.relation + ' ' + record.arg2 + '?')
		if record.arg3 != '':
			q_list.append(record.relation + ' ' + record.arg2 + ' ' + record.arg3 + '?')
		if len(q_list) == 0:
			return None

		sub, ner, att = dealArg(record.arg1)
		if ner in ['PERSON']:
			if att is None:  # No attribute
				for q in q_list:
					wh_list.append(WHType.WHO.value + ' ' + q)
			else:
				for q in q_list:
					wh_list.append(WHType.WHOSE.value + ' ' + att + ' '+ q)
		elif ner in ['CARDINAL']:
			if att is not None:
				for q in q_list:
					wh_list.append(WHType.HOWMANY.value + ' ' + att + ' ' + q)
		else:#what
			for q in q_list:
				wh_list.append(WHType.WHAT.value + ' ' + q)

	return wh_list


def genQuestions(dict_records):
	q_list = []
	for rel, listRecords in dict_records.items():
		l = askSub(listRecords)
		if l is not None:
			q_list.extend(l)

		b_type = getAux(rel)
		if b_type is None:
			l = genRealVerbQuestion(rel, listRecords)
			if l is not None:
				q_list.extend(l)
		else:
			l = genAuxQuestion(b_type, listRecords)
			if l is not None:
				q_list.extend(l)

	return q_list




def test():

	listRecords = [Record('died', 'he', 'March 1727', 'on 31 .')]
	relation = 'died'

	b_type = getAux(relation)
	if b_type is None:
		print(genRealVerbQuestion(relation, listRecords))
	else:
		print(genAuxQuestion(b_type, listRecords))


	listRecords = [Record('had been watching', 'Tom', 'the ball', '')]
	relation = 'had been watching'
	print(askSub(listRecords))

	listRecords = [Record('watched', 'Tom', 'the ball', '')]
	relation = 'watched'
	print(askSub(listRecords))

	listRecords = [Record('is', "Tom's book", 'opening', '')]
	relation = 'is'
	print(askSub(listRecords))

	listRecords = [Record('attended', '3 people', 'the meeting', '')]
	relation = 'attended'
	print(askSub(listRecords))

	listRecords = [Record('are', 'a lot of chairs', 'in the room', '')]
	relation = 'are'
	print(askSub(listRecords))


	listRecords = [Record('was born', 'he', '', 'at Woolsthorpe Manor')]
	relation = 'was born'

	b_type = getAux(relation)
	if b_type is None:
		print(genRealVerbQuestion(relation, listRecords))
	else:
		print(genAuxQuestion(b_type, listRecords))


# test()



if __name__ == "__main__":
	records_file = '../resources/records.txt'
	#num_questions = int(sys.argv[2])
	num_questions = int('20')




	dict_records = readRecordDict(records_file)

	q_list = genQuestions(dict_records)

	for q in q_list:
		print(q)



#
# if __name__ == "__main__":
#
# 	text_file = sys.argv[1]
# 	num_questions = int(sys.argv[2])
# 	out_file = '../resources/questions.txt'
# 	extra_json = '../resources/train-v1.1.json'
#
# 	dict_records = extractDictRecords(text_file)
# 	q_list = genQuestions(dict_records)
#
# 	extra_train = extract_json.extra_train_data(extra_json)
# 	generate_hmm.get_hmm(text_file, extra_train)
# 	hmmfile = '../resources/my.hmm'
#
# 	sort_list = rank.get_best_q_n(q_list, num_questions, text_file, hmmfile)
# 	for s in sort_list:
# 		print(s)
# 	#write_file(out_file, sort_list)