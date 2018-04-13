#!/usr/bin/env python3

import random
import pcfg



def sort_by_score(questions_list, num_questions):
	train = './a1.txt'
	list = []
	for q in questions_list:
		if len(q) > 3:
			list.append(q)
	ques_list = pcfg.test_score(list, train)
	print(ques_list)
	sentences = sorted(ques_list, key = lambda  x : q_score(x)+ques_list[x])
	if len(sentences) > num_questions:
		return sentences[0 : num_questions]
	else:
		return sentences


# TARGET_LEN = 10
def q_score(q):
	#weight of length effect
	weight = 0.5
	total_score = abs(q.count(' ') - 10) * weight
	return total_score


def get_best_n(bin_list, wh_list, num_questions):
	best_list = []
	bin_num = num_questions//3
	wh_num = num_questions - bin_num
	bin_list = sort_by_score(bin_list, bin_num)
	wh_list = sort_by_score(wh_list, wh_num)
	for q in bin_list:
		best_list.append(q)
	for q in wh_list:
		best_list.append(q)
	random.shuffle(best_list)
	return best_list


