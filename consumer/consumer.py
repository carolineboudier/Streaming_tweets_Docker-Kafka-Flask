'''Le consumer reçoit les tweets depuis le cluster, leur applique un traitement et va transmettre à la base de données les informations nécessaires pour mettre en place une table de compte de hashtags, et une table de compte d'unigrammes'''


'''I) PRÉ-REQUIS'''
import json
import os
from kafka import KafkaConsumer, KafkaProducer
from json import loads
import psycopg2
import re
from gensim.utils import tokenize
from clean_tweet import preprocess_tweet

# connection au cluster Kafka
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')

# informations sur notre base de données
db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

'''II) FONCTIONS UTILES POUR LA MISE À JOUR DE LA BASE DE DONNÉE'''
# HASHTAGS
# fonction update_hashtags counts qui va être liée avec la database hashtags
def update_hashtag_count(payload):
    '''cette fonction prend en entrée une liste de tuples (hashtag,nbre d'occurences)'''
    # connection à la base de donnée
    conn = psycopg2.connect(user=db_user, host=db_host,port=db_port,password=db_pass,database=db_name)
    cur=conn.cursor()
    for i in payload:
        value = i[0] # texte du hashtags
        count = i[1] # nombre d'occurences de ce hashtag dans le tweet
        cur.execute("SELECT * FROM hashtags_table WHERE hashtags_table.hashtag_text='"+value+"'")
        result = len(cur.fetchall())>0
        # si le hashtag est déjà présent dans la base de données, on augmente son compte
        if(result):
            cur.execute("UPDATE hashtags_table SET count = hashtags_table.count+ %s WHERE hashtags_table.hashtag_text=%s",(count,value))
        # sinon on l'insère dans la base de données
        else:
            cur.execute("INSERT INTO hashtags_table VALUES (DEFAULT,%s,%s)",(value,count))
    conn.commit()
    conn.close()
    cur.close()

    # fonction get_hashtags qui permet de récupérer les hashtags des tweets puis de mettre à jour la BDD
def get_hashtags(text):
    try:
        hashtags = text["entities"]["hashtags"]
        if(len(hashtags)>0):
            hashtags =map(lambda w: (w["text"],1),hashtags)
            update_hashtag_count(hashtags)
    except:
        return False

# UNIGRAMMES (même principe que #HASHTAGS mais avec plus de préprocessing nécessaire)
    # fonction update_words_counts qui va être liée avec la database
def update_words_count(payload):
    conn = psycopg2.connect(user=db_user, host=db_host,port=db_port,password=db_pass,database=db_name)
    cur=conn.cursor()
    for i in payload:
        value = i
        count = 1
        cur.execute("SELECT * FROM unigrams_table WHERE unigrams_table.unigram_text='"+value+"'")
        result = len(cur.fetchall())>0
        if(result):
            cur.execute("UPDATE unigrams_table SET count = unigrams_table.count + 1 WHERE unigrams_table.unigram_text='"+value+"'")

        else:
            cur.execute("INSERT INTO unigrams_table VALUES (DEFAULT,%s,%s)",(value,count))

    conn.commit()
    conn.close()
    cur.close()

    # fonction get_words qui permet de récupérer les unigrammes des tweets
def get_words(text):
    try:
        my_text = text["text"]
        # on tokenise avec gensim
        tok_text=list(tokenize(my_text, deacc=True, lower=True))
        # on fait appel à ka fonction de préprocessing codée dans clean_tweet.py
        tok_text=preprocess_tweet(tok_text)
        if(len(tok_text)>0):
            update_words_count(tok_text)
    except:
        return False

'''III) LIEN AVEC LE PRODUCER ET MISE À JOUR DE NOS BASES DE DONNÉES'''
if __name__ == '__main__':
    print('Application started')
    # on connecte notre consumer au cluster Kafka
    consumer = KafkaConsumer(
        TRANSACTIONS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,auto_offset_reset='earliest',enable_auto_commit=True,group_id='my-group',value_deserializer= (lambda x: json.loads(x.decode('utf-8'))))
    # pour chaque tweet reçu on met à jour la table hashtags et la table unigrammes
    for message in consumer:
        twitter_message = message.value
        get_words(twitter_message)
        get_hashtags(twitter_message)
        

