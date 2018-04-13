#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import math

def read_data(file):
    with open(file) as f:
        data = f.readlines()
    return data

def compare(target, candidate):
    size = len(target)
    err = 0
    for i in range(size):
        target_dic = {}
        candidate_dic = {}
        voc = set()
        sen_true = target[i].strip().split(' ')
        sen_candi = candidate[i].strip().split(' ')
        for j in range(len(sen_true)):
            if not sen_true[j] in target_dic:
                target_dic[sen_true[j]] = 1
                voc.add(sen_true[j])
            else:
                target_dic[sen_true[j]] += 1

            if j < len(sen_candi):
                if not sen_candi[j] in candidate_dic:
                    candidate_dic[sen_candi[j]] = 1
                    voc.add(sen_candi[j])
                else:
                    candidate_dic[sen_candi[j]] += 1
        sum = 0
        target_count = 0
        candidate_count = 0
        for tag in voc:
            if (tag in target_dic) and (tag in candidate_dic):
                sum += target_dic[tag] * candidate_dic[tag]
                target_count += target_dic[tag] * target_dic[tag]
                candidate_count += candidate_dic[tag] * candidate_dic[tag]
            elif tag in target_dic:
                target_count += target_dic[tag] * target_dic[tag]
            elif tag in candidate_dic:
                candidate_count += candidate_dic[tag] * candidate_dic[tag]
            else:
                pass
        err += float(sum) / (math.sqrt(target_count) * math.sqrt(candidate_count))

    err /= size
    return err


def main(target, candidate):
    target = read_data(target)
    candidate = read_data(candidate)
    err = compare(target, candidate)

if __name__ == "__main__":
    target = sys.argv[1]
    candidate = sys.argv[2]
    main(target, candidate)