#!/usr/bin/env python3

from scraper import CarScraper
from store import CarStorage
import sys
import smtplib
import os
import json
from email.message import EmailMessage
import pywhatkit

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
            if len(new_cars) > 0:
                self.logger.info("Sending an email")
                email_address = os.environ.get("EMAIL_ADDRESS")
                self.send_email(self.format_message_content(new_cars), email_address)
                self.logger.info("Email sent")

                self.logger.info("Sending WhatsApp message")
                self.send_whatsapp_message(self.format_message_content(new_cars))
                self.logger.info("Sent WhatsApp message")
            self.store.update_cars(cars)
        except Exception as e:
            self.logger.error(f"Error in notifier: {e}")
            print(f"Error in notifier: {e}", file=sys.stderr)
            sys.exit(1)

    def format_message_content(self, new_cars):
        car_strings = ["Nowe samochody są dostępne"]
        for car in new_cars:
            car_info = (f"Model: {car['model']}\n"
                        f"Przebieg: {car['mileage']}\n"
                        f"Rok produkcji: {car['production year']}\n"
                        #f"{car['image source']}\n"
                        f"Link: https://www.gedsted-autoophug.dk{car['link']}\n")
            car_strings.append(car_info)
        return "\n\n".join(car_strings)

    def send_whatsapp_message(self, message_content):
        phone_number = os.environ.get("PHONE_NUMBER")
        pywhatkit.sendwhatmsg_instantly(phone_number, message_content, wait_time=10, tab_close=True)

    def send_email(self, message, receiver):
        credentials = self.get_email_credentials()
        msg = self.setup_message(message, credentials["username"], receiver)
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(credentials["username"], credentials["appPassword"])
            smtp.send_message(msg)

    def setup_message(self, content, username, receiver):
        msg = EmailMessage()
        msg["Subject"] = "Nowe samochody są dostępne"
        msg["From"] = username
        msg["To"] = receiver
        msg.set_content(content)
        return msg

    # TODO throw error when file not exists
    def get_email_credentials(self):
        credentials_file = "/home/krzysztof/scrapper/data/credentials.json"
        if os.path.exists(credentials_file):
            with open(credentials_file, "r", encoding="utf-8") as file:
                return json.load(file)

# Run the notifier
if __name__ == "__main__":
    CarAuctionNotifier("https://www.gedsted-autoophug.dk/biler/export-biler").run()
