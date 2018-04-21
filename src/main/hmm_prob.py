#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Jocelyn Huang
# 10/27/2017
# Viterbi in Python, ported pretty directly from Noah A. Smith's viterbi.pl.
# Not responsible for comment typos due to doing this late at night.

# Usage: ./hmm_prob.py my.hmm ptb.22.txt > my.out

# The following is an excerpt from his comments (go look at the original 
# if you want more detail):

# Runs the Viterbi algorithm (no tricks other than logmath!), given an
# HMM, on sentences, and outputs the best state path.

import collections
import math
import sys
import io
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import brown
from collections import Counter
import glob
import os

# hmmfile = sys.argv[1]
# txt = sys.argv[2]

init_state = "init"
final_state = "final"
oov_symbol = "OOV"

# A -> 2-layer hash for transition probabilities
A = collections.defaultdict(dict)
# B -> Emission probabilities
B = collections.defaultdict(dict)

States = set()
Voc = set()

# Read in the HMM and store probs as log probs
def read_hmm(hmmfile):
    with open(hmmfile, 'r') as f:
        for line in f:
            line = line.split()
            if line[0] == 'trans':
                # Read in states qq -> q, and transition prob
                qq,q,prob = line[1:4]
                # Add transition log prob and states seen
                A[qq][q] = math.log(float(prob))
                States.add(qq)
                States.add(q)
            # elif line[0] == 'emit':
            #     # Read in state q -> word w, and emission prob
            #     q,w,prob = line[1:4]
            #     # Add emission log prob and state/vocab seen
            #     B[q][w] = math.log(float(prob))
            #     States.add(q)
            #     Voc.add(w)
    return A, B, States, Voc


def tag_question(list):
    tag_list = []
    # with io.open(file, 'r', encoding='utf-8') as f:
    for line in list:
        tagged = pos_tag(word_tokenize(line))
        temp = [x[1] for x in tagged]
        tag_list.append(temp)
    # print(tag_list)
    return tag_list

def compute_prob(ques_tag, A):
    count = len(ques_tag) - 1
    prob = 0
    # combine every n tag
    for i in range(count):
        # new_ngram = space.join(ques_tag[i: (i + 2)])
        qq = ques_tag[i]
        q = ques_tag[i+1]
        if (qq in A) and (q in A[qq]):
            prob += A[qq][q]
    return prob

def compute_prob_list(tag_list, A):
    prob_list = []
    for q in tag_list:
        prob = compute_prob(q, A)
        prob_list.append(prob)
    return prob_list

def hmm_probility(hmmfile, questions):
    ques_tag = tag_question(questions)
    A, B, States, Voc = read_hmm(hmmfile)
    prob_list = compute_prob_list(ques_tag, A)
    ques_list = {}
    for i in range(len(questions)):
        ques_list[questions[i]] = prob_list[i]
    # print(prob_list)
    return ques_list

if __name__ == "__main__":
    hmmfile = '../resources/my.hmm'
    questions = '../resources/questions.txt'
    ques_tag = tag_question(questions)
    A, B, States, Voc = read_hmm(hmmfile)
    prob_list = compute_prob_list(ques_tag, A)
    print(prob_list)
