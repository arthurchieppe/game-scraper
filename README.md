# game-scraper

## Description and motivation

## How to install 

## How to run

Run the following in the command line, to ensure all the python project structure and imports work flawlessly.

```
export PYTHONPATH=$(pwd)
```

## How it works

## Data sources

## How to test

Here are the three main scenarios and test cases provided:

* A test that yields 10 results: "A racing game with mercedes cars"

* A test that yields more than 1, but less than 10 results because there are not enough relevant documents in the database: "A puzzle game featuring portal and teleportation mechanics"

* A test that yields something non-obvious (remember to comment why this is non-obvious): "A game that combines elements of horror and educational content". 

The last query is non-obvious because horror games and educational content are typically not associated with each other. The results yielded by this query were such that the most relevant result was an educational game, followed only by horror games. This could be because there are more horror games than educational games in the database. As such, the TF-IDF algorithm preferred the educational game because it is more unique in the context of the database.


## Running the Project with Docker

```bash
docker build -t game-scraper .
docker run -d -p 10254:8888 game-scraper
```


## Authors

Arthur Chieppe