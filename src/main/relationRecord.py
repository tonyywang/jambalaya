#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Wei Wang
# Created: 4/17/2018


#curl -X POST -H "Content-Type: application/json"  -d '{"text":"Gemini is one of the constellations of the zodiac. It was one of the 48 constellations described by the 2nd century AD astronomer Ptolemy and it remains one of the 88 modern constellations today. Its name is Latin for twins, and it is associated with the twins Castor and Pollux in Greek mythology.", "doCoreference": "true", "isolateSentences": "false"}' -H "Accept: application/json" "http://localhost:8080/relationExtraction/text"

#curl -X POST -H "Content-Type: application/json"  -d '{"text": "Gemini is one of the constellations of the zodiac. It was one of the 48 constellations described by the 2nd century AD astronomer Ptolemy and it remains one of the 88 modern constellations today. Its name is Latin for twins, and it is associated with the twins Castor and Pollux in Greek mythology."}' -H "Accept: application/json" "http://localhost:8080/coreference/text"


#conda install -c asmeurer pattern
#from pattern.en import lemma
from nltk.stem import PorterStemmer
from rake_nltk import Rake
# Generate keywords for quetion
def keywords_generation(question):
	ps = PorterStemmer()
	r = Rake()
	r.extract_keywords_from_text(question.lower())
	phrases = r.get_ranked_phrases()
	keywords = set()
	for p in phrases:
		for w in p.split():
			keywords.add(ps.stem(w))
	return keywords


class Record:
	def __init__(self, r, a1, a2, a3):
		self.relation = r.strip()
		self.arg1 = a1.strip()
		self.arg2 = a2.strip()
		self.arg3 = a3[:-1].strip()

	def getArg123(self):
		return self.arg1 + ' ' + self.relation + ' ' + self.arg2 + ' '  + self.arg3 + '.'

	def getKeywords(self):
		sent = self.arg1 + ' ' + self.relation + ' ' + self.arg2 + ' '  + self.arg3 + '.'
		return sent, keywords_generation(sent)

	def findMissingArg(self, keywords):
		args = [self.arg1, self.arg2, self.arg3]
		missing_args = []
		for arg in args:
			if arg == '':
				continue
			if len(keywords.intersection(keywords_generation(arg))) == 0:
				missing_args.append(arg)
		return missing_args

	def isMissingArg2(self, keywords):
		if self.arg2 != '' and len(keywords.intersection(keywords_generation(self.arg2))) == 0:
			return self.arg2
		return None

	def print_record(self):
		print(self.relation, '( ', self.arg1, ', ', self.arg2, ', ', self.arg3, ' )')


	def __str__(self):
		l = [self.relation, self.arg1, self.arg2, self.arg3]
		return ' ### '.join(l)


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
