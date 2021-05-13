'''Le producer se branche sur l'API Twitter pour streamer des tweets en live (filtrés par certains critères) puis les transmet au cluster Kafka'''

import os
import json
from kafka import KafkaConsumer, KafkaProducer, KafkaClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# connection au cluster Kafka
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')

# clés d'identification pour se connecter sur l'API Twitter
consumer_key = "pEoCQ3xZXxHD3dckpRjxJsxzY"
consumer_secret = "SCj0UrwtcmQUq6ROC5pPnF6Vzm1QCAPAh75kZeZyjug9iLcqI9"
access_token = "2884852895-eTwycUiyhoQX2GfmA7neFTvwlLwhMWrDFid4caz"
access_token_secret = "IyOihXSvP2g1R8s8h4F9PRa7kSYT5pj8oKQjj3wBmVSK9"


class TwitterListener(StreamListener):
    def on_data(self, raw_data):
        # le producer enverra ce qu'il recevra via le topic TRANSACTIONS TOPIC
        producer.send(TRANSACTIONS_TOPIC, raw_data.encode('utf-8'))
        return True
    def on_error(self, status_code):
        print(status_code)

if __name__ == '__main__':
    # on crée le producer
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL)
    # on instancie un objet Twitter Listener
    l = TwitterListener()
    # on s'authentifie
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # on crée le flux de streaming
    stream = Stream(auth, l)
    # on indique ici les tweets que l'on souhaite filtrer
    stream.filter(languages=["fr"],track=['corona virus','COVID-19','vaccin','covid'])
