# Question-generation

#Steps to install spacy
1. Open anaconda command prompt
2. conda install -c conda-forge spacy
3. conda install spacy
4. python -m spacy download en


#to set up coreNLPServer
1. Download stanford corenlp link: https://stanfordnlp.github.io/CoreNLP/download.html
2. open command prompt
3. set path for stanford corenlp folder
4. run command

java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000

 link: https://www.khalidalnajjar.com/setup-use-stanford-corenlp-server-python/
 
#install requirements

pip install -r requirements.txt
