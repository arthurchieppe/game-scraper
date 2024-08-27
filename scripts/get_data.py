import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import logging

# Function to scrape game reviews from a specific page
def scrape_reviews(page_number):
    url = f"https://gamerant.com/game-reviews/{page_number}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the main div containing the list of games
    main_div = soup.find('div', class_='sentinel-listing-page-list')
    if not main_div:
        return []  # Return empty if the main div is not found

    # Extract the relevant data from the children of the main div
    reviews = []
    game_divs = main_div.find_all('div', recursive=False)
    
    for index, game_div in enumerate(game_divs):
        a_tag = game_div.find('a')
        if a_tag:
            link = "https://gamerant.com" + a_tag['href']

        # game_div.find('div', class_='w-display-card-content regular article-block')
        # if game_div:
        title = game_div.find('h5', class_='display-card-title').get_text(strip=True)
        
        if title and link:
            reviews.append({'title': title, 'link': link})
        else:
            logging.warning(f"Missing data for game {index + 1} on page {page_number}")

    
    return reviews

# Example usage: Scrape the first 3 pages
all_reviews = []
for i in tqdm(range(1, 4), desc="Página: "):  # Pode ir até 75
    all_reviews.extend(scrape_reviews(i))
    time.sleep(1)  # Add a delay to prevent overwhelming the server

# Print the scraped data
for review in all_reviews:
    print(review)