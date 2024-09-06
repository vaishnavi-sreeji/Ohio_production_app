# main.py
from flask import Flask, request,Response
import pandas as pd
import sqlite3
from collections import OrderedDict
import ujson

app = Flask(__name__)


# Load Excel file and calculate annual production data
def load_and_calculate_data(excel_file):
    data = pd.read_excel(excel_file, sheet_name='Sheet1')
    
    # Group by API WELL NUMBER and calculate sum for oil, gas, brine
    annual_data = data.groupby('API WELL  NUMBER').agg({
        'OIL': 'sum',
        'GAS': 'sum',
        'BRINE': 'sum'
    }).reset_index()
    
    return annual_data

# Store data in SQLite database
def store_data_in_sqlite(data):
    conn = sqlite3.connect('production_data.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS annual_production (
        api_well_number TEXT PRIMARY KEY,
        oil INTEGER,
        gas INTEGER,
        brine INTEGER
    )
    ''')
    
    # Insert data
    for _, row in data.iterrows():
        cursor.execute('''
        INSERT OR REPLACE INTO annual_production (api_well_number, oil, gas, brine)
        VALUES (?, ?, ?, ?)
        ''', (str(row['API WELL  NUMBER']), row['OIL'], row['GAS'], row['BRINE']))
    
    conn.commit()
    conn.close()

# Retrieve annual data for a well number
def get_annual_data(well_number):
    conn = sqlite3.connect('production_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT oil, gas, brine FROM annual_production WHERE api_well_number = ?
    ''', (str(well_number),))
    result = cursor.fetchone()
    conn.close()

    if result:
        oil, gas, brine = map(decode_value, result)
        return OrderedDict([("oil", oil), ("gas", gas), ("brine", brine)])
    return None

# Helper to decode bytes to int
def decode_value(value):
    if isinstance(value, bytes):
        try:
            return int.from_bytes(value, byteorder='little')
        except ValueError:
            return 0
    return value

# # API route to get data for a well number
# @app.route('/data', methods=['GET'])
# def get_data():
#     well_number = request.args.get('well')
#     if not well_number:
#         return jsonify({"error": "Well number is required"}), 400
    
#     data = get_annual_data(well_number)
#     if data:
#         return jsonify(data)
#     else:
#         return jsonify({"error": "Well number not found"}), 404
    
@app.route('/data', methods=['GET'])
def get_data():
    well_number = request.args.get('well')
    if not well_number:
        return Response(ujson.dumps({"error": "Well number is required"}), status=400, mimetype='application/json')
    
    data = get_annual_data(well_number)
    if data:
        # Use ujson.dumps to control the order of the keys
        ordered_data = OrderedDict([("oil", data["oil"]), ("gas", data["gas"]), ("brine", data["brine"])])
        return Response(ujson.dumps(ordered_data), mimetype='application/json')
    else:
        return Response(ujson.dumps({"error": "Well number not found"}), status=404, mimetype='application/json')

# Test route
@app.route('/', methods=['GET'])
def test():
    return "congratz"

if __name__ == '__main__':
    # Load and calculate annual data from Excel
    excel_file = "20210309_2020_1 - 4.xls"
    annual_data = load_and_calculate_data(excel_file)
    
    # Store data in SQLite
    store_data_in_sqlite(annual_data)
    
    app.run(debug=True, port=8080)
