FROM python:3.10.8
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD echo "Wait 30s..."; sleep 30; python3 main.py --load --truncate --debug --mongodb-host mongodb --neo4j-host neo4j