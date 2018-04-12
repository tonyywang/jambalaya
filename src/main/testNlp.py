# from stanfordcorenlp import StanfordCoreNLP
#
# nlp = StanfordCoreNLP(r'../lib/stanford-corenlp-full-2018-02-27')
#
# sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
# print('Tokenize:' + nlp.word_tokenize(sentence))
# print('Part of Speech:'+ nlp.pos_tag(sentence))
# print('Named Entities:'+ nlp.ner(sentence))
# print('Constituency Parsing:'+ nlp.parse(sentence))
# print('Dependency Parsing:'+ nlp.dependency_parse(sentence))
#
# nlp.close()

# from pycorenlp import StanfordCoreNLP

# nlp = StanfordCoreNLP('http://nlp01.lti.cs.cmu.edu:9000')
# text = (
#   'Pusheen and Smitha walked along the beach. '
#   'Pusheen wanted to surf, but fell off the surfboard.')
# output = nlp.annotate(text, properties={
#   'annotators': 'tokenize,ssplit,pos,depparse,parse',
#   'outputFormat': 'json'
#   })
#
# print("")
# print(output['sentences'][0]['parse'])

# sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
# print('Tokenize:' + nlp.word_tokenize(sentence))
# print('Part of Speech:'+ nlp.pos_tag(sentence))
# print('Named Entities:'+ nlp.ner(sentence))
# print('Constituency Parsing:'+ nlp.parse(sentence))
# print('Dependency Parsing:'+ nlp.dependency_parse(sentence))
#
# nlp.close()


#
# from nltk.parse.corenlp import CoreNLPParser

# parser = CoreNLPParser(url='http://nlp01.lti.cs.cmu.edu:9000')

# from nltk.tag.stanford import CoreNLPNERTagger
# tagger = CoreNLPNERTagger(url='http://nlp01.lti.cs.cmu.edu:9000')
# print(tagger.tag(['John', 'Adams', 'went', 'to', 'New', 'York']))



nlp = StanfordCoreNLP('http://nlp01.lti.cs.cmu.edu:9000')

props = {'annotators': 'coref', 'pipelineLanguage': 'en'}

text = 'Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008.'
result = json.loads(nlp.annotate(text, properties=props))

num, mentions = result['corefs'].items()[0]
for mention in mentions:
    print(mention)



# from nltk.parse.corenlp import CoreNLPDependencyParser
# dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
parse, = dep_parser.raw_parse(
	'The quick brown fox jumps over the lazy dog.'
	)
print(parse.to_conll(4))
print(parse.tree())