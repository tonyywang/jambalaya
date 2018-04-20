#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Tony Wang April 2018
# Use Graphene to conduct open relation extraction

import requests
import json
import sys
import time
import io
import unicodedata

def preprocessing(file):
    with open(file, 'r') as a:
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


def post(paragraphs_only):

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    r = requests.post('http://localhost:8080/relationExtraction/text', headers=headers, json={'text':paragraphs_only, 'doCoreference': 'true', 'isolateSentences': 'false'})
    # print(r.json())
    time.sleep(0.5)
    article = r.json()
    return article


def coreference(file, output):
    data = preprocessing(file)
    paragraphs_only = concat(data)
    article = post(paragraphs_only)
    with io.open(output, 'w+', encoding='utf-8') as wf:
        wf.write(article)


if __name__ == "__main__":
    file = sys.argv[1]
    data = preprocessing(file)
    paragraphs_only = concat(data)
    article = post(paragraphs_only)
    print(json.dumps(article))
