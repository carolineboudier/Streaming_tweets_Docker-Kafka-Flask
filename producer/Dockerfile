# Dockerfile

# on part d'une image python
FROM python:3.6

# on se crée un dossier courant
WORKDIR /usr/app

# on copie le document requirements.text
ADD ./requirements.txt ./

# on exécute la commande pour installer les requirements
RUN pip install -r requirements.txt

# on copie le reste des documents
ADD ./ ./

# on fait tourner le script producer.py 
CMD ["python", "producer.py"]