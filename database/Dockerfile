# Dockerfile


# on part d'une image postgres
FROM postgres:12.0

# on définit des variables d'environnements
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_USER=username
ENV POSTGRES_DB=database

# on copie le document qui permettra de lancer la création de nos tables
COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql