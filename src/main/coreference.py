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

def post(headers, data):
    article = []
    for section in data:
        if len(section) > 200:
            r = requests.post('http://localhost:5128/resolve/text', headers=headers, json={"text":section})
            # print(r.text)
            time.sleep(0.5)
            json_text = r.json()['text']
            article.append(json_text)
        else:
            article.append(section)

    return article

def concat(article):
    replace_article = "\n".join([section for section in article])
    return replace_article

if __name__ == "__main__":
    file = sys.argv[1]
    data = preprocessing(file)
    article = post(headers, data)
    replace_article = concat(article)
    print(replace_article)
