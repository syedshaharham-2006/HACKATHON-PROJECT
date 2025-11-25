import requests
from bs4 import BeautifulSoup
import boto3
import json
import time

# Initialize S3 client
s3 = boto3.client('s3')

# Your S3 bucket name
bucket_name = 'data-hackathon-smit-syedshaharham'

URL = "https://coinmarketcap.com/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def get_top_10():
    resp = requests.get(URL, headers=headers, timeout=15)
    resp.raise_for_status()

    # Use the default HTML parser instead of lxml
    soup = BeautifulSoup(resp.text, "html.parser")

    # Grab table body
    tbody = soup.select_one("table tbody")
    if tbody is None:
        raise RuntimeError("Could not find coins table. CoinMarketCap changed layout.")

    rows = tbody.select("tr")[:10]

    data = []
    for row in rows:
        cols = row.find_all("td")

        # Extracting the data
        rank = cols[1].get_text(strip=True) if len(cols) > 1 else None
        name = cols[2].get_text(strip=True) if len(cols) > 2 else None
        price = cols[3].get_text(strip=True) if len(cols) > 3 else None
        one_hour_change = cols[4].get_text(strip=True) if len(cols) > 4 else None
        twenty_four_hour_change = cols[5].get_text(strip=True) if len(cols) > 5 else None
        seven_day_change = cols[6].get_text(strip=True) if len(cols) > 6 else None
        market_cap = cols[7].get_text(strip=True) if len(cols) > 7 else None
        hr_volume = cols[8].get_text(strip=True) if len(cols) > 8 else None

        # Append to data list
        data.append({
            "rank": rank,
            "name": name,
            "price": price,
            "one_hour_change": one_hour_change,
            "twenty_four_hour_change": twenty_four_hour_change,
            "seven_day_change": seven_day_change,
            "market_cap": market_cap,
            "hr_volume": hr_volume,
        })

    return data

def save_to_s3(data):
    # Convert data to JSON format
    json_data = json.dumps(data)

    # Generate a unique file name based on current timestamp or any other identifier
    file_name = f"raw/top_10_coins_{int(time.time())}.json"  # Save to 'raw' folder

    # Upload the data to the S3 bucket inside the 'raw' folder
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,  # This includes the folder structure 'raw'
        Body=json_data,
        ContentType='application/json'
    )
    print(f"Data successfully uploaded to S3 bucket {bucket_name} in the 'raw' folder as {file_name}")

# Lambda entry point
def lambda_handler(event, context):
    # Get the top 10 coins
    coins = get_top_10()

    # Save data to S3
    save_to_s3(coins)

    # You can also return the data or a success message if needed
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully fetched and uploaded the data to the "raw" folder.')
    }
