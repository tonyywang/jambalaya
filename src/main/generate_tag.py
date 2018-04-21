#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import io
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import brown
from collections import Counter
import glob


def tag_file(filename):
    tag_list = []
    with io.open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            tagged = pos_tag(word_tokenize(line))
            temp = [x[1] for x in tagged]
            if len(temp) > 5:
                tag_list.append(temp)
    # print(tag_list)
    return tag_list


def write_file(filename, sent_list):
    with io.open(filename, 'w') as wf:
        for sent in sent_list:
            # wf.writelines(sent)
            wf.write(' '.join(sent) + '\n')


def generate_tag(file):
    # text_files = glob.glob(dir_name +'*.txt')
    out = '../resources/hmm.out'
    tag_list = tag_file(file)
    write_file(out, tag_list)


if __name__ == "__main__":
    generate_tag(sys.argv[1])
