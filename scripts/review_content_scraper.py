from bs4 import BeautifulSoup, Tag
import requests
import logging
import pandas as pd
from tqdm import tqdm
import time


class ReviewContentScraper:

    @staticmethod
    # Function to scrape the content of a review page
    def scrape_page(url: str) -> str:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the main div containing the list of games
            body = soup.find("div", class_="content-block-regular")
            # Find the div with class "article-hidden-content" (present when paywall is present)
            hidden_content = soup.find("div", class_="article-hidden-content")
            # Find all immediate <p> children of the body element
            if not body or not isinstance(body, Tag):
                logging.warning(f"Body not found on page {url}")
                return ""

            paragraphs = body.find_all("p", recursive=False)
            # If hidden content exists, find all <p> elements inside it
            if hidden_content and isinstance(hidden_content, Tag):
                hidden_paragraphs = hidden_content.find_all("p")
                paragraphs.extend(hidden_paragraphs)

            # Remove \n and spaces from the text
            concatenated_text = " ".join([p.get_text().strip() for p in paragraphs])
            cleaned_text = " ".join(concatenated_text.split())
            return cleaned_text
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            logging.error("Error on page: ", url)
            return ""

    @staticmethod
    def scrape_reviews(df: pd.DataFrame) -> pd.DataFrame:
        # For each Title and Link in the DataFrame, scrape the content
        reviews = []
        try:
            for _, row in tqdm(df.iterrows(), total=len(df)):
                title = row["title"]
                link = row["link"]
                content = ReviewContentScraper.scrape_page(link)
                reviews.append({"title": title, "link": link, "content": content})
                time.sleep(10)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        return pd.DataFrame(reviews)
