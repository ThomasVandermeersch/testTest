# Projet-GLO-4035/7035

Projet réalisé dans le cadre du cours de base de données avancées GLO-4035/7035 lors de la session d'automne 2022.
Par Billot Mathias, Labrie Martin et Vandermeersch Thomas.

## Construire les instances Docker avec docker-compose

Ouvrir une invite de commandes et entrer les instructions suivantes
````
docker-compose up
````

## Architecture du projet

### [back-api](./back-api/)
`Dockerfile` utilisé pour construire l'API et les fichiers sources de celle-ci.

### [datasets](./datasets/)
Ffichiers de données originaux et, si présents, les fichiers de données travaillés.

### [db-mongodb](./db-mongodb/)
`Dockerfile` utilisé pour construire la base de données MongoDB.

### [db-neo4j](./db-neo4j/)
`Dockerfile` utilisé pour construire la base de données Neo4j.

### [script-etl](./script-etl/)
Script ETL utilisé lors du projet.

## Commande pour utiliser le script ETL

Pour effectuer le pipeline en entier

`python3 script-etl/main.py -etl`

### Paramètres optionnels

`--debug` Affiche plus d'informations dans la console

`--truncate` S'assure que les bases de données sont vides lors du pipeline

`--skip-nearest-map` Permet de sauter l'opération d'association des restaurants à leur plus proche piste cyclable car cette opération peut prendre __plusieurs heures__.
