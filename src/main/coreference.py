import requests
import sys
import time
import io
import unicodedata

# curl -X POST \
#  -H "Content-Type: application/json" \
#  -H "Accept: application/json" \
#  -d '{"text": "Donald Trump is the president of USA. He is a business man."}' \
#  "http://localhost:5128/resolve/text"

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

data = {
    "doCoreference": "true", "isolateSentences": "false",
}

# text = "Donald Trump is the president of USA. He is a business man."

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

def post(headers, paragraphs_only):
    r = requests.post('http://localhost:8080/relationExtraction/text', headers=headers, json={"text":paragraphs_only})
    # print(r.json())
    time.sleep(0.5)
    article = r.json()
    return article


def coreference(file, output):
    data = preprocessing(file)
    paragraphs_only = concat(data)
    article = post(headers, paragraphs_only)
    with io.open(output, 'w+', encoding='utf-8') as wf:
        wf.write(article)


if __name__ == "__main__":
    file = sys.argv[1]
    data = preprocessing(file)
    paragraphs_only = concat(data)
    article = post(headers, paragraphs_only)
    print(article)
