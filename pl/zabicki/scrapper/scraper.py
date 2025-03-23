import random

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from logger import get_logger


class CarScraper:
    def __init__(self, base_url):
        self.logger = get_logger(CarScraper.__name__)
        self.base_url = base_url
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
            ]

    def get_browser_context(self, playwright):
        return playwright.chromium.launch(headless=True).new_context(
            user_agent=random.choice(self.user_agents),
            viewport={"width": random.randint(1200, 1920), "height": random.randint(800, 1080)},
            locale="en-US",
            timezone_id="Europe/London"
        )

    def get_car_listings(self):
        with sync_playwright() as p:
            browser = self.get_browser_context(p)
            all_listings = []
            page_num = 0

            while True:
                page = browser.new_page()
                page_num = page_num + 1
                if page_num == 1:
                    page.goto(self.base_url, timeout=120000)
                else:
                    page.goto(self.base_url + "/" + str(page_num), timeout=120000)

                page.wait_for_selector("body > div.bg-light.text-primary > div > div:nth-child(3) > div > div > div > div")
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                listings =  self.extract_car_data(soup)
                all_listings.extend(listings)
                if len(listings) < 128:
                    break

            browser.close()
            self.logger.info(f"Scraped {len(all_listings)} cars.")
            return all_listings

    def extract_car_data(self, soup):
        listings = soup.find_all("a", class_ = "card text-reset text-decoration-none h-100")
        page_cars = []

        for listing in listings:
            link = listing["href"] if listing.has_attr("href") else None
            image_src = listing.find("img")["src"] if listing.find("img") else None
            model = listing.find("div", class_ = "h6 card-title mb-2").text.strip() if listing.find("div", class_="h6 card-title mb-2") else None
            mileage_year = listing.find("div", class_="small mt-auto d-flex justify-content-between")

            # Extract mileage and production year
            mileage, year = None, None
            if mileage_year:
                spans = mileage_year.find_all("span")
                if len(spans) == 2:
                    mileage = spans[0].text.strip()
                    year = spans[1].text.strip()

            page_cars.append({"model": model,
                              "image source": image_src,
                              "link": link,
                              "mileage": mileage,
                              "production year": year})

        return page_cars
