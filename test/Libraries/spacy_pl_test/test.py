import spacy
from spacy.lang.pl.examples import sentences 

pl_vocab = spacy.load('pl_core_news_lg')
doc = pl_vocab(sentences[0])
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.dep_)