@echo off

set /p CSV_PATH=Enter absolute path to your CSV file (e.g. C:\path\to\data.csv):

REM Extract folder from file path for mounting
for %%F in ("%CSV_PATH%") do (
    set "DATA_DIR=%%~dpF"
    set "FILE_NAME=%%~nxF"
)

REM Remove trailing backslash
if "%DATA_DIR:~-1%"=="\" set "DATA_DIR=%DATA_DIR:~0,-1%"

echo Starting the network...
docker network create mynetwork
echo Starting MongoDB container...
docker run -d --name mongo --network mynetwork -p 27017:27017 mongo:latest
echo Starting CSV to DB container...
docker run -d --rm --network mynetwork --name hw_csv_to_db --mount type=bind,src="%DATA_DIR%",dst=/app/data -e CSV_PATH="/app/data/%FILE_NAME%" csv_to_db:latest
echo Starting DB to REST API container...
docker run --rm -d --network mynetwork --name hw_db_to_api -p 8000:8000 db_rest_api:latest

echo.
echo ================================================================
echo Pipeline is running. Access the API at http://localhost:8000
echo ================================================================
echo.
pause
