import pandas as pd

# Load Excel file and calculate annual production data
def load_and_calculate_data(excel_file):
    data = pd.read_excel(excel_file, sheet_name='Sheet1')
    
    # print(df.columns)
    # print(data['API WELL  NUMBER'].head(5))
    
    # Group by API WELL NUMBER and calculate sum for oil, gas, brine
    annual_data = data.groupby('API WELL  NUMBER').agg({
        'OIL': 'sum',
        'GAS': 'sum',
        'BRINE': 'sum'
    }).reset_index()
    # annual_data = data.groupby('API WELL  NUMBER').sum()
    # print("annual",annual_data)
    
    return annual_data



