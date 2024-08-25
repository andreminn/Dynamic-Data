import pandas as pd

# Original data as a list of dictionaries
data = [
    {"Company": "Adidas AG", "Ticker": "ADS"},
    {"Company": "Allianz SE", "Ticker": "ALV"},
    {"Company": "BASF SE", "Ticker": "BAS"},
    {"Company": "Bayer AG", "Ticker": "BAYN"},
    {"Company": "Beiersdorf AG", "Ticker": "BEI"},
    {"Company": "BMW AG", "Ticker": "BMW"},
    {"Company": "Brenntag SE", "Ticker": "BNR"},
    {"Company": "Continental AG", "Ticker": "CON"},
    {"Company": "Covestro AG", "Ticker": "1COV"},
    {"Company": "Deutsche Telekom AG", "Ticker": "DTE"},
    {"Company": "Deutsche Post AG", "Ticker": "DPWA.F"},
    {"Company": "Deutsche Börse AG", "Ticker": "DB1"},
    {"Company": "Siemens Energy AG", "Ticker": "ENR"},
    {"Company": "E.ON SE", "Ticker": "EOAN"},
    {"Company": "Fresenius Medical Care AG & Co. KGaA", "Ticker": "FME"},
    {"Company": "Fresenius SE & Co. KGaA", "Ticker": "FRE"},
    {"Company": "Henkel AG & Co. KGaA", "Ticker": "HEN3"},
    {"Company": "Heidelberg Materials AG", "Ticker": "HEI"},
    {"Company": "Hannover Rück SE", "Ticker": "HNR1"},
    {"Company": "Infineon Technologies AG", "Ticker": "IFX"},
    {"Company": "Linde PLC", "Ticker": "LIN"},
    {"Company": "Merck KGaA", "Ticker": "MRK"},
    {"Company": "MTU Aero Engines AG", "Ticker": "MTX"},
    {"Company": "Munich Re AG", "Ticker": "MUV2"},
    {"Company": "Porsche Automobil Holding SE", "Ticker": "PAH3"},
    {"Company": "Puma SE", "Ticker": "PUM"},
    {"Company": "Qiagen N.V.", "Ticker": "QIA"},
    {"Company": "RWE AG", "Ticker": "RWE"},
    {"Company": "SAP SE", "Ticker": "SAP"},
    {"Company": "Siemens AG", "Ticker": "SIE"},
    {"Company": "Sartorius AG", "Ticker": "SRT3"},
    {"Company": "Symrise AG", "Ticker": "SY1"},
    {"Company": "Vonovia SE", "Ticker": "VNA"},
    {"Company": "Volkswagen AG", "Ticker": "VOW3"},
    {"Company": "Zalando SE", "Ticker": "ZAL"},
    {"Company": "Airbus SE", "Ticker": "AIR"},
    {"Company": "Daimler Truck Holding AG", "Ticker": "DTG"},
    {"Company": "Porsche AG", "Ticker": "P91A.SG"},
    {"Company": "Mercedes-Benz Group AG", "Ticker": "MBG"},
    {"Company": "Rheinmetall AG", "Ticker": "RHM"}
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to add ".DE" except for the exceptions, including quotation marks
def format_ticker(ticker):
    if ticker not in ["DPWA.F", "P91A.SG"]:
        return f"{ticker}.DE"
    else:
        return ticker

# Apply the function
df['Ticker'] = df['Ticker'].apply(format_ticker)

# Save the updated DataFrame to a CSV file with quotation marks
updated_file_path = "DAX40_2024_formatted_exceptions_with_quotes.csv"
df.to_csv(updated_file_path, index=False, quoting=1)

print("CSV file updated and saved!")
