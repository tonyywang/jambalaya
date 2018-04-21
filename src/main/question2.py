#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spacy.symbols import nsubj, VERB
import spacy
import sys
import io
import rank
import coreference
import generate_hmm

beVerbs = ['am', 'is', 'are', 'was', 'were']
# python -m spacy download en
nlp = spacy.load('en')
doc = nlp(u'San Fan is a city')



def findSub(sent):
	for chunk in sent.noun_chunks:
		if chunk.root.dep_ == 'nsubj':
			return chunk.root.text
	return ""

#he travelled Pitt -> Pitt dobj
def findDobj(sent):
	for chunk in sent.noun_chunks:
		if chunk.root.dep_ == 'dobj':
			return chunk.root.text
	return ""

def dealTense(sent):
	root_loc = sent.root.i
	root_token = doc[root_loc]
	q_str = []
	if root_token.tag_ == 'VBZ':
		q_str.append('does')
	elif root_token.tag_ == 'VBP':
		q_str.append('do')
	elif root_token.tag_ == 'VBD':
		q_str.append('did')
	elif root_token.tag_ == 'VBN':
		aux_loc = -1
		for left in root_token.lefts:
			# print(left.text, left.dep_)
			if left.dep_ == 'aux':  # has
				aux_loc = left.i
		if aux_loc == -1:
			return ""
		else:
			q_str.append(doc[aux_loc].text)
	else:
		return ""
	return " ".join(q_str)




# Pitt is a city. -> Is Pitt a city?
def genBeQ(sent):
	root_loc = sent.root.i
	root_token = doc[root_loc]
	q_str = []
	if root_token.pos_ == 'VERB' and root_token.text in beVerbs:
		left_span = doc[0: root_loc]
		right_span = doc[root_loc + 1: -1]
		q_str.append(root_token.text)
		q_str.append(left_span.text)
		q_str.append(right_span.text)
		q_str.append("?")
		return " ".join(q_str)
	return ""





#doc = nlp('He works well.') #Does he work well?
#doc = nlp('She had finished her work')
#doc = nlp('She has finished her work')
def genBinOtherQ(sent):
	root_loc = sent.root.i
	root_token = doc[root_loc]
	q_str = []

	q_str.append(dealTense(sent)) #does
	q_str.append(findSub(sent)) #he
	q_str.append(root_token.lemma_) #work

	right_span = doc[root_loc + 1: -1]
	q_str.append(right_span.text)
	q_str.append("?")
	return " ".join(q_str)


#doc = nlp('It was created by John.') #Was it created by Jnoh?
def genBePassiveQ(sent):
	root_loc = sent.root.i
	root_token = doc[root_loc]
	q_str = []
	aux_loc = -1
	subj_loc = -1
	#     print( root_token.text, root_token.tag_)
	#     for left in root_token.lefts:
	#         print(left.text, left.dep_)
	if (root_token.tag_ == 'VBN' or root_token.tag_ == 'VBD') and (root_token.text not in beVerbs):
		for left in root_token.lefts:
			# print(left.text, left.dep_)
			if left.dep_ == 'auxpass':  # was
				aux_loc = left.i
			elif left.dep_ == 'nsubjpass':  # it
				subj_loc = left.i

		if aux_loc >= 0 and subj_loc >= 0:
			q_str.append(doc[aux_loc].text)
			q_str.append(doc[subj_loc].text)
			q_str.append(doc[aux_loc + 1: -1].text)
			q_str.append("?")
			return " ".join(q_str)
	return ""


def genBinQuestions(sent):
	q_strs = []
	beQ = genBeQ(sent)
	binOtherQ = genBinOtherQ(sent)
	bePassiveQ = genBePassiveQ(sent)
	if beQ != "":
		q_strs.append(beQ)
	if binOtherQ != "":
		q_strs.append(binOtherQ)
	if bePassiveQ != "":
		q_strs.append(bePassiveQ)
	return q_strs




#doc = nlp("A constellation is a group.") # What is a constellation?
#doc = nlp("They are friends.") # What are they?
def genWhatIs(sent):
	root_loc = sent.root.i
	root_token = doc[root_loc]
	q_str = []
	if root_token.text in beVerbs and root_token.pos_ == 'VERB':
		for chunk in sent.noun_chunks:
			if chunk.root.dep_ == 'nsubj':
				q_str.append("What")
				q_str.append(root_token.text)
				q_str.append(chunk.text)
				q_str.append("?")
				return " ".join(q_str)
	return ""


#doc = nlp("He plays football.")  # What does he play?
#doc = nlp("They play football.")
#doc = nlp("He has finished his hw.") # What has he finished?
def genWhatDoes(sent):
	root_loc = sent.root.i
	root_token = doc[root_loc]
	q_str = []
	#print(root_token.pos_)
	if root_token.pos_ == 'VERB' and root_token.text not in beVerbs:
		q_str.append('What')
		q_str.append(dealTense(sent))

		for chunk in sent.noun_chunks:
			if chunk.root.dep_ == 'nsubj':
				q_str.append(chunk.text)
		#q_str.append(root_token.lemma_)
		q_str.append(root_token.text)
		q_str.append("?")
		return " ".join(q_str)
	return ""

#doc = nlp('John plays football.')
def genWho(sent):
	q_str = []
	for chunk in sent.noun_chunks:
		if chunk.root.dep_ == 'nsubj':
			for ent in sent.doc.ents:
				if ent.label_ == 'PERSON':
					#str_person = ent.text
					root_loc = sent.root.i
					q_str.append('Who')
					q_str.append(doc[root_loc:-1].text)
					q_str.append('?')
					return " ".join(q_str)
	return ""


#doc = nlp('San Fan is located in CA.') # Where is San Fan located in?
#doc = nlp('Apple is in San Francisco.')
#doc = nlp('He grew up in Pitt') # Where did he grow up?
#doc = nlp('He studies in Pitt')
#doc = nlp('He like running in the morning')
def genWhere(sent):
	q_str = []
	root_loc = sent.root.i
	root_token = doc[root_loc]
	for t in sent.subtree:
		if t.dep_ == 'prep':
			for ent in sent.doc.ents:
				# print(ent.text, ent.label_)
				if ent.label_ == 'LOC' or ent.label_ == 'GPE':
					q_str.append('Where')
					q_str.append(dealTense(sent)) #did
					q_str.append(findSub(sent)) #he
					q_str.append(root_token.lemma_) #grow
					q_str.append(findDobj(sent)) #up
					q_str.append("?")
					return " ".join(q_str)
	return ""


#doc = nlp("He travelled Pitt last year.") #When did he travel Pitt
#doc = nlp("He travelled Pitt on July.") #When did he travel Pitt
def genWhen(sent):
	q_str = []
	root_loc = sent.root.i
	root_token = doc[root_loc]
	for ent in sent.doc.ents:
		# print(ent.text, ent.label_)
		if ent.label_ == 'DATE' or ent.label_ == 'TIME':
			q_str.append('When')
			q_str.append(dealTense(sent)) #did
			q_str.append(findSub(sent)) #he
			q_str.append(root_token.lemma_) #travel
			q_str.append(findDobj(sent)) #Pitt
			q_str.append("?")
			return " ".join(q_str)
	return ""

def genWhQuestions(sent):
	q_str = []
	whatIs = genWhatIs(sent)
	whatDoes = genWhatDoes(sent)
	who = genWho(sent)
	where = genWhere(sent)
	when = genWhen(sent)
	if whatIs != "":
		q_str.append(whatIs)
	if whatDoes != "":
		q_str.append(whatDoes)
	if who != "":
		q_str.append(who)
	if where != "":
		q_str.append(where)
	if when != "":
		q_str.append(when)
	return q_str


def printInfo(s):
	for chunk in s.noun_chunks:
		print(chunk.text, chunk.root.dep_, chunk.root.text)

	print("root: ", s.root.text, s.root.tag_, s.root.i)

	print("Parser Tree:")
	for t in s.subtree:
		print(t.text, t.dep_, t.tag_, t.pos_)

	for ent in s.doc.ents:
		print(ent.text, ent.label_)


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
			#wf.write(unicode(sent +'\r\n'))

if __name__ == "__main__":

	text_file = sys.argv[1]
	num_questions = int(sys.argv[2])
	out_file = '../resources/questions.txt'
	#replaced_file = text_file + '.replaced'
	#coreference.coreference(text_file, replaced_file)
	replaced_file = text_file
	sentences = read_data(replaced_file)
	question_list = []
	bin_list = []
	wh_list = []
	# trim too-long sentences
	sentences = [s for s in sentences if s.count(' ') < 100 and s.count(' ') > 2]
	for line in sentences:
		doc = nlp(line)
		sents = list(doc.sents)
		for s in sents:
			for q in genBinQuestions(s):
				bin_list.append(q)
			for q in genWhQuestions(s):
				wh_list.append(q)
	print(len(question_list))
	# sort_list = sort_by_score(question_list, num_questions)
	generate_hmm.get_hmm(text_file)
	hmmfile = '../resources/my.hmm'
	sort_list = rank.get_best_n(bin_list, wh_list, num_questions, text_file, hmmfile)
	for s in sort_list:
		print(s)
	write_file(out_file, sort_list)


