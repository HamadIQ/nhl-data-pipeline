import os
import pandas as pd

def compress_file(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Error: taget file {input_path} not found")
    
    df = pd.read_csv(input_path)

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True) 

    print("Compressing CSV file ...")
    # Convert input csv file to Parquet
    df.to_parquet(output_path, compression="snappy", index=False)

if __name__ == "__main__":
    input = "data/processed/nhl_yearly_goals_vs_xgf.csv"
    output = "data/compressed/nhl_yearly_goals_vs_xgf.parquet"
    compress_file(input, output)