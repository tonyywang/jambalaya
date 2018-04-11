#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import operator
import numpy as np
import math

def read_data(file):
    with open(file) as f:
        text = str.lower(f.read().strip())
    return text



def vocaulary_generate(text):
    vocaulary_count = {}
    sort_vocaulary = {}
    text = text.strip().split(' ')
    for word in text:
        if word in vocaulary_count:
            vocaulary_count[word] += 1
        else:
            vocaulary_count[word] = 1
    sort_vocaulary['UNKNOWNWORD'] = 0
    for word in vocaulary_count:
        if vocaulary_count[word] < 5:
            sort_vocaulary['UNKNOWNWORD'] += vocaulary_count[word]
        else:
            sort_vocaulary[word] = vocaulary_count[word]
    # sort_vocaulary = sorted(sort_vocaulary.items(), key=operator.itemgetter(1), reverse=True)
    new_text = []
    for word in text:
        if word in sort_vocaulary:
            new_text.append(word)
        else:
            new_text.append('UNKNOWNWORD')
    # sort_vocaulary = sorted(sort_vocaulary.items(), key=operator.itemgetter(1), reverse=True)
    return sort_vocaulary, new_text


def ngram_generate(text, n):
    ngram_dic = {}
    count = len(text) - n + 1
    space = ' '
    # combine every n word
    for i in range(count):
        new_ngram = space.join(text[i: (i + n)])
        if new_ngram in ngram_dic:
            ngram_dic[new_ngram] += 1
        else:
            ngram_dic[new_ngram] = 1
    for key in ngram_dic:
        ngram_dic[key] /= count
    # ngram_dic = sorted(ngram_dic.items(), key=operator.itemgetter(1), reverse=True)
    return ngram_dic, count


def compute_perplexity(test, dic, count1, lamb0, lamb1, lamb2, lamb3, unigram, bigram, trigram):
    test = test.strip().split(' ')
    new_test = []
    for word in test:
        if word in dic:
            new_test.append(word)
        else:
            new_test.append('UNKNOWNWORD')
    num = len(new_test)
    perplexity = 0
    space = ' '
    for i in range(num):
        if i >= 2:
            p0 = float(lamb0) / count1
            p1 = float(lamb1) * float(unigram[new_test[i]])
            uni = float(unigram.get(new_test[i - 1], '0'))
            bi = float(bigram.get(space.join(new_test[i-1:i+1]),'0'))
            tri = float(trigram.get(space.join(new_test[i-2:i+1]), '0'))
            if uni == 0:
                p2 = 0
            else:
                p2 = float(lamb2) * bi / uni
            if bi == 0:
                p3 = 0
            else:
                p3 = float(lamb3) * tri / bi

            prob = p0 + p1 + p2 + p3
            perplexity += np.log(prob)
    perplexity = math.exp( (-1.0/(num - 2)) * perplexity)
    return perplexity


# Main function
def test_score(test, train):
    train = read_data(train)
    # test = read_data(test)
    dic, new_text = vocaulary_generate(train)
    unigram, count1 = ngram_generate(new_text, 1)
    bigram, count2 = ngram_generate(new_text, 2)
    trigram, count3 = ngram_generate(new_text, 3)
    perplexity_dic = {}
    for q in test:
        perplex = compute_perplexity(q, dic, count1, 0.01, 0.1, 0.4, 0.49, unigram, bigram, trigram)
        perplexity_dic[q] = perplex
    return perplexity_dic


