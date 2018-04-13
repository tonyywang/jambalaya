import requests
import sys
import time

# curl -X POST \
#  -H "Content-Type: application/json" \
#  -H "Accept: application/json" \
#  -d '{"text": "Donald Trump is the president of USA. He is a business man."}' \
#  "http://localhost:5128/resolve/text"

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

# text = "Donald Trump is the president of USA. He is a business man."

def preprocessing(file):
    with open(file, 'r') as a:
        # list = []
        # for line in a:
        #     list.append(line)
        text = a.read()

    data = text.split('\n\n\n')

    # test = "\n".join(text.split('\n\n\n')[1:])

    return data

def concat(article):
    for section in data:
        if len(section) > 100:
            paragraphs_only = "\r\n".join([section for section in article])

    return paragraphs_only

def post(headers, paragraphs_only):
    r = requests.post('http://localhost:8080/coreference/text', headers=headers, json={"text":section})
    # print(r.text)
    time.sleep(0.5)
    article = r.json()['substitutedText']

    return article

if __name__ == "__main__":
    file = sys.argv[1]
    data = preprocessing(file)
    paragraphs_only = concat(data)
    article = post(headers, paragraphs_only)
    print(article)

def coreference(file, output):
    data = preprocessing(file)
    paragraphs_only = concat(data)
    article = post(headers, paragraphs_only)
    print(article)
    with io.open(output, 'w+', encoding='utf-8') as wf:
        wf.write(unicode(article))

