#!/usr/bin/env python3
from message_buffer import MessageBuffer
from scraper import CarScraper
from store import CarStorage
from email.message import EmailMessage
from logger import get_logger

import sys
import smtplib
import os
import json
import pywhatkit


def get_email_credentials():
    credentials_file = os.environ.get("SCRAPPER_DATA") + "/credentials.json"
    try:
        with open(credentials_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON from {credentials_file}: {e.msg}", e.doc, e.pos) from e
    except Exception as e:
        raise IOError(f"Error reading credentials file {credentials_file}: {e}") from e


class CarAuctionNotifier:
    def __init__(self, base_url):
        self.logger = get_logger(CarAuctionNotifier.__name__)
        self.scraper = CarScraper(base_url)
        self.store = CarStorage()
        self.message_buffer = MessageBuffer()

    def run(self):
        self.logger.info("Running car auction notifier")
        try:
            cars = self.scraper.get_car_listings()
            self.message_buffer.add(self.store.find_new_cars(cars))
            cars_to_send = self.message_buffer.get()

            if len(cars_to_send) > 0:
                self.send_email(self.format_message_content(cars_to_send))
                self.send_whatsapp_message(self.format_message_content(cars_to_send))
                self.message_buffer.remove_buffered_messages()

            self.store.update_cars(cars)
        except Exception as e:
            self.logger.error(f"Error in notifier: {e}")
            raise Exception(f"Error in notifier: {e}") from e


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
        self.logger.info("Sending WhatsApp message")
        pywhatkit.sendwhatmsg_instantly(phone_number, message_content, wait_time=10, tab_close=True)
        self.logger.info("WhatsApp message sent")

    def send_email(self, message):
        receiver = os.environ.get("EMAIL_ADDRESS")
        credentials = get_email_credentials()
        msg = self.setup_message(message, credentials["username"], receiver)
        self.logger.info("Sending an email")
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(credentials["username"], credentials["password"])
            smtp.send_message(msg)
        self.logger.info("Email sent")

    def setup_message(self, content, username, receiver):
        msg = EmailMessage()
        msg["Subject"] = "Nowe samochody są dostępne"
        msg["From"] = username
        msg["To"] = receiver
        msg.set_content(content)
        return msg


# Run the notifier
if __name__ == "__main__":
    CarAuctionNotifier("https://www.gedsted-autoophug.dk/biler/export-biler").run()
