import requests
import json
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
# NER tagging prerequisites
classf=r'C:\Users\Akshada\Downloads\genquest-master\stanford-ner-2018-10-16\classifiers\english.all.3class.distsim.crf.ser.gz'
jar1=r'C:\Users\Akshada\Downloads\genquest-master\stanford-ner-2018-10-16\stanford-ner.jar'
st = StanfordNERTagger(classf,jar1,encoding='utf-8')

jar =  r'C:\Users\Akshada\Downloads\stanford-postagger-2018-10-16\stanford-postagger.jar'
model =  r'C:\Users\Akshada\Downloads\stanford-postagger-2018-10-16\models\english-left3words-distsim.tagger'
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')

url = "http://localhost:9000/tregex"
request_params = {"pattern":  " SBAR|VP|NP=app $, /,/ "  }
text = "Mexico City, the biggest city in the world, has many interesting archaeological sites."
print(text)
r = requests.post(url, data=text, params=request_params)
json_data = json.loads(r.text)
text1 = json_data['sentences'][0]['0']['match']
tree = nltk.Tree.fromstring(text1, read_leaf=lambda x: x.split("/")[0])
line = tree.leaves()
#print(line)
appos=''
begin_text=''
obj=''
for tag in line:
     appos = appos + tag+' '
#print(appos)
text = text.replace(',','')
result = text.index(appos)
text = text.replace(appos,'')
for x in range(0,result):
	begin_text = begin_text + text[x]
#print(begin_text)
text = text.replace(begin_text,'')
#print(text)
obj=""
for i in begin_text.split():
	classified_text = st.tag(word_tokenize(i))
	if classified_text[0][1]=='LOCATION':
		obj = obj + classified_text[0][0]+ " "

text1 = pos_tagger.tag(word_tokenize(text))
#print(text1)
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

