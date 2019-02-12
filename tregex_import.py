import requests
import json
import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
# NER tagging prerequisites
classf=r'C:\Users\Akshada\Downloads\genquest-master\stanford-ner-2018-10-16\classifiers\english.all.3class.distsim.crf.ser.gz'
jar1=r'C:\Users\Akshada\Downloads\genquest-master\stanford-ner-2018-10-16\stanford-ner.jar'
st = StanfordNERTagger(classf,jar1,encoding='utf-8')

url = "http://localhost:9000/tregex"
#request_params = {"pattern":  " NP = n1 > (S = n2 > ROOT) & $++ VP = n3 "  }
request_params = {"pattern": "  NP=n1 !>> NP >> (VP > (S=n2 > ROOT)) "}
text = " Barack Obama is the president of America."
r = requests.post(url, data=text, params=request_params)
json_data = json.loads(r.text)
print(type(json_data))
print(json_data)
text = json_data['sentences'][0]['0']['match']
tree = nltk.Tree.fromstring(text, read_leaf=lambda x: x.split("/")[0])
print(tree.leaves())
line = tree.leaves()
# NER tagging
for i in line:
	classified_text = st.tag(word_tokenize(i))
	print("ENTITIES:",classified_text, '\n')
#type(json_data['sentences'][0]['0']['match'])