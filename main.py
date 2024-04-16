import requests
import time
from datetime import datetime, timedelta
import json

# Constants
API_KEY = 'CkVrpUVgOQdeTxMcHuHHvlsQQqJaghzD'
BASE_URL = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data'
HEADERS = {'token': API_KEY}
DATASET_ID = 'GHCND'  # Global Historical Climatology Network - Daily
DATA_TYPES = ['TMAX', 'TMIN', 'PRCP', 'SNWD']  # Modify as needed
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 1, 2)  # Example: querying one day
RATE_LIMIT = 5  # Requests per second
DAILY_LIMIT = 10000  # Adjust based on actual limits and needs
RETRY_LIMIT = 5  # Maximum number of retries per request
RETRY_BACKOFF = 5  # Seconds to wait between retries

def make_api_request(start_date, end_date, offset=1):
    """Makes a single API request and handles rate limiting and retries."""
    params = {
        'datasetid': DATASET_ID,
        'locationid': 'FIPS:US',
        'startdate': start_date.strftime('%Y-%m-%d'),
        'enddate': end_date.strftime('%Y-%m-%d'),
        'limit': 1000,
        'offset': offset,
        'units': 'standard',
        'datatypeid': ','.join(DATA_TYPES)
    }
    for attempt in range(RETRY_LIMIT):
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            print(f"Successful request for offset {offset}")
            return response.json()
        elif response.status_code == 503:
            print("Service unavailable. Retrying...")
            time.sleep(RETRY_BACKOFF)
        else:
            print(f"Failed with status code {response.status_code}")
            return None
    print("Max retries reached. Moving to next request.")
    return None

def fetch_daily_summaries(start_date, end_date):
    """Fetches daily summaries for all stations within the specified date range."""
    results = []
    request_count = 0
    current_date = start_date

    while current_date <= end_date and request_count < DAILY_LIMIT:
        offset = 1
        while True:
            data = make_api_request(current_date, current_date, offset)
            if data and data.get('results'):
                results.extend(data['results'])
                request_count += 1
                if request_count % RATE_LIMIT == 0:
                    time.sleep(1)  # Respect rate limit
                if len(data['results']) < 1000:
                    break  # No more data for this day
                offset += 1000
            else:
                break
        current_date += timedelta(days=1)
        if request_count >= DAILY_LIMIT:
            print("Reached daily API request limit. Stopping.")
            break

    return results

def save_data_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    print("x")

if __name__ == "__main__":
    main()