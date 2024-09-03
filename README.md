# game-scraper

## Introduction and motivation

This project is a Game Recommender that utilizes TF-IDF (Term Frequency-Inverse Document Frequency) to recommend games based on a user descritption of their ideal game. It leverages data scraped from [Gamerant's](https://gamerant.com/game-reviews/) reviews available in their website. These reviews were scraped using BeautifulSoup.

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

4. Add python project root dir to PYTHONPATH. Navigate to the root of project and run the following:

```
export PYTHONPATH=$(pwd)
```

## Data Scraping and Training

This project includes both a scraper and a web server for deploying a trained model. Before running the project it is important to verify that all files required to execute the model are available and correctly located and named.

### Data Directory
Ensure the following file exists in the `data` directory:
- **reviews_content.csv**: A CSV file containing the scraped content. It must have the following columns:
  - `title`
  - `link`
  - `content`

### Models Directory
Ensure the following files are available in the `models` directory:
- **tfidf.pkl**: Serialized TF-IDF vectorizer object.
- **documents_vector.pkl**: Serialized TF-IDF matrix of the scraped documents.

If you have all these files inplace and correctly named, you are free to skip to the **[usage](#usage)** section. If any of these files are missing, you will need to run the training script:

```
python3 scripts/get_data_and_train.py
```

This script has three main parts to it:
1. **Scrape for all review links**: during this part the scraper will cycle through all the pages in https://gamerant.com/game-reviews/1 all the way to https://gamerant.com/game-reviews/75, which is the max number of pages in the website. This way, the scraper can make a collection of all the available game titles and review links in a relatively short period of time. The results will be a dataframe, which will be saved as a csv file with the prefix `reviews_links` and the timestamp as a suffix.

2. **Scrape through all the gathered links**: In this part, the scraper will visit each review link collected in the first step. It will extract the review content, including the title, link, and review text. The results will be compiled into a dataframe and saved as a CSV file named `reviews_content` in the `data` directory, with the timestamp as the filename suffix.

3. Training: In this step, the `TfidfTrainer` class from the provided code will be used to train a TF-IDF vectorizer on the review content. The process involves the following steps:

- **Initialization**: The `TfidfTrainer` class is initialized with a DataFrame containing the review content.
- **Training**: The `train` method of the `TfidfTrainer` class:
  - Creates a `TfidfVectorizer` instance.
  - Fits the vectorizer to the review content and transforms the content into a TF-IDF matrix.
  - Saves the trained vectorizer and the TF-IDF matrix to the `./models/` directory as `tfidf.pkl` and `documents_vector.pkl`, respectively.
  - Logs the shapes of the input data and the resulting document vectors.
- **Error Handling**: The method includes error handling for common issues such as missing columns, fitting errors, and missing directories.

Currently, the scripts require manual changes to certain variables, such as the file paths for the data and model files. As such, it is important to remove the timestamp from the filename, as it is only there to prevent accidental overwrites. Since this file will be used for further processing and model training, it should be named appropriately. Future updates will include modular scripts that support environment variables for easier configuration.

Assuming all these files are correctly named and place, it is possible to proceed.

## Usage

Before running the project, ensure that the file paths specified during the instantiation of the `TfidfUtility` class in `app/main.py` are correct. Below is the default configuration:
```python
tfidf = TfidfUtility.load(
    data_path="./data/reviews_content.csv",
    tfidf_path="./models/tfidf.pkl",
    documents_vector_path="./models/documents_vector.pkl",
)
```

You can run the web server in one of two ways:

1. **[Manually setting up a Python virtual environment](#option-1-manual-setup-with-python-virtual-environment)**

2. **[Using a Docker container](#option-2-using-a-docker-container)**

### Option 1: Manual Setup with Python Virtual Environment

### Prerequisites
- Python 3.10 (Tested on 3.12.5)

To run the API, run the following from the root folder of the project:
```bash
python3 app/main.py
```


You can quickly try out the API by acessing the FastAPI documentation at [localhost:8000/docs](http://localhost:8000/docs) with your browser of choice.

You can also use a client such as Postman or curl

### Option 2: Using a Docker Container​

### Prerequisites
- Docker

To run this application using docker, first build the docker image:
```bash
docker build -t game-scraper .
```

After that, you can run the container with the following command(note that you can change the host port binding):
```bash
docker run -p 10136:8888 game-scraper
```



## Testing

Unit tests for relevant cases are included in this project. To execute them, run the following in the terminal from the project's root:

```bash
pytest test/
```

Here are the three main scenarios and test cases provided:

* A test that yields 10 results: "A racing game with mercedes cars": http://10.103.0.28:10136/query?query=A%20racing%20game%20with%20mercedes%20cars

* A test that yields more than 1, but less than 10 results because there are not enough relevant documents in the database: "A puzzle game featuring portal and teleportation mechanics": http://10.103.0.28:10136/query?query=A%20puzzle%20game%20featuring%20portal%20and%20teleportation%20mechanics

* A test that yields something non-obvious (remember to comment why this is non-obvious): "A game that combines elements of horror and educational content": http://10.103.0.28:10136/query?query=A%20game%20that%20combines%20elements%20of%20horror%20and%20educational%20content

The last query is non-obvious because horror games and educational content are typically not associated with each other. The results yielded by this query were such that the most relevant result was an educational game, followed only by horror games. This could be because there are more horror games than educational games in the database. As such, the TF-IDF algorithm preferred the educational game because it is more unique in the context of the database.


## Authors

Arthur Chieppe