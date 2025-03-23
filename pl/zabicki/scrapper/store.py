import os
import json

from logger import get_logger

class CarStorage:
    def __init__(self, filename = "scrapper/data/cars.json"):
        self.logger = get_logger(CarStorage.__name__)
        self.filename = filename
        self.cars = self.load_cars()

    def load_cars(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)

        self.logger.warn(f"Storage file {self.filename} not found. ")
        return []

    def save_cars(self):
        if os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.cars, file, indent=2, ensure_ascii=False)
        else:
            with open(self.filename, "x", encoding="utf-8") as file:
                json.dump(self.cars, file, indent=2, ensure_ascii=False)
        self.logger.info("Updated listed cars storage.")

    def update_cars(self, new_cars):
        existing_links = {car["link"] for car in self.cars}
        new_links = {car["link"] for car in new_cars}

        # Remove sold cars
        self.cars = [car for car in self.cars if car["link"] in new_links]

        # Add new cars
        for car in new_cars:
            if car["link"] not in existing_links:
                self.cars.append(car)

        # Save the updated list
        self.save_cars()

    def find_new_cars(self, scraped_cars):
        existing_links = {car["link"] for car in self.cars}
        scraped_links = {car["link"] for car in scraped_cars}

        new_links = scraped_links - existing_links
        new_cars = [car for car in scraped_cars if car["link"] in new_links]
        for new_car in new_cars:
            self.logger.info(f"Scraped new car: "
                             f"Model: {new_car["model"]} "
                             f"Mileage: {new_car["mileage"]} "
                             f"Year: {new_car["production year"]}")
        return new_cars