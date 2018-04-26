#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pcfg
import hmm_prob
import similarity



def sort_by_score(questions_list, num_questions, hmmfile):
	# train = './a1.txt'
	list = []
	for q in questions_list:
		if len(q) > 3:
			list.append(q)
	# ques_list = pcfg.test_score(list, train)
	ques_list = hmm_prob.hmm_probility(hmmfile, list)
	for q in ques_list:
		ques_list[q] = q_score(q)-0.5* ques_list[q]
	sentences = sorted(ques_list, key = lambda  x : ques_list[x])
	i = 0
	while (i < len(sentences)-1):
		j = i+1
		while (similarity.compare(sentences[i], sentences[j]) > 0.7 and j < len(sentences)-1):
			ques_list[sentences[j]] = ques_list[sentences[j]] + 100
			j = j+1
		i = j
	sentences = sorted(ques_list, key=lambda x: ques_list[x])


	if len(sentences) > num_questions:
		return sentences[0 : num_questions]
	else:
		return sentences



# TARGET_LEN = 10
def q_score(q):
	#weight of length effect
	# weight = 1
	total_score = abs(q.count(' ') - 10)
	return total_score


def get_best_n(bin_list, wh_list, num_questions, hmmfile):
	best_list = []
	bin_num = num_questions//3
	wh_num = num_questions - bin_num
	bin_list = sort_by_score(bin_list, bin_num, hmmfile)
	wh_list = sort_by_score(wh_list, wh_num, hmmfile)
	for q in bin_list:
		best_list.append(q)
	for q in wh_list:
		best_list.append(q)
	random.shuffle(best_list)
	return best_list


def get_best_q_n(q_list, num_questions, hmmfile):
	best_list = sort_by_score(q_list, num_questions, hmmfile)
	#random.shuffle(best_list)
	return best_list