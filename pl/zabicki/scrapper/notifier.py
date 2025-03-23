#!/usr/bin/env python3

from scraper import CarScraper
from store import CarStorage
import sys

from logger import get_logger

class CarAuctionNotifier:
    def __init__(self, base_url):
        self.logger = get_logger(CarAuctionNotifier.__name__)
        self.scraper = CarScraper(base_url)
        self.store = CarStorage()

    def run(self):
        self.logger.info("Running car auction notifier")
        try:
            cars = self.scraper.get_car_listings()
            self.logger.info(f"Scraped {len(cars)} cars")
            new_cars = self.store.find_new_cars(cars)
            self.logger.info(f"Found {len(new_cars)} new cars.")
            # TODO add notification system and notify about new cars here
            self.store.update_cars(cars)
        except Exception as e:
            self.logger.error(f"Error in notifier: {e}")
            print(f"Error in notifier: {e}", file=sys.stderr)
            sys.exit(1)


# Run the notifier
if __name__ == "__main__":
    CarAuctionNotifier("https://www.gedsted-autoophug.dk/biler/export-biler").run()
