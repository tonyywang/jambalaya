#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Wei Wang
# Created: 4/17/2018

import spacy
import json
#curl -X POST -H "Content-Type: application/json"  -d '{"text":"Who gave the ball to Jim?", "doCoreference": "true", "isolateSentences": "false"}' -H "Accept: application/json" "http://localhost:8080/relationExtraction/text"



class Record:
	def __init__(self, r, a1, a2, a3):
		self.relation = r.lower()
		self.arg1 = a1.lower()
		self.arg2 = a2.lower()
		self.arg3 = a3.lower()

		self.sentence = self.arg2 + self.arg1 + self.arg3

		self.tokens = set()
		nlp = spacy.load('en')
		doc = nlp(self.sentence)
		for token in doc:
			self.tokens.add(str(token))


	def print_record(self):
		print(self.relation, '( ', self.arg1, ', ', self.arg2, ', ', self.arg3, ' )')

	# only for Who
	def match_keywords(self, keywords):
		matched_words = set(filter(set(keywords).__contains__, self.tokens))

		if len(matched_words) == 0:
			return None

		arg1 = set(self.arg1)
		if not arg1.intersection(keywords):
			return self.arg1
		if not arg2.intersection(keywords):
			return self.arg2
		if not arg3.intersection(keywords):
			return self.arg3

		return None


def mytest():
	rels = '{"coreferenced":true,"sentences":[{"originalSentence":"It is a toy .","sentenceIdx":0,"extractions":[{"id":"3c0573f5a7fe44648782fbd7c3632020","type":"VERB_BASED","confidence":{"present":false},"sentenceIdx":0,"contextLayer":0,"relation":"is","arg1":"it","arg2":"a toy","linkedContexts":[],"simpleContexts":[]}]}],"extractions":[{"id":"3c0573f5a7fe44648782fbd7c3632020","type":"VERB_BASED","confidence":{"present":false},"sentenceIdx":0,"contextLayer":0,"relation":"is","arg1":"it","arg2":"a toy","linkedContexts":[],"simpleContexts":[]}]}'
	a = json.loads(rels)
	records = a["extractions"]
	for idx in range(0,len(records)):
		record = records[idx]
		r = record["relation"]
		arg1 = record["arg1"]
		arg2 = record["arg2"]
		context = record["simpleContexts"]
		Record(r, arg1, arg2, context).print_record()
