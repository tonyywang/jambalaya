from nltk.corpus import wordnet as wn
import json

file = "../resources/test.txt"

with open(file, 'r') as a:
    text = a.read()

stuff = json.loads(text)

extractions = stuff['extractions']

for i in range(0, len(extractions)):
    extraction = extractions[i]
    rel = extraction['relation']
    test = wn.synsets(rel, pos=wn.VERB)
    print(test)