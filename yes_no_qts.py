from textblob import Word
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk import sent_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
from nltk import word_tokenize
from nltk.tokenize import word_tokenize

# POS tagging prerequisites
jar =  r'C:\Users\Akshada\Downloads\stanford-postagger-2018-10-16\stanford-postagger.jar'
model =  r'C:\Users\Akshada\Downloads\stanford-postagger-2018-10-16\models\english-left3words-distsim.tagger'
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')
line = 'She has eaten the fruits.'
text = pos_tagger.tag(word_tokenize(line))
print(text)
c = 0
s = ['null']
q = ''
for tagg in text:
	s.append(tagg[0])
	if(c == 0 and tagg[1]!= "NNP"):
		s[1]=s[1].lower()
	
	#line = 'She ate the fruits.'	
	if tagg[1]== "VBD" and text[c][0]!= 'had':
		s[0] = "Did"
		s[c+1] = WordNetLemmatizer().lemmatize(tagg[0],'v')

	#line = 'We eat the fruits.'
	if tagg[1]=="VBP" and text[c][0]!= 'is' and text[c][0]!='are' and text[c][0]!= 'have':
		s[0] = "Do"
	
	#line = 'She eats the fruits.'
	if tagg[1]=="VBZ" and text[c+1][1]!='VBN':
		s[0] = "Does"
		s[c+1] = WordNetLemmatizer().lemmatize(tagg[0],'v')
	
	#line = 'She has eaten the fruits.'	
	if tagg[1]=="VBZ" and text[c+1][1]=='VBN' and text[c+2][1]!="VBG":
		s[0] = tagg[0].capitalize()
		s.pop(c+1)	
		#s[c+1] = tagg[0]
	#line = 'She is eating the fruits.'
	#line = 'She was eating the fruits.'
	#line = 'She is going to eat the fruits.'
	if tagg[1]=="VBG" and text[c-1][1]!='VB' and text[c-1][1]!='VBN':
		s[0] = text[c-1][0].capitalize()
		s.pop(c)
		s[c] = tagg[0]
	
	#line = 'She will be eating the fruits.'
	if tagg[1]=="VBG" and text[c-1][1]=='VB':
		s[0] = text[c-2][0].capitalize()
	
	#line = 'She has been eating the fruits.'
	#line = 'She had been eating the fruits.'
	if (tagg[1]=="VBZ" or tagg[1]=="VBD") and text[c+1][1]=='VBN' and text[c+2][1]== 'VBG':
		s[0] = text[c][0].capitalize()
		s.pop(c+1)
		
	#line = 'She had eaten the fruits.'
	#line = 'We have eaten the fruits.'
	if tagg[1]=="VBN" and tagg[0]!='been' and (text[c-1][0]== 'had' or text[c-1][0]== 'have') and text[c-2][1]!='MD':
		s[0] = text[c-1][0].capitalize()
		s.pop(c)
		s[c] = tagg[0]
		
	#line = 'She will have eaten the fruits.'
	#line = 'She will eat the fruits.'
	#line = 'She would have eaten the fruits.'
	if tagg[1]=="MD" and text[c+1][1]=='VB':
		s[0] = tagg[0].capitalize()
		s.pop(c+1)
	
	c  = c + 1
	
for i in range(len(s)-1): 
    q = q +' '+ s[i]
q = q + ' ?'
print(q)