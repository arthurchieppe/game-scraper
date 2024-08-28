import logging
from ReviewLinkScraper import ReviewLinkScraper
from ReviewContentScraper import ReviewContentScraper
from datetime import datetime
import pandas as pd


def save_to_csv(df, filename) -> None:
    now = datetime.now()
    filename = filename.replace(".csv", "")
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    file_to_save = f"{filename}_{timestamp}.csv"
    df.to_csv(file_to_save, index=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Get all review links from the first 75 pages
    # links_df = ReviewLinkScraper.get_all_review_links(range(1, 3))
    links_df = pd.read_csv("reviews_links.csv")
    save_to_csv(links_df, "reviews_links.csv")
    # Get only 5 first rows of df
    reviews_df = ReviewContentScraper.scrape_reviews(links_df)
    save_to_csv(reviews_df, "reviews_content.csv")
