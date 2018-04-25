#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Wei Wang
# Created: 4/17/2018

from enum import Enum

class TAGList(Enum):
	WHO_TAGS = ['PERSON', 'noun.person', 'noun.group']
	# WHOSE_TAGS = ['PERSON', 'noun.person', 'noun.group']
	WHERE_TAGS = ['LOC', 'FACILITY', 'ORG', 'GPE', 'noun.location']
	WHEN_TAGS = ['DATE', 'TIME', 'noun.time']
	WHAT_TAGS = ['noun.act', 'noun.animal', 'noun.artifact', 'noun.attribute', 'noun.body', 'noun.cognition',
				 'noun.communication', 'noun.event', 'noun.feeling', 'noun.food', 'noun.motive', 'noun.object',
				 'noun.other', 'noun.phenomenon', 'noun.plant', 'noun.possession', 'noun.process',
				 'noun.relation', 'noun.shape', 'noun.state', 'noun.substance']
	HOWMANY_TAGS = ['CARDINAL', 'noun.quantity']
	HOWMUCH_TAGS = ['PERCENT', 'MONEY', 'QUANTITY']
	HOWLONG_TAGS = ['DATE', 'TIME']
	HOWOLD_TAGS = ['DATE']
	HOW_TAGS = ['npadvmod', 'advmod']
	HOWOFTEN_TAGS = []


class WHType(Enum):
	WHATTIME = 'what time'
	WHATYEAR = 'what year'
	WHATMONTH = 'what month'
	WHATDAY = 'what day'
	WHO = 'who'
	WHOSE = 'whose'
	WHOM = 'whom'
	WHAT = 'what'
	WHERE = 'where'
	WHEN = 'when'
	WHICH = 'which'
	WHY = 'why'
	HOWMANY = 'how many'
	HOWOLD = 'how old'
	HOWLONG = 'how long'
	HOWOFTEN = 'how often'
	HOWMUCH = 'how much'
	HOW = 'how'
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
	DOES = 'does'
	DID = 'did'
	WILL = 'will'
	WOULD = 'would'
	CAN = 'can'
	COULD = 'could'

# isinstance(obj, WHType)
def detect_type(question):
	question = question.lower()

	for b_type in BINType:
		if question.startswith(b_type.value):
			return b_type

	for w_type in WHType:
		# if question.startswith(w_type.value):
		# 	return w_type
		if w_type.value in question:
			return w_type

	return 'Unknown question type'

# # check for lexical category; might be slow needs testing
# def checkCategory(text):
# 	for synset in wn.synsets(text):
# 		if synset.lexname == noun.location:
# 			return WHType.WHERE
# 		if synset.lexname == noun.time:
# 			return WHType.WHEN
# 		# if synset.lexname == noun.quantity:
# 		# 	return WHType.HOWMUCH?
# 		else:
# 			sysnet.lexname == noun.location:
# 			return WHTYPE.WHAT