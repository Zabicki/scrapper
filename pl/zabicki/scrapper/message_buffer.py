from datetime import datetime
from logger import get_logger

import os
import json

class MessageBuffer:
    def __init__(self):
        self.filename = os.environ.get("SCRAPPER_DATA") + "/buffered_cars.json"
        self.logger = get_logger(MessageBuffer.__name__)
        self.messages = self.load_buffered_messages()

    def add(self, messages):
        self.messages.extend(messages)
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.messages, file, indent=2, ensure_ascii=False)  # create empty file
        except IOError as e:
            self.logger.error(f"Error emptying buffered cars file {self.filename}: {e}")


    def get(self):
        now = datetime.now()
        if 8 <= now.hour <= 21:
            result_messages = self.messages
            self.messages = []
            return result_messages
        else:
            self.logger.info(f"Buffering {len(self.messages)} messages until 8 AM.")
            return []

    def load_buffered_messages(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            try:
                with open(self.filename, 'w') as file:
                    json.dump([], file, indent=2, ensure_ascii=False) # create empty file
            except IOError as e:
                self.logger.error(f"Error creating buffered cars file {self.filename}: {e}")

        self.logger.warn(f"Buffered cars file {self.filename} not found. ")
        return []

    def remove_buffered_messages(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump([], file, indent=2, ensure_ascii=False)  # create empty file
        except IOError as e:
            self.logger.error(f"Error emptying buffered cars file {self.filename}: {e}")