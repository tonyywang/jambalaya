#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import sys

def extra_train_data(text):
    # text = '../resources/train-v1.1.json'
    with open(text, 'r') as f:
        text = f.read()
        train = json.loads(text)

    questions = []
    data = train["data"]
    for i in range(len(data)):
        paragraphs = data[i]["paragraphs"]

        for j in range(len(paragraphs)):
            ans_ques = paragraphs[j]["qas"]
            for k in range(len(ans_ques)):
                q = ans_ques[k]["question"]
                questions.append(q)
    return questions

