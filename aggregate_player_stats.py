import os
import pandas as pd
import requests
import time

def aggregate_players(player_dict, player_stats, output_path):
    shots_df = pd.read_csv(player_stats)
    print("Shots Dataframe")
    print(shots_df.head(5))
    player_df = pd.read_csv(player_dict)
    # Total number of wrist shots on goal
    shots_df['Wrist_Shot_On_Goal'] = (shots_df['eventType'] == 'shot-on-goal') & (shots_df['shotType'] == 'wrist')
    # Total number of slap shots on goal
    shots_df['Slap_Shot_On_Goal'] = (shots_df['eventType'] == 'shot-on-goal') & (shots_df['shotType'] == 'slap')
    # Total number of snap shots ong goal
    shots_df['Snap_Shot_On_Goal'] = ((shots_df['eventType'] == 'shot-on-goal')) & (shots_df['shotType'] == 'snap') 
    
    # Calculate total expected goals for each player by season
    # Creates a column to store all shots on goal for each player by season total and by type
    grouped_xgf = shots_df.groupby(['shootingPlayerId', 'season']).agg(
        xgf=('xgf', 'sum'),
        Shots_On_Goal=('eventType', lambda x: x.isin(['shot-on-goal', 'goal']).sum()),
        Wrist_Shots_On_Goal_Total=('Wrist_Shot_On_Goal', 'sum'),
        Slap_Shots_On_Goal_Total=('Slap_Shot_On_Goal', 'sum'),
        Snap_Shots_On_Goal_Total=('Snap_Shot_On_Goal', 'sum'),
    ).reset_index() 
    # NHL seasons included in the analysis
    seasons = [
        "20202021", "20212022", "20222023", "20232024", "20242025"
    ]
    # Store the results for each season
    all_seasons_compiled = []
    for season_str in seasons:

        # Request goal totals for the current season for each player
        url =  f"https://api-web.nhle.com/v1/skater-stats-leaders/{season_str}/2?categories=goals&limit=-1"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                raw_json = response.json()
                if "goals" in raw_json:
                    api_goals_df = pd.DataFrame(raw_json["goals"])
                    
                    api_goals_df = api_goals_df[["id", "value"]].rename(
                        columns={'id':'shootingPlayerId', 'value': 'actualGoals'}
                    )
                    api_goals_df['season'] = season_str
                    all_seasons_compiled.append(api_goals_df)
            else:
                print(f"Could not fetch season {season_str} (Status Code: {response.status_code})")
        except Exception as e:
            print(f"Error trying to fetch {season_str}: {e}")

        # Delay to avoid API throttling
        time.sleep(0.4)
    # Stop if no season data was retrieved
    if not all_seasons_compiled:
        raise RuntimeError("No NHL goal data could be retrieved")
    # Combine the goal totals from all seasons   
    master_api_goals = pd.concat(all_seasons_compiled, ignore_index=True)
    # Set the season type as a str
    grouped_xgf['season'] = grouped_xgf['season'].astype(str)
    master_api_goals['season'] = master_api_goals['season'].astype(str)

    # Merge the goals per player per season and the grouped expected goals table on the players id and the season
    # Fill empty goal values with 0
    integrated_df = pd.merge(grouped_xgf, master_api_goals, on=['shootingPlayerId', 'season'], how="left")
    integrated_df['actualGoals'] = integrated_df['actualGoals'].fillna(0).astype(int)
    # Add player names to the results
    final_df = pd.merge(integrated_df, player_df, left_on="shootingPlayerId", right_on="shootingPlayerId", how="inner")
    # Compare actual goals with expected goals
    final_df['goals_minus_xgf'] = final_df['actualGoals'] - final_df['xgf']
    # Group by season and actualGoals
    final_df = final_df.sort_values(by=['season', 'actualGoals'], ascending=[True, False])
    # Creates an output csv with transformed data
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    final_df.to_csv(output_path, index=False)

    print("Expected Goals by player---")
    print(final_df.head())
if __name__ == "__main__":
    player_dictionary = "data/raw/nhl_player_dictionary.csv"
    nhl_shots = "data/processed/nhl_expected_goals_clean.csv"
    target_storage_path = "data/processed/nhl_yearly_goals_vs_xgf.csv"
    aggregate_players(player_dictionary, nhl_shots, target_storage_path)