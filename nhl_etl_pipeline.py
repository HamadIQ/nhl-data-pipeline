import os
import pandas as pd
import numpy as np

def run_spatial_etl_pipeline(input_path, output_path):
    """
    Clean NHL shot event data and calculate heuristic expected
    goals estimates.

    Args:
        input_path (str): Path to the shot event data CSV.
        output_path (str): Destination for the processed CSV.
    """
    
    
    print("Starting NHL Spatial ETL Pipeline...")


    # Check that the input file exists before processing
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Error target file '{input_path}' not found")

    # Load shot event data and record the initial row count
    df = pd.read_csv(input_path)
    initial_count = len(df)
    print(f"Loaded {initial_count:,} raw records from storage")

    # Find rows missing shot coordinates or player IDs
    invalid_records_mask = (
        df['shootingPlayerId'].isnull() |
        df['xCoord'].isnull() |
        df['yCoord'].isnull()
    )
    # Remove rows with missing required data
    dropped_corrupt_rows = invalid_records_mask.sum()
    df_clean = df[~invalid_records_mask].copy()
    print("\n Cleaned data preview ---")
    print(df_clean.head())
    print("\n number or rows dropped ---")
    print(dropped_corrupt_rows)

    # Normalize rink coordinates to consistent shooting direction 
    df_clean['norm_x'] = df_clean['xCoord'].abs()
    df_clean['norm_y'] = df_clean['yCoord'].abs()

    # Net coordinates
    NET_X, NET_Y = 89.0, 0.0
    # Distance from net and center of the ice using coordinates x and y
    dx = NET_X - df_clean['norm_x']
    dy = df_clean['norm_y'] - NET_Y

    # Calculate distance from each shot to the net
    df_clean['shot_distance'] = np.sqrt((dx)**2 + (dy)**2)

    # Calculate angle of each shot
    df_clean['shot_angle'] = np.degrees(np.arctan2(dy, dx))

    # Identify shots taken from behind the goal
    behind_goal = df_clean['norm_x'] > NET_X

    # Estimate expected goals using a rule based heuristic
    # Assign higher probabilities to close range shots with favourable angles
    # in the offensive zone, and lower probabilities to distant or
    # behind the net shots. Remaining shots receive the baseline value
    df_clean['xgf'] = 0.05

    # High danger shots: close to the net, favourable angle,
    # and recorded in the offensive zone
    df_clean.loc[(df_clean['shot_distance']< 25) & (df_clean['shot_angle']<30) & (df_clean['zoneCode']=='O') & (~behind_goal), 'xgf'] = 0.22

    # Low danger shots: distant shots with large angles,
    # or shots taken from behind the goal
    df_clean.loc[((df_clean['shot_distance']>55) & (df_clean['shot_angle']>55)) | behind_goal, 'xgf'] = 0.02

    # Save the cleaned shot data and derived expected goals to a CSV
    print("Writing to a csv...")
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    df_clean.to_csv(output_path, index=False)
    # number of rows in df_clean
    final_count = len(df_clean)
    print(f"Success, pipeline completed. {final_count:,} rows\n")
    print(df_clean[['gameId', 'eventType', 'shootingPlayerId', 'shot_distance', 'shot_angle', 'xgf']].head())

if __name__ == "__main__":
    input_file = "data/raw/nhl_shots_data.csv"
    output_file = "data/processed/nhl_expected_goals_clean.csv"
    run_spatial_etl_pipeline(input_file, output_file)
