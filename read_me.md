# PROJET DONNÉES DISTRIBUÉES - ENSAE 2021
## Caroline Boudier et Florian Schirrer

## 1) Objectif : 
Notre idée est de parvenir à construire une application de streaming avec Apache Kafka en utilisant Python et Postgresql pour alimenter une application Flask, le tout de manière conteneurisée (en utilisant Docker-Compose). 
Pour mettre en place une telle architecture nous avons décidé d'utiliser l’API Twitter comme source de données pour y récupérer un flux de tweets qui seront ensuite traités pour mettre à jour un dashboard interactif basique. 


## 2) Architecture générale : 

Les données viennent de **l'API-Twitter** qui permet de "streamer" les tweets publiés en live. Nous nous intéressons aux tweets en français qui comprennent les mots clés "corona virus", "COVID-19", "vaccin", et "covid". Une fois que l'application Flask finale sera lancée, elle sera mise à jour automatiquement avec tous les tweets publiés à partir du lancement et permettra d'afficher les hashtags et unigrammes les plus fréquents dans le flux de tweets étudiés. *En fonction de l'importance du flux de tweets à un instant -t, les graphiques peuvent donc mettre un peu de temps avant de se remplir (s'il y a peu de tweets publiés en ce moment)* 

 
Nous avons décidé de faire tourner notre cluster Kafka de manière indépendante des autres applications pour se rapprocher d’une application en production. Nous avons donc **deux fichiers Docker Compose** : 
- (1) un fichier Docker Compose de configuration (avec les services Kafka et Zookeeper)
- (2) un fichier Docker Compose pour les applications (avec les services : producer, consumer, database et flask_app)

Pour que ces deux fichiers Docker Compose puissent communiquer nous mettons en place un **réseau Docker** que l’on appelera kafka-network. 

En ce qui concerne **le cluster Kafka (1)**, le Docker Compose de configuration (``docker-compose.kafka.yml``) comprend deux services : 
- le broker Kafka 
- une instance Zookeeper. 

En ce qui concerne les **applications (2)**, quatre conteneurs sont impliqués. Chacun de ces conteneurs dispose d’un folder associé comprenant le dockerfile (‘Dockerfile’) utilisé pour builder l’image, les pré-requis (‘requirements.txt’) et le script à exécuter (ficher .py). 
- un “producer” qui se connecte sur l’API de streaming de Twitter et transmet ce flux de données au consumer via le serveur Kafka *(script producer.py)*
- un “consumer” qui reçoit les tweets, les traite et les injecte dans une base de données Postgres *(script consumer.py lié avec le script clean_tweet.py pour les fonctions de préprocessing de texte)*
- une base de données (‘db’) dans laquelle sont stockées des informations relatives aux tweets (hashtags et leur nombre dans la table hashtags_table, unigrammes les plus courants et leur nombre dans la table unigrams_table ) *(script create_fixtures.sql qui permet de créer les tables)*
- un conteneur dédié à l’application Flask. On y requêtera la base de données pour créer un serveur Flask qui permettra d’afficher les informations collectées. *(script flask_app.py lié avec les repo static/templates pour le design de l'HTML)*


## 3) Démarrage rapide : comment faire tourner l’application? 

### a) Créer le réseau kafka-network ...
... pour permettre la communication entre les applications et le cluster Kafka
- ``docker network create kafka-network``

### b) Lancer le cluster Kafka ...
Se placer dans le dossier ``[DD Projet final 2021] Florian Schirrer Caroline Boudier`` et lancer le cluster Kafka
- ``docker-compose -f docker-compose.kafka.yml up``

### c) Lancer les applications
Dans un autre terminal se placer dans le même dossier et lancer les applications
- ``docker-compose build``
- ``docker-compose up``
- Puis ouvrir l’application flask en suivant le lien : http://0.0.0.0:5000/

## 4) Arrêter l’application

- Pour arrêter les applications 
- ``docker-compose down``
- Pour mettre fin au cluster Kafka
- ``docker-compose -f docker-compose.kafka.yml stop``
- Pour supprimer le réseau kafka
- `` docker network rm kafka-network``

## 5) Liens qui nous ont aidé et inspiré pour mettre en place ce projet : 

- Docker/Flask/Postgres
- https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

- Kafka/Twitter
- https://medium.com/@pblmjc/tracking-what-people-are-tweeting-during-the-covid-19-pandemic-using-apache-kafka-be1b6b597a3

- Docker-Compose/Postgres
- https://dev.to/stefanopassador/docker-compose-with-python-and-posgresql-33kk

- Docker-Compose/Kafka
- https://florimond.dev/en/posts/2018/09/building-a-streaming-fraud-detection-system-with-kafka-and-python/

