#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Tony Wang April 2018

import requests
import sys
import time
import io
import unicodedata
import re
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

def remove_text_inside_brackets(text, brackets="()[]"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    saved = ''.join(saved_chars)

    finalsaved = ""
    if "  " in saved:
        finalsaved = saved.replace("  ", " ")

    return finalsaved

def concat(data):
    paragraphs_only = []
    for section in data:
        new_section = remove_text_inside_brackets(section)
        if len(new_section) > 30:
            # nobrackets = re.sub("[\(\[].*?[\)\]]", "", section)
            paragraphs_only.append(new_section)
    return "\n".join(paragraphs_only)
    # return paragraphs_only

if __name__ == "__main__":
    file = sys.argv[1]
    data = preprocessing(file)
    paragraphs_only = concat(data)
    print(paragraphs_only)

def post(paragraphs_only):

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