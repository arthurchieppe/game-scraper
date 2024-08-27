import requests
from bs4 import BeautifulSoup


# Function to scrape game titles and publishers from Steam
def scrape_games_from_steam():
    url = "https://store.steampowered.com/search/?sort_by=Released_DESC&tags=-1&category1=998"  # Example: New Releases on Steam

    # Send a request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all game titles and publishers
        games = []
        for item in soup.find_all("a", class_="search_result_row"):
            title = item.find("span", class_="title").text.strip()
            # Publisher name is usually inside a div or span, find accordingly
            publisher = (
                item.find("div", class_="search_reviewscore")
                .find_next_sibling("div")
                .text.strip()
            )
            games.append({"title": title, "publisher": publisher})

        return games
    else:
        print(f"Failed to retrieve data from {url}")
        return []


# Scrape and print the games
games = scrape_games_from_steam()
for game in games:
    print(f"Title: {game['title']}\nPublisher: {game['publisher']}\n")
