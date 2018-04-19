#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Wei Wang
# Created: 4/17/2018

from enum import Enum

class WHType(Enum):
	WHO = 'who'
	WHOSE = 'whose'
	WHOM = 'whom'
	WHAT = 'what'
	WHERE = 'where'
	WHEN = 'when'
	WHICH = 'which'
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
def detect_type(question):
	question = question.lower()
	for w_type in WHType:
		if question.startswith(w_type.value):
			return w_type

	for b_type in BINType:
		if question.startswith(b_type.value):
			return b_type

	return 'Unknown question type'