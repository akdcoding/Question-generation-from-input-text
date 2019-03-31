import requests
import json
import nltk
import spacy
nlp = spacy.load('en_core_web_sm')
from nltk.tag.stanford import CoreNLPPOSTagger

url = "http://localhost:9000/tregex"
request_params = {"pattern":  " SBAR|VP|NP=app $, /,/ "  }
#text = "Mexico City, the biggest city in the world, has many interesting archaeological sites."
text = "Hallway, the biggest room in the house, was empty."
print(text)
r = requests.post(url, data=text, params=request_params)
json_data = json.loads(r.text)
text1 = json_data['sentences'][0]['0']['match']
tree = nltk.Tree.fromstring(text1, read_leaf=lambda x: x.split("/")[0])
line = tree.leaves()

appos=''
begin_text=''
for tag in line:
     appos = appos + tag+' '

text = text.replace(',','')
result = text.index(appos)
text = text.replace(appos,'')
for x in range(0,result):
	begin_text = begin_text + text[x]


doc = nlp(begin_text)
for ent in doc.ents:
	sub_ent = ent.label_
if sub_ent == 'GPE' or sub_ent == 'LOC':
	text = text.replace(begin_text,'')
text1 = CoreNLPPOSTagger(url='http://localhost:9000').tag(text.split())

for tagg in text1:
	#line = 'She ate the fruits.'	
	if tagg[1]== "VBD" :
		tense = "was"

	#line = 'We eat the fruits.'
	if tagg[1]=="VBP" :
		tense = "is"
	
	#line = 'She eats the fruits.'
	if tagg[1]=="VBZ":
		tense = "is"

qts = "Which/Where"
qts = qts+' '+tense+' '+appos+'?'
print(qts)
