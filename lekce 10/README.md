# CSV to MongoDB to REST API Pipeline

This project demonstrates a data pipeline that:
1. Reads sensor data from a CSV file.
2. Loads new rows into a MongoDB database.
3. Exposes the data via a REST API using Flask.

## Project Structure

- `csv_to_db_docker/`: Reads CSV and loads new data into MongoDB.
- `rest_api_docker/`: Flask REST API to access MongoDB data.
- `data/`: Example CSV data.
- `run_pipeline.bat`: Batch script to run the pipeline using Docker.

## Usage

1. **Prepare your CSV file**  
   Place your CSV file in a folder (see `data/data.csv` for an example).
   File must have a header row with column names and a `row_id` column for unique identification.
   New rows will be appended based on ascending `row_id`.
   It is possible to add new columns, but existing columns should not be removed.

2. **Run the pipeline**  
   Run the `run_pipeline.bat` file.
   Enter the absolute path to your CSV file when prompted.

3. **Access the API**  
   Once running, open http://localhost:8000 in your browser to see available API commands.

## API Endpoints

- `GET /` — List available API endpoints.
- `GET /column/<column_name>` — Get all values for a column with `row_id`.
- `GET /full_db` — Get all records in the database.
- `GET /available_columns` — List available column names.