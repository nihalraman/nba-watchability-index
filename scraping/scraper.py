import os
from typing import List
import json
import csv
import requests
import pandas as pd
import re
import time
from bs4 import BeautifulSoup
from pathlib import Path
import boto3
from string import ascii_lowercase

# Constants
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
S3_BUCKET_NAME = "nba-game-logs"
S3_INDEX_FILE = "metadata.json"
LOCAL_INDEX_FILE = "metadata_local.json"

s3 = boto3.client("s3")


def fetch_player_links() -> List[str]:
    base_url = "https://www.basketball-reference.com/players/"
    player_urls = []

    for c in ascii_lowercase:
        letter_url = base_url + c + "/"
        time.sleep(4)
        response = requests.get(letter_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        players = soup.select('th[data-stat="player"]')
        for player in players:
            raw_link = str(player.find_all('a', href=True)).split("\">")[0][11:]
            link = "https://www.basketball-reference.com/" + raw_link
            player_urls.append(link)
    
    return player_urls


def get_gamelog_links():
    player_urls = []
    with open('player_urls.txt', 'r') as f:
        player_urls = [line.strip() for line in f]

    gamelog_urls = set()
    checkpoint_file = "checkpoint.txt"
    gamelog_file = "gamelog_links.csv"
    start_index = 0
    if Path(checkpoint_file).is_file():
        with open(checkpoint_file, 'r') as f:
            start_index = int(f.read().strip())

    print(f"Resuming from player index {start_index}")

    for i in range(start_index, len(player_urls)):
        url = player_urls[i]
        time.sleep(3)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        target_tag = soup.find('strong', string='Game Logs')
        if target_tag:
            base_link = "https://www.basketball-reference.com"
            for link in target_tag.find_all_next('a'):
                if link.get('href') and '/gamelog/' in link.get('href'):
                    gamelog_urls.add(base_link + link.get('href').rstrip('/'))

        if (i + 1) % 10 == 0 or i == len(player_urls) - 1:
            with open(gamelog_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for gamelog_link in gamelog_urls:
                    writer.writerow([gamelog_link])
            gamelog_urls.clear()
            with open(checkpoint_file, 'w') as f:
                f.write(str(i + 1))
            print(f"Saved progress at index {i + 1}")

    print("Game log links extraction completed.")


def extract_gamelog_stats(gamelog_url):
    time.sleep(5)
    response = requests.get(gamelog_url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", id="pgl_basic")
    if not table:
        print(f"No game log table found at {gamelog_url}")
        return pd.DataFrame()
    match = re.search(r"players/./(\w+)/gamelog/", gamelog_url)
    player_id = match.group(1) if match else "Unknown"
    headers = [th.text.strip() for th in table.find("thead").find_all("tr")[-1].find_all("th")][1:]
    rows = []
    for tr in table.find_all("tr")[1:]:
        cols = [td.text.strip() for td in tr.find_all("td")]
        if cols:
            row_data = dict(zip(headers, cols))
            row_data["Player"] = player_id
            rows.append(row_data)
    return pd.DataFrame(rows)


def upload_to_s3(df, player_id):
    if df.empty:
        return
    file_path = f"gamelogs/{player_id}.parquet"
    df.to_parquet("/tmp/temp.parquet", index=False)
    s3.upload_file("/tmp/temp.parquet", S3_BUCKET_NAME, file_path)
    print(f"Uploaded {file_path} to S3.")


def load_index():
    try:
        response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=S3_INDEX_FILE)
        index_data = json.loads(response["Body"].read().decode("utf-8"))
    except:
        index_data = {"processed_logs": [], "last_index": 0}
    with open(LOCAL_INDEX_FILE, "w") as f:
        json.dump(index_data, f)
    return index_data


def save_index(index_data):
    with open(LOCAL_INDEX_FILE, "w") as f:
        json.dump(index_data, f)
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=S3_INDEX_FILE,
        Body=json.dumps(index_data)
    )


def process_all_gamelogs():
    gamelog_file = "gamelog_links.csv"
    if not Path(gamelog_file).is_file():
        print("No game log links file found. Generating...")
        get_gamelog_links()

    index_data = load_index()
    processed_logs = set(index_data["processed_logs"])
    start_index = index_data["last_index"]

    with open(gamelog_file, 'r') as f:
        gamelog_links = [line.strip() for line in f]

    print(f"Resuming from game log index {start_index}")

    for i in range(start_index, len(gamelog_links)):
        gamelog_url = gamelog_links[i]
        match = re.search(r"players/./(\w+)/gamelog/", gamelog_url)
        player_id = match.group(1) if match else None
        if not player_id or player_id in processed_logs:
            continue
        df = extract_gamelog_stats(gamelog_url)
        if not df.empty:
            upload_to_s3(df, player_id)

        if (i + 1) % 10 == 0 or i == len(gamelog_links) - 1:
            index_data["processed_logs"].append(player_id)
            index_data["last_index"] = i + 1
            save_index(index_data)
            print(f"Saved progress at index {i + 1}")

    print("Game log extraction and upload completed.")


def main():
    if not Path("player_urls.txt").is_file():
        print("Fetching player URLs...")
        player_links = fetch_player_links()
        with open('player_urls.txt', 'w') as f:
            for link in player_links:
                f.write(f"{link}\n")
    else:
        print("Using cached player_urls.txt")

    if not Path("gamelog_links.csv").is_file():
        print("Fetching game log links...")
        get_gamelog_links()
    else:
        print("Using cached gamelog_links.csv")

    process_all_gamelogs()


if __name__ == "__main__":
    main()

