import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/"
START_URL = BASE_URL + "catalogue/page-1.html"

def extract_star_rating(article):
    classes = article.select_one("p.star-rating")["class"]
        ratings = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five']
            for r in ratings:
                    if r in classes:
                                return r
                                    return "Unknown"

                                    def get_books_from_page(url):
                                        response = requests.get(url)
                                            soup = BeautifulSoup(response.text, "html.parser")
                                                books = []

                                                    for article in soup.select("article.product_pod"):
                                                            title = article.h3.a["title"]
                                                                    price = article.select_one(".price_color").text
                                                                            availability = article.select_one(".availability").text.strip()
                                                                                    star_rating = extract_star_rating(article)
                                                                                            relative_url = article.h3.a["href"]
                                                                                                    product_url = urljoin(url, relative_url)

                                                                                                            books.append({
                                                                                                                        "title": title,
                                                                                                                                    "price": price,
                                                                                                                                                "availability": availability,
                                                                                                                                                            "rating": star_rating,
                                                                                                                                                                        "product_page": product_url
                                                                                                                                                                                })

                                                                                                                                                                                    return books, soup

                                                                                                                                                                                    def scrape_all_books():
                                                                                                                                                                                        current_url = START_URL
                                                                                                                                                                                            all_books = []

                                                                                                                                                                                                while True:
                                                                                                                                                                                                        print(f"Scraping: {current_url}")
                                                                                                                                                                                                                books, soup = get_books_from_page(current_url)
                                                                                                                                                                                                                        all_books.extend(books)

                                                                                                                                                                                                                                next_button = soup.select_one("li.next > a")
                                                                                                                                                                                                                                        if next_button:
                                                                                                                                                                                                                                                    next_url = urljoin(current_url, next_button["href"])
                                                                                                                                                                                                                                                                current_url = next_url
                                                                                                                                                                                                                                                                            time.sleep(1)
                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                break

                                                                                                                                                                                                                                                                                                    return all_books

                                                                                                                                                                                                                                                                                                    if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                        all_books = scrape_all_books()

                                                                                                                                                                                                                                                                                                            with open("books.json", "w", encoding="utf-8") as f:
                                                                                                                                                                                                                                                                                                                    json.dump(all_books, f, indent=4, ensure_ascii=False)

                                                                                                                                                                                                                                                                                                                        print(f"Scraped {len(all_books)} books and saved to 'books.json'")