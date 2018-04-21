#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import io
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import brown
from collections import Counter
import glob
import os

def read_data(filename):
    sentences = []
    with io.open(filename, 'r') as f:
        for line in f:
            # sents = line.strip().split('.')
            sents = line.strip()
            # for sent in sents:
            if (sents.count(' ') > 4):
                sentences.append(sents)
                # print(sents)
    return sentences

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


def write_list(filename, sent_list):
    with io.open(filename, 'w') as wf:
        for sent in sent_list:
            # wf.writelines(sent)
            wf.write(' '.join(sent) + '\n')

def write_txt(filename, sent_list):
    with io.open(filename, 'w') as wf:
        for sent in sent_list:
            # wf.writelines(sent)
            wf.write(sent + '\n')



def generate_tag(file):
    # text_files = glob.glob(dir_name +'*.txt')
    out = '../resources/train.tgs'
    tag_list = tag_file(file)
    write_list(out, tag_list)



def get_hmm(txt, extra):
    # txt = '../resources/a1.txt'
    txt_list = read_data(txt)
    # print(txt_list)
    revise_txt = '../resources/train_revise.txt'
    write_txt(revise_txt, txt_list)
    write_txt(revise_txt, extra)
    generate_tag(txt)
    command = './train_hmm.pl ../resources/train.tgs ../resources/train_revise.txt > ../resources/my.hmm'
    os.system(command)


if __name__ == "__main__":
    txt = '../resources/a1.txt'
    txt_list = read_data(txt)
    # print(txt_list)
    revise_txt = '../resources/train_revise.txt'
    write_txt(revise_txt, txt_list)
    generate_tag(sys.argv[1])
    command = './train_hmm.pl ../resources/train.tgs ../resources/train_revise.txt > ../resources/my.hmm'
    os.system(command)
