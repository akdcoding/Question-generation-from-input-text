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
request_params = {"pattern":  " NP=n1 !>> NP >> (VP > (S=n2 > ROOT)) "  }
text = "John would have loved Anne."
r = requests.post(url, data=text, params=request_params)
json_data = json.loads(r.text)
text1 = json_data['sentences'][0]['0']['match']
tree = nltk.Tree.fromstring(text1, read_leaf=lambda x: x.split("/")[0])
line = tree.leaves()
#print(line)
text_pos = pos_tagger.tag(word_tokenize(text))
print(text_pos)
c = 0
for tagg in text_pos:
	#line = 'John loved Anne.'	
	if tagg[1]== "VBD" and text_pos[c][0]!= 'had' and text_pos[c+1][1]!='VBG':
		verb_tense = "did"
		root_verb = WordNetLemmatizer().lemmatize(tagg[0],'v')
		text = text.replace(tagg[0],root_verb)

	#line = 'John love Anne.'
	if tagg[1]=="VBP" and text_pos[c][0]!= 'is' and text_pos[c][0]!='are' and text_pos[c][0]!= 'have':
		verb_tense = "do"
		root_verb = WordNetLemmatizer().lemmatize(tagg[0],'v')
		text = text.replace(tagg[0],root_verb)
	
	#line = 'John loves Anne.'
	if tagg[1]=="VBZ" and text_pos[c+1][1]!='VBN' and text_pos[c+1][1]!='VBG':
		verb_tense = "does"
		root_verb = WordNetLemmatizer().lemmatize(tagg[0],'v')
		text = text.replace(tagg[0],root_verb)

	#line = 'John is playing with Anne'
			#who is john playig with?
	#line = 'John was playing with Anne.'
			#who was john playing with?
	#line = 'John is going to play with Anne.'
			#who is john going to play with?

	if tagg[1]=="VBG" and text_pos[c-1][1]!='VB' and text_pos[c-1][1]!='VBN':
		verb_tense = text_pos[c-1][0]
		text = text.replace(text_pos[c-1][0]+" ","")


	#line = 'John has loved Anne.'	
	if tagg[1]=="VBZ" and text_pos[c+1][1]=='VBN' and text_pos[c+2][1]!="VBG":
		verb_tense = text_pos[c][0]
		text = text.replace(text_pos[c][0]+" ","")

	#line = 'John will be playing with Anne.'
	if tagg[1]=="VBG" and text_pos[c-1][1]=='VB':
		verb_tense = text_pos[c-2][0]
		text = text.replace(text_pos[c-2][0]+" ","")

	#line = 'John has been playing with Anne.'
	#line = 'John had been playing with Anne.'
	if (tagg[1]=="VBZ" or tagg[1]=="VBD") and text_pos[c+1][1]=='VBN' and text_pos[c+2][1]== 'VBG':
		verb_tense = text_pos[c][0]
		text = text.replace(text_pos[c][0]+" ","")

	#line = 'John had loved Anne.'
	#line = 'We have loved Anne.'
	if tagg[1]=="VBN" and tagg[0]!='been' and (text_pos[c-1][0]== 'had' or text_pos[c-1][0]== 'have') and text_pos[c-2][1]!='MD':
		verb_tense = text_pos[c-1][0]
		text = text.replace(text_pos[c-1][0]+" ","")

	#line = 'John will have played with Anne.'
	#line = 'John will love Anne.'
	#line = 'John would have loved Anne.'
	if tagg[1]=="MD" and text_pos[c+1][1]=='VB':
		verb_tense = text_pos[c][0]
		text = text.replace(text_pos[c][0]+" ","")
	c  = c + 1

obj=""
for i in line:
	classified_text = st.tag(word_tokenize(i))
	if classified_text[0][1]!='PERSON':
		break
	obj = obj + classified_text[0][0]+ " "

text = text.replace("."," ?")
text = text.replace(obj,"")
Q = 'Who '+verb_tense+' '+text
print(Q)