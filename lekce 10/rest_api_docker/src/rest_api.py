from pymongo import MongoClient
from flask import Flask, request, jsonify

# Create Flask application instance
app = Flask(__name__)

# Server configuration
HOST = "localhost"
PORT = 8000

@app.route("/", methods=["GET"])
def index():
    """
    Lists available API endpoints.
    """
    commands = {
        "GET /column/column_name": "Get all values for a column with row_id.",
        "GET /full_db": "Get all records in the database.",
        "GET /available_columns": "Get list of available column names in the database."
    }
    return jsonify(commands), 200

@app.route("/column/<column_name>", methods=["GET"])
def get_data_from_db(column_name):
    """
    Returns a list of dicts with row_id and the requested sensor value.
    Example response: [{"row_id": 0, "sensor_1": 22.7}, ...]
    """
    cursor = collection.find({}, {"row_id": 1, column_name: 1, "_id": 0})
    results = [
        {"row_id": doc["row_id"], column_name: doc[column_name]}
        for doc in cursor if column_name in doc and "row_id" in doc
    ]
    if results:
        return jsonify(results), 200
    return "Not Found", 404

@app.route("/full_db", methods=["GET"])
def get_full_db():
    """
    Handle GET requests - retrieve full database content.

    URL pattern: /full_db
    Example: GET /full_db

    Returns:
        - 200: JSON data of all records
    """
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data), 200

@app.route("/available_columns", methods=["GET"])
def get_available_columns():
    """
    Handle GET requests - retrieve list of available column names.

    URL pattern: /available_columns
    Example: GET /available_columns

    Returns:
        - 200: JSON data of column names
    """
    sample_doc = collection.find_one({}, {"_id": 0})
    if sample_doc:
        columns = list(sample_doc.keys())
        return jsonify(columns), 200
    return "No data available", 404


if __name__ == "__main__":
    client = MongoClient("mongodb://mongo:27017/")
    # client = MongoClient("mongodb://localhost:27017/") # testing locally
    db = client["test_database"]
    collection = db["test_collection"]

    client.admin.command('ping')
    print("Connected to MongoDB successfully!")

    # Run Flask application
    app.run(host="0.0.0.0", port=8000, debug=True)