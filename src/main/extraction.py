#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Tony Wang April 2018

import json
import sys
from collections import defaultdict
from relationRecord import Record

# output = article['sentences']

def read(file):
    # loadedText = json.load(file)

    with open(file, 'r') as a:
        text = a.read()

    loadedText = json.loads(text)

    return loadedText

def extraction(text):

    extractions = text['extractions']

    allTuples = defaultdict(list)
    allRecords = []

    for i in range(0, len(extractions)):
        extraction = extractions[i]
        rel = extraction['relation']
        arg1 = extraction['arg1']
        arg2 = extraction['arg2']
        if not extraction['simpleContexts']:
            simpleContexts = ''
        else:
            simpleContexts = extraction['simpleContexts'][0]['text']

        allTuples[rel].append((arg1, arg2, simpleContexts))
        allRecords.append(Record(rel, arg1, arg2, simpleContexts))

    return allTuples, allRecords

if __name__ == "__main__":
    file = sys.argv[1]
    text = read(file)
    allTuples, allRecords = extraction(text)
    print(dict(allTuples))