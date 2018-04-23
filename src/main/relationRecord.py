#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Wei Wang
# Created: 4/17/2018

import spacy
import json
#curl -X POST -H "Content-Type: application/json"  -d '{"text":"A lot of chairs are in the room.", "doCoreference": "true", "isolateSentences": "false"}' -H "Accept: application/json" "http://localhost:8080/relationExtraction/text"

# python -m spacy download en_core_web_lg
nlp = spacy.load('en_core_web_lg')

class Record:
	def __init__(self, r, a1, a2, a3):
		self.relation = r
		self.arg1 = a1
		self.arg2 = a2
		self.arg3 = a3[:-1]

		# self.sentences = []
		if self.arg2 == '':
			self.sentence = self.arg1 + ' ' + self.relation + '.'
		else:
			self.sentence = self.arg1 + ' ' + self.relation + ' ' + self.arg2 +  '.'
		if self.arg3 != '':
			self.sentence = self.arg1 + ' ' + self.relation + ' ' + self.arg2 + ' '  + self.arg3 + '.'

		# You can use the for loop to add similar relations and arg2s from WordNext.


		# self.tokens = set()
		# nlp = spacy.load('en')
		# doc = nlp(self.sentence)
		# for token in doc:
		# 	self.tokens.add(str(token))

	def print_record(self):
		# print(self.relation, '( ', self.arg1, ', ', self.arg2, ', ', self.arg3, ' )')
		# print('simplified sentences:')
		print(self.sentence)

	# sub, NER, att
	# Tom,  PERSON, book
	# 3, CARDINAL, people
	def dealArg1(self):
		doc = nlp(self.arg1)
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



	def __str__(self):
		return self.relation, '( ', self.arg1, ', ', self.arg2, ', ', self.arg3, ' )'
		#return self.sentence



# def mytest():
# 	rels = '{"coreferenced":true,"sentences":[{"originalSentence":"It is a toy .","sentenceIdx":0,"extractions":[{"id":"3c0573f5a7fe44648782fbd7c3632020","type":"VERB_BASED","confidence":{"present":false},"sentenceIdx":0,"contextLayer":0,"relation":"is","arg1":"it","arg2":"a toy","linkedContexts":[],"simpleContexts":[]}]}],"extractions":[{"id":"3c0573f5a7fe44648782fbd7c3632020","type":"VERB_BASED","confidence":{"present":false},"sentenceIdx":0,"contextLayer":0,"relation":"is","arg1":"it","arg2":"a toy","linkedContexts":[],"simpleContexts":[]}]}'
# 	a = json.loads(rels)
# 	records = a["extractions"]
# 	for idx in range(0,len(records)):
# 		record = records[idx]
# 		r = record["relation"]
# 		arg1 = record["arg1"]
# 		arg2 = record["arg2"]
# 		context = ''
# 		Record(r, arg1, arg2, context).print_record()
# mytest()
