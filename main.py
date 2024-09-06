from app import create_app
from app.calculations import load_and_calculate_data
from app.db import store_data_in_sqlite

app = create_app()


if __name__ == '__main__':
    
    excel_file = "data/20210309_2020_1 - 4.xls"
    annual_data = load_and_calculate_data(excel_file)
    print("annual_data",annual_data)
    
    store_data_in_sqlite(annual_data)
    
    app.run(debug=True,port=8080)




