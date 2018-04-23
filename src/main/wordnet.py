from nltk.corpus import wordnet as wn
import json
import spacy
from relationRecord import Record

# from splitter.SentenceSplitter import *
# from splitter.Tokenizer import *
# from tag.PosTagger import *
# from tag.SST import *
#
# ssp = SentenceSplitter('en.ss').pipe('infile')
# tokp = Tokenizer('en.tok').pipe(ssp)
# posp = PosTagger('en.pos').pipe(tokp)
# sstp = SST('it.sst').pipe(posp)
#
# for tok in sstp:
#    print(tok)

for synset in wn.synsets('school.n.01'):
    print(synset.lexname())

# ### Wordnet
# file = "../resources/test.txt"
#
# with open(file, 'r') as a:
#     text = a.read()
#
# stuff = json.loads(text)
#
# extractions = stuff['extractions']
#
# for i in range(0, len(extractions)):
#     extraction = extractions[i]
#     rel = extraction['relation']
#     arg1 = extraction['arg1']
#     arg2 = extraction['arg2']
#     if not extraction['simpleContexts']:
#         simpleContexts = ''
#     else:
#         simpleContexts = extraction['simpleContexts'][0]['text']
#
#     record = Record(rel, arg1, arg2, simpleContexts)
#
#     # if arg2 != '':
#     #     print(arg2)
#     #     for synset in list(wn.all_synsets('n'))[:10]:
#     #         print(synset)
#
#     nlp = spacy.load('en')
#     doc = nlp(str(record))
#     for token in doc:
#         # print(token.text, token.tag_, token.dep_)
#         print(token.text, token.tag_)
#         if token.dep_ == 'dobj' and token.tag_ != 'NNP' and token.tag_ != '-PRON-':
#             print(wn.synset(token.lemma_ + '.n.01').lexname)
#             # for synset in list(wn.all_synsets('n'))[:3]:
#             #     print(token.text)
#             #     print(synset)
#
#         if token.dep_ == 'pobj' and token.tag_ != 'NNP' and token.tag_ != '-PRON-':
#             print(wn.synset(token.lemma_ + '.n.01').lexname)
#             # for synset in list(wn.all_synsets('n'))[:3]:
#             #     print(token.text)
#             #     print(synset)
