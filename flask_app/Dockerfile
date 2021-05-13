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

# on lance l'application flash (chemin défini dans le docker-compose) sur l'host 0.0.0.0
CMD ["flask","run","--host=0.0.0.0"]
