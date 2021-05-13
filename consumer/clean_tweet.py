"""Package pour nettoyer les tweets"""

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


'''Pour le décompte des mots
on fait en sorte de ne pas compter les mots les plus courants
de la langue française
que l'on obtient grâce à une liste déjà préparée par nltk'''

stoplist = stopwords.words('french')
rajouts_stoplist=['ça','a','fait','tout','rt']
stoplist = stoplist+rajouts_stoplist

def preprocess_tweet(tweet):
    final_vec=[]
    for word in tweet:
    # on retire les noms d'utilisateurs cités, les stopwords et les url
        if word[0]!="@" and (word[0:4]!='http') and (word not in stoplist):
        # on retire les chiffres
            if not word.isnumeric():
                final_vec.append(word)
    return final_vec
  
