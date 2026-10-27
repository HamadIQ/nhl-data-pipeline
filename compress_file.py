import os
import pandas as pd

def compress_file(input_path, output_path_parquet, output_path_csv):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Error: target file {input_path} not found")
    
    df = pd.read_csv(input_path)

    # Adjust Column Order
    col_order = ["season", "player_name", "actualGoals", "xgf", "goals_minus_xgf"]
    df_reordered = df[col_order]

    # Map the columns to more clear names
    column_mapping = {
        "season": "Season",
        "player_name": "Player Name",
        "actualGoals": "Actual Goals",
        "xgf": "XGF",
        "goals_minus_xgf": "Goals Minus XGF"
    }

    # Final clean dataframe
    df_final = df_reordered.rename(columns=column_mapping)
    # Compressed parquet
    output_dir_parquet = os.path.dirname(output_path_parquet)
    if output_dir_parquet:
        os.makedirs(output_dir_parquet, exist_ok=True)
    # Compressed csv
    output_dir_csv = os.path.dirname(output_path_csv)
    if output_dir_csv:
        os.makedirs(output_dir_csv, exist_ok=True)  

    print("Compressing CSV file ...")
    # Convert input csv file to Parquet
    df_final.to_parquet(output_path_parquet, compression="snappy", index=False)
    # Drop the column shootingPlayerId
    # Export to a csv
    df_final.to_csv(output_path_csv, index=False, float_format='%.2f')
if __name__ == "__main__":
    input_file = "data/processed/nhl_yearly_goals_vs_xgf.csv"
    output_parquet = "data/compressed/nhl_yearly_goals_vs_xgf.parquet"
    output_csv = "data/compressed/nhl_yearly_goals_vs_xgf_preview.csv"
    compress_file(input_file, output_parquet, output_csv) 