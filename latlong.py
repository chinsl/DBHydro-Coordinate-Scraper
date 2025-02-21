import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import subprocess

#------------------ LatLong Extraction  ---------------------

# Base URL for station info (Replace {station_id} with actual station ID)
BASE_URL = "https://my.sfwmd.gov/dbhydroplsql/show_dbkey_info.show_station_info?v_station={}"

# List of station IDs to query
stations = [
    'C44SC24', 'C44SC23', 'C44SC19', 'C44SC14', 'C44SC5', 'C44SC2', 'C44S80', 
    'C23S48', 'C24S49', 'SE+01', 'SE+02', 'SE+03', 'SE+06', 'SE+08B', 'SE+09', 'SE+11', 'SE+12', 
    'SE+13', 'S153', 'S404', 'S417E', 'S415E', 'HR1', 'GORDYRD', 'S308C'
]

# Headers to simulate a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_coordinates(station_id, max_retries=3):
    """Fetches latitude and longitude from SFWMD DBHYDRO for a given station."""
    url = BASE_URL.format(station_id)

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()  # Raise an error for failed responses

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract latitude and longitude from the table
            lat_tag = soup.find("td", string="Latitude (ddmmss.sss)")
            lon_tag = soup.find("td", string="Longitude (ddmmss.sss)")

            #iterate through tags
            if lat_tag and lon_tag:
                latitude = lat_tag.find_next_sibling("td").text.strip()
                longitude = lon_tag.find_next_sibling("td").text.strip()
                if(attempt>1):
                    print("Retry successful")
                return latitude, longitude
            else:
                return None, None
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Retry {attempt+1}/{max_retries} for {station_id} due to error: {e}")
            time.sleep(2)  # Wait before retrying
    
    print(f"Skipping {station_id} after {max_retries} failed attempts")
    return None

# Store results
station_data = []

for station in stations:
    print(f"Fetching lat-long data for {station}...")
    lat, lon = fetch_coordinates(station)
    station_data.append({"Station": station, "Latitude (ddmmss)": lat, "Longitude (ddmmss)": lon})
    time.sleep(1)  # Pause to avoid overwhelming the server

# Convert data to DataFrame and display
df = pd.DataFrame(station_data)


#------------ Decimal Conversion --------------

# Function to convert DMS (ddmmss.sss) to decimal degrees
def dms_to_decimal(dms):
    try:
        dms = str(dms).strip()
        degrees = int(dms[:2])  # First 2 characters are degrees
        minutes = int(dms[2:4])  # Next 2 characters are minutes
        seconds = float(dms[4:])  # Remaining characters are seconds

        # Convert to decimal degrees
        decimal = degrees + (minutes / 60) + (seconds / 3600)
        return round(decimal, 6)
    except ValueError:
        return None  # Return None if conversion fails

# Convert latitude and longitude to decimal degrees
df["Latitude (Decimal)"] = df["Latitude (ddmmss)"].apply(dms_to_decimal)
df["Longitude (Decimal)"] = df["Longitude (ddmmss)"].apply(dms_to_decimal)

# Negate longitude
df["Longitude (Decimal)"] = df["Longitude (Decimal)"] * -1

# Save the updated DataFrame
output_file = "/Users/metta/Documents/Research/latlong/latlong_conv_neg.csv"  # path for latlong data 
df.to_csv(output_file, index=False)

# Confirmation message
print(f"\nCoordinate retrieval and conversion complete. Data saved to {output_file}\n")

subprocess.run(["open", output_file]) #open latlong file



