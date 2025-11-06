import time
import pandas as pd
from pymongo import MongoClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FOLDER_PATH = r"./data"
CSV_PATH = r"./data/data.csv"

client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]
collection = db["test_collection"]

class CSVHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = 0

    def on_modified(self, event):
        if event.src_path.endswith("data.csv"):
            now = time.time()
            # Ignore events within 1 second of each other
            if now - self.last_modified < 1:
                return
            self.last_modified = now
            print(f"{CSV_PATH} changed, reading...")
            data = pd.read_csv(CSV_PATH)
            self.add_row_to_db(data)

    def add_row_to_db(self, data):
        if not data.empty:
            last_row = data.iloc[-1]
            # Replace 'row_id' with your unique column name
            if not collection.find_one({"row_id": int(last_row["row_id"])}):
                collection.insert_one({**last_row.to_dict(), "row_id": int(last_row["row_id"])})
                print("Last row added to database.")
            else:
                print("Last row already exists in database.")

if __name__ == "__main__":
    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, path=FOLDER_PATH, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()