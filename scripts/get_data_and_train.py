import logging
from scripts.review_link_scraper import ReviewLinkScraper
from scripts.review_content_scraper import ReviewContentScraper
from scripts.tfidf_trainer import TfidfTrainer
from datetime import datetime

# import pandas as pd


# Save the DataFrame to a CSV file with the current timestamp as suffix
def save_to_csv(df, filename) -> None:
    now = datetime.now()
    filename = filename.replace(".csv", "")
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    file_to_save = f"{filename}_{timestamp}.csv"
    df.to_csv(file_to_save, index=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Get all review links from the first 75 pages
    links_df = ReviewLinkScraper.get_all_review_links(range(1, 76))
    # Save backup of the links in case any error occurs
    save_to_csv(links_df, "reviews_links.csv")

    # Use the links to access each review page and scrape the content
    reviews_df = ReviewContentScraper.scrape_reviews(links_df)
    # Save the reviews content to a CSV file
    save_to_csv(reviews_df, "reviews_content.csv")

    # Train the TF-IDF model using the reviews content
    trainer = TfidfTrainer(reviews_df)
    # This will save the models to the models directory
    trainer.train()
