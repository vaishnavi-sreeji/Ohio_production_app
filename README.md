# Ohio_production_app
This Ohio_Production_app is a Flask-based API to provide annual production data for oil, gas, and brine from wells in Ohio. The data is processed from quarterly data available in Excel format.

## Features

- Download and process quarterly production data
- Store processed data in a SQLite database using sqlit3
- Provide API endpoints to query annual production data
  

## Setup

1. Clone the repository:
    ```
    git clone https://github.com/vaishnavi-sreeji/Ohio_production_app.git
    cd Ohio_production_app
    ```

2. Create and activate a virtual environment:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Run the application:
    ```
    python main.py
    ```


## API Documentation

The API provides the following endpoint:

- `GET /api/data?well=<WELL_NUMBER>`: Returns the annual production data for the specified well number.
