# game-scraper

## Introduction and motivation

This project is a Game Recommender that utilizes TF-IDF (Term Frequency-Inverse Document Frequency) to reccomend games based on a user descritption of their ideal game. It leverages data scraped from [Gamerant's](https://gamerant.com/game-reviews/) reviews available in their website. These reviews were scraped using BeautifulSoup.

## Folder structure:

- **app/**: Contains the FastAPI application code, including API routes and the recommendation logic.
- **data/**: Stores resulting dataset from the scraper and any intermediate processed files in order to achieve it.
- **models/**: Contains trained models and vectorizers.
- **scripts/**: Includes scripts for data scraping and preprocessing.
- **test/**: Contains the unit tests required in the project especification.


## Installation Steps

1. Clone the repository:
```
git clone https://github.com/arthurchieppe/game-scraper.git
cd game-scraper/
```

2. Create virtual environment (recommended)
```
python3 -m venv .venv
source env/bin/activate
```

3. Install dependencies
```
pip3 install -r requirements.txt
```

## Usage
Before actually running the project, it is important to first certify that the needed configurations and files for it to run are available.
Since this cproject encompasses both a scraper and a webserver for deploying a trained model, first we need the Tfidf model is trained. 
You can run this project in one of two ways: by manually setting up a Python virtual environment or by using a Docker container.

### Option 1: Manual Setup with Python Virtual Environment







## Option 2: Using a Docker Container​⬤

### Prerequisites
Python 3.10 (Tested on 3.12.5)


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