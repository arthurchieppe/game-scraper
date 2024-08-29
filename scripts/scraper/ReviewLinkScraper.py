import requests
from bs4 import BeautifulSoup, Tag
from tqdm import tqdm
import time
import logging
import pandas as pd
from datetime import datetime


class ReviewLinkScraper:

    # Function to scrape game reviews from a specific page
    @staticmethod
    def scrape_page(page_number: int) -> list[dict]:
        url = f"https://gamerant.com/game-reviews/{page_number}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the main div containing the list of games
        main_div = soup.find("div", class_="sentinel-listing-page-list")
        if not main_div or not isinstance(main_div, Tag):
            logging.warning(f"Main div not found or not a Tag on page {page_number}")
            return []  # Return empty if the main div is not found or not a Tag

        # Extract the relevant data from the children of the main div
        reviews = []
        game_divs = main_div.find_all("div", recursive=False)

        for index, game_div in enumerate(game_divs):
            a_tag = game_div.find("a")
            if a_tag:
                link = "https://gamerant.com" + a_tag["href"]

            title = game_div.find("h5", class_="display-card-title").get_text(
                strip=True
            )

            if title and link:
                reviews.append({"title": title, "link": link})
            else:
                logging.warning(
                    f"Missing data for game {index + 1} on page {page_number}"
                )

        return reviews

    @staticmethod
    def save_to_csv(df):
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"reviews_links_{timestamp}.csv"
        df.to_csv(filename, index=False)

    @staticmethod
    def get_all_review_links(page_range: range) -> pd.DataFrame:
        # Example usage: Scrape the first 3 pages
        all_reviews = []
        try:
            for i in tqdm(page_range, desc="Página: "):  # Pode ir até 75
                all_reviews.extend(ReviewLinkScraper.scrape_page(i))
                time.sleep(1)  # Add a delay to prevent overwhelming the server
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            logging.info("Data collected so far will be saved to csv")
            # Save the data collected so far

            df = pd.DataFrame(all_reviews)
            exit(1)

        # Save df as csv
        df = pd.DataFrame(all_reviews)
        logging.info("Data saved to csv")
        return df
