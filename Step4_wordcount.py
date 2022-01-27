import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
import nltk
import re
from nltk.corpus import wordnet
import wordcounter
from collections import Counter
from gensim.models import Word2Vec
from nltk import ngrams

'''
This function removes html links, punctuation, stopwords and lemmatized words 
'''
def pre_processing(text_vector):
    j=0
    no_links = text_vector[:]
    no_punct = text_vector[:]
    no_stopwords = text_vector[:]
    no_lemma = text_vector[:]
    stop_words = set(nltk.corpus.stopwords.words('english'))
    
    for i in text_vector:
        
        no_sym = remsym(i)
        no_links[j] = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', no_sym , flags=re.MULTILINE)
        #print(no_links[j])
        
        no_punct[j] = "".join([c if c not in string.punctuation else " " for c in no_links[j]  ])
        #print(no_punct[j])
        word_tokens = nltk.tokenize.word_tokenize(no_punct[j]) 
        word_tokens = [token.lower() for token in word_tokens]
        no_stopwords[j] = [w for w in word_tokens if not w in stop_words]
        #print(no_stopwords[j])
        no_lemma[j] = [lemmatizer.lemmatize(w,get_wordnet_pos(w)) for w in no_stopwords[j]]
        #print(no_lemma[j])
        j=j+1
    
    return no_lemma
'''
Symbol removal function
'''
def remsym(vec):
    
    j=0
    str1 = " "
    for i in range(len(vec)):
        if vec[i] == "@" or vec[i] == ";" :
            j=1
        if vec[i] == " ":
            j=0
        if j==1:
            str1 += " "
        else:
            str1 += vec[i]              
    return str1

'''
word parts of speech tagging for efficient lemmatization
'''
def get_wordnet_pos(word):
    
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

# Load the dataset
file_dir = 'lib/data/normies-dump.csv'
with open(file_dir, encoding = 'utf8') as f:
        my_data_1 = pd.read_csv(f, sep=',')
my_data_normies = my_data_1.iloc[0:80000].copy()

my_data = my_data_normies.iloc.copy()
# Check the data
print(my_data.shape)
print(my_data.head(4))

# Convert body of all comments into lists 
x = my_data['body'].tolist()
lemmatizer =nltk.stem.WordNetLemmatizer()
l3 = pre_processing(x)
print(l3[0])



bigram = []
trigram = []
fourgram = []
# Splitting the sentences into bi, tri and four grams

for i in x:
    bigram.extend(list(ngrams(i.split(),2)))
    trigram.extend(list(ngrams(i.split(),3)))
    fourgram.extend(list(ngrams(i.lower().split(),4)))

#for unigram
model = Word2Vec(l3, min_count=1)

print(model)
x2 = []
# COmbine all sentences into one single document of text for wordcount extraction
[x2.extend(i) for i in l3] 
df3 = pd.DataFrame(list(Counter(x2).items()), columns = ['word', 'count'])
df3.to_csv('wordcount_unigram.csv', index=False)
words = list(model.wv.vocab)
print(words)
# save the unigram model
model.save('model_uni.bin')
# load the unigram model
new_model = Word2Vec.load('model_uni.bin')
print(new_model)

#for bigrams
model = Word2Vec(bigram, min_count=1)

print(model)
df4 = pd.DataFrame(list(Counter(bigram).items()), columns = ['word', 'count'])
df4.to_csv('wordcount_bigram.csv', index=False)
# save bigram model
model.save('model_bi.bin')
# load bigram model
new_model = Word2Vec.load('model_bi.bin')
print(new_model)

#for trigrams
model = Word2Vec(trigram, min_count=1)

print(model)
df5 = pd.DataFrame(list(Counter(trigram).items()), columns = ['word', 'count'])
df5.to_csv('wordcount_trigram.csv', index=False)

# save trigram model
model.save('model_tri.bin')
# load trigram model
new_model = Word2Vec.load('model_tri.bin')
print(new_model)
df6 = pd.DataFrame(list(Counter(fourgram).items()), columns = ['word', 'count'])
df6.to_csv('wordcount_fourgram.csv', index=False)
#for fourgrams
model = Word2Vec(fourgram, min_count=1)
# save fourgram model
model.save('model_four.bin')
# load fourgram model
new_model = Word2Vec.load('model_four.bin')
print(new_model)
