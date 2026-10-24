import os
import requests
import pandas as pd

def ingest_nhl_player_dictionary(output_csv_path):
    # Get player IDs and names from the NHL API 
    url = "https://search.d3.nhle.com/api/v1/search/player?culture=en-us&limit=50000&q=*"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            raw_json = response.json()
            # Extract each player's ID and name
            parsed_players = []
            for item in raw_json:
                parsed_players.append ({
                    'shootingPlayerId': int(item.get('playerId')),
                    'player_name': item.get('name')
                })
            # Converth the parsed players into a data frame
            # and store the results in an output csv
            df_players = pd.DataFrame(parsed_players)
            output_dir = os.path.dirname(output_csv_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            df_players.to_csv(output_csv_path, index=False)
            print(f"Success. number of rows of players mathched to id {len(df_players)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_storage_path = "data/raw/nhl_player_dictionary.csv"
    ingest_nhl_player_dictionary(target_storage_path)