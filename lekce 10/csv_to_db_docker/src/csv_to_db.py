import os
import time
import pandas as pd
from pymongo import MongoClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CSV_PATH = os.environ.get("CSV_PATH", "/app/data/data.csv")
# CSV_PATH = r"C:\Python_Projects\robot_dream_skoleni\lekce 10\data\data.csv"

if __name__ == "__main__":
    client = MongoClient("mongodb://mongo:27017/")
    # client = MongoClient("mongodb://localhost:27017/")
    db = client["test_database"]
    collection = db["test_collection"]

    client.admin.command('ping')
    print("Connected to MongoDB successfully!")

    while True:
        print("Checking for new data...")
        data = pd.read_csv(CSV_PATH)
        if not data.empty:
            # last row in db
            last_row_in_db = collection.find_one(sort=[("row_id", -1)])["row_id"] if collection.count_documents({}) > 0 else -1
            # add all rows after last row in db
            data = data[pd.to_numeric(data["row_id"], errors="coerce").notnull()]
            data["row_id"] = data["row_id"].astype(int)
            new_rows = data[data["row_id"] > last_row_in_db]
            if not new_rows.empty:
                collection.insert_many(new_rows.to_dict("records"))
                print(f"Inserted {len(new_rows)} new rows into MongoDB.")
        else:
            print("No data found in CSV.")
        time.sleep(5)