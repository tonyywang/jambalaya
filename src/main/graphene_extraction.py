#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Tony Wang April 2018

import requests
import sys
import time
import io
import unicodedata
from collections import defaultdict
from relationRecord import Record

### Graphene
def preprocessing(file):
    with io.open(file, 'r') as a:
        # list = []
        # for line in a:
        #     list.append(line)
        text = a.read()

    asciiOnly = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()

    data = asciiOnly.split('\n')
    # print(data)

    return data


def concat(data):
    paragraphs_only = []
    for section in data:
        if len(section) > 100:
            paragraphs_only.append(section)
    return "\n".join(paragraphs_only)
    # return paragraphs_only

def post(paragraphs_only):

    # article = []
    #
    # for i in range(len(paragraphs_only)):

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    r = requests.post('http://localhost:8080/relationExtraction/text', headers=headers, json={'text':paragraphs_only, 'doCoreference': 'true', 'isolateSentences': 'false'})
    # print(r.json())
    time.sleep(0.5)
    article = r.json()
    # article.append(paragraph)

    # return "\n".join(paragraphs_only)
    return article


def graphene(file):
    data = preprocessing(file)
    paragraphs_only = concat(data)
    article = post(paragraphs_only)
    return article

#     with io.open(output, 'w+', encoding='utf-8') as wf:
#         wf.write(article)
#
# def read(file):
#     # loadedText = json.load(file)
#
#     with open(file, 'r') as a:
#         text = a.read()
#
#     loadedText = json.loads(text)
#
#     return loadedText

### Process files into relation dictionary of simplified sentences.
### Output: {rel1: [sentence1, sentence2, ...], rel2: [sentence1, sentence2, ...], ...}

def extraction(text):

    extractions = text['extractions']

    allRecords = defaultdict(list)

    for i in range(0, len(extractions)):
        extraction = extractions[i]
        rel = extraction['relation']
        arg1 = extraction['arg1']
        arg2 = extraction['arg2']
        if not extraction['simpleContexts']:
            simpleContexts = ''
        else:
            simpleContexts = extraction['simpleContexts'][0]['text']

        record = Record(rel, arg1, arg2, simpleContexts)
        allRecords[rel].append(str(record))

    return allRecords


def readRecordDict(file):
    s = open(file, 'r', encoding='utf-8').read()
    my_dict = eval(s)

    allRecords = defaultdict(list)
    for rel, l in my_dict.items():
        for item in l:
            rel, arg1, arg2, arg3 = item.split(' ### ')
            allRecords[rel].append(Record(rel, arg1, arg2, arg3))
    return allRecords


def extractDictRecords(file):
    data = preprocessing(file)
    paragraphs_only = concat(data)
    article = post(paragraphs_only)
    allRecords = extraction(article)
    return allRecords

if __name__ == "__main__":
    file = sys.argv[1]
    data = preprocessing(file)
    paragraphs_only = concat(data)
    article = post(paragraphs_only)
    allRecords = extraction(article)
    print(dict(allRecords))