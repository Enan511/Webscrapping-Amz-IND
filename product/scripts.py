import requests as req
from bs4 import BeautifulSoup
import csv


class AmazonScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "DNT": "1",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"
        }
        self.soup = None

    def fetch_page(self):
        try:
            response = req.get(self.url, headers=self.headers)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except req.exceptions.RequestException as e:
            raise SystemExit(f"Failed to retrieve the webpage: {e}")

    def get_product_title(self):
        try:
            title = self.soup.find(id='productTitle').get_text(strip=True)
            return title
        except AttributeError:
            return "Product title not found."

    def get_product_price(self):
        try:
            price = self.soup.find(class_='a-price-whole').get_text(strip=True)
            return price
        except AttributeError:
            return "Product price not found."

    def get_product_image(self):
        try:
            image = self.soup.find(id="landingImage")
            return image['src'] if image else "Product image not found."
        except (AttributeError, KeyError):
            return "Product image not found."

    def get_product_details(self):
        try:
            # Product details are in a table or list under certain classes or IDs.
            details_section = self.soup.find(id="feature-bullets")
            details = details_section.find_all('span', class_='a-list-item')
            formatted_details = "\n".join([f"- {detail.get_text(strip=True)}" for detail in details])
            return formatted_details if formatted_details else "Product details not found."
        except AttributeError:
            return ["Product details not found."]

    def scrape_product_details(self):
        self.fetch_page()
        return {
            "title": self.get_product_title(),
            "price": self.get_product_price(),
            "image_url": self.get_product_image(),
            "description": self.get_product_details(),
        }


def scrape_products_from_csv(csv_file_path):
    scraped_data = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            url = row[0]  # Assuming the URL is in the first column
            scraper = AmazonScraper(url)
            product_details = scraper.scrape_product_details()
            scraped_data.append(product_details)
    return scraped_data
