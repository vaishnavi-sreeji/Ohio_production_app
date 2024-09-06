import sqlite3
from collections import OrderedDict

# decoding the values which is in bytes 
def decode_value(value):
    if isinstance(value, bytes):
        try:
            return int.from_bytes(value, byteorder='little')
        except ValueError:
            return 0
    return value

#This function gets the annual data
def get_annual_data(well_number):
    conn = sqlite3.connect('production_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT oil, gas, brine FROM annual_production WHERE api_well_number = ?
    ''', (str(well_number),))
    result = cursor.fetchone()
    conn.close()
    print(result[0])
    

    if result:
        oil = decode_value(result[0])
        print("oil",oil)
        gas = decode_value(result[1])
        brine = decode_value(result[2])

       

        return OrderedDict([
            ("oil", oil),
            ("gas", gas),
            ("brine", brine)
        ])
    return None





# Insert data into SQLite database
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

