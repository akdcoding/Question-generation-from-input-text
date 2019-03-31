import requests
import json
import nltk
import spacy
nlp = spacy.load('en_core_web_sm')
from nltk.tag.stanford import CoreNLPPOSTagger
from nltk.stem.wordnet import WordNetLemmatizer


url = "http://localhost:9000/tregex"
request_params = {"pattern":  " RB=n1  > (ADVP >> (S=n2 > ROOT)) | > (ADJP >> (S=n2 > ROOT))"  }
text = "John is playing quietly."
print(text)
r = requests.post(url, data=text, params=request_params)
json_data = json.loads(r.text)
text1 = json_data['sentences'][0]['0']['match']
tree = nltk.Tree.fromstring(text1, read_leaf=lambda x: x.split("/")[0])
str1 = tree.leaves()
adverb = ' '.join(str1)

text_pos = CoreNLPPOSTagger(url='http://localhost:9000').tag(text.split())
#print(text_pos)
c = 0
for tagg in text_pos:
	if(c == 0 and tagg[1]!= "NNP" and tagg[0]!='I'):
		s=tagg[0].lower()
		text = text.replace(tagg[0], s)
	#line = 'He ran quickly.'	
	if tagg[1]== "VBD" and text_pos[c][0]!= 'had' and text_pos[c+1][1]!='VBG':
		verb_tense = "did"
		root_verb = WordNetLemmatizer().lemmatize(tagg[0],'v')
		text = text.replace(tagg[0],root_verb)

	#line = 'I run quickly.'
	if tagg[1]=="VBP" and text_pos[c][0]!= 'is' and text_pos[c][0]!='are' and text_pos[c][0]!= 'have':
		verb_tense = "do"
		root_verb = WordNetLemmatizer().lemmatize(tagg[0],'v')
		text = text.replace(tagg[0],root_verb)
	
	#line = 'John runs quickly.'
	if tagg[1]=="VBZ" and text_pos[c+1][1]!='VBN' and text_pos[c+1][1]!='VBG':
		verb_tense = "does"
		root_verb = WordNetLemmatizer().lemmatize(tagg[0],'v')
		text = text.replace(tagg[0],root_verb)

	#line = 'John is playing quietly.'
	#line = 'John was playing quietly.'
	#line = 'John is going to play quietly.'

	if tagg[1]=="VBG" and text_pos[c-1][1]!='VB' and text_pos[c-1][1]!='VBN':
		verb_tense = text_pos[c-1][0]
		text = text.replace(text_pos[c-1][0]+" ","")


	#line = 'John has ran quickly.'	
	if tagg[1]=="VBZ" and text_pos[c+1][1]=='VBN' and text_pos[c+2][1]!="VBG":
		verb_tense = text_pos[c][0]
		text = text.replace(text_pos[c][0]+" ","")

	#line = 'John will be playing quietly.'
	if tagg[1]=="VBG" and text_pos[c-1][1]=='VB':
		verb_tense = text_pos[c-2][0]
		text = text.replace(text_pos[c-2][0]+" ","")

	#line = 'John has been playing quietly.'
	#line = 'John had been playing quietly.'
	if (tagg[1]=="VBZ" or tagg[1]=="VBD") and text_pos[c+1][1]=='VBN' and text_pos[c+2][1]== 'VBG':
		verb_tense = text_pos[c][0]
		text = text.replace(text_pos[c][0]+" ","")

	#line = 'John had left quietly.'
	#line = 'We have eaten the meal quietly.'
	if tagg[1]=="VBN" and tagg[0]!='been' and (text_pos[c-1][0]== 'had' or text_pos[c-1][0]== 'have') and text_pos[c-2][1]!='MD':
		verb_tense = text_pos[c-1][0]
		text = text.replace(text_pos[c-1][0]+" ","")

	
	#line = 'John will run quickly.'
	#line = 'John would have ran quickly.'
	if tagg[1]=="MD" and text_pos[c+1][1]=='VB':
		verb_tense = text_pos[c][0]
		text = text.replace(text_pos[c][0]+" ","")
	c  = c + 1
"""
obj=""
for i in line:
	classified_text = st.tag(word_tokenize(i))
	if classified_text[0][1]!='PERSON':
		break
	obj = obj + classified_text[0][0]+ " "
"""
text = text.replace("."," ?")
text = text.replace(adverb,"")
Q = 'How '+verb_tense+' '+text
print(Q)

#java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000