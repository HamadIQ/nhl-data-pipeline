# NHL Data Engineering Pipeline
## Project Overview
This project builds a Python based data pipeline for NHL shot data and extracts each players expected goals using a heuristic approach. The pipeline transforms and aggregates data for analysis.
## Features
- NHL player data ingestion
- ETL pipeline for data transformation and processing
- Heuristic expected goals estimation
- Player statistics
- Raw and processed data organization
- AWS S3 Bucket Deployment
## Dataset Preview
| Season | Player Name | Actual Goals | XGF | Goals Minus XGF |
| :---: | :---: | :---: | :---: | :---: |
| 20202021 | Auston Matthews | 41 | 25.59 | 15.41 |
| 20202021 | Connor McDavid | 33 | 20.53 | 12.37 |
| 20202021 | Alex DeBricant | 32 | 13.89 | 18.11 |
| 20202021 | Leon Draisaitl | 31 | 15.59 | 15.41 |
| 20202021 | Mikko Rantanen | 30 | 16.62 | 13.38 |

## Project Structure
```text
.
├── aggregate_player_stats.py
├── fetch_players.py
├── nhl_etl_pipeline.py
├── data/
│        ├── compressed/
│        ├── raw/
│        └── processed/
│── .github/
│        └── workflows/
│── nhl-infra/
│        └──nhl_infra/
├── .gitignore
├── README.md
```
## Data Sources & References
- [NHL Clean Shots Data on Kaggle] (https://www.kaggle.com/datasets/samuarg/nhl-clean-shots-data-2020-2021-to-2024-2025)
- [NHL API Reference] (https://github.com/Zmalski/NHL-API-Reference)

The API reference is an unofficial community maintained resource. Refer to the linked documentation for endpoint details.

## Technologies
- Python
- pandas
- numpy
- Data engineering and ETL workflows
- Github Actions
- AWS S3

## Getting Started
Clone the repository:
```bash
git clone https://github.com/HamadIQ/nhl-data-pipeline.git
cd nhl-data-pipeline
```
Create and activate a virtual environment, then install the projects dependencies

Run the pipeline using the appropriate script order
1. fetch_players.py
2. nhl_etl_pipeline.oy
3. aggregate_player_stats.py
4. compress_file.py

## Roadmap
- [ ] Build an interactive dashboard
- [ ] Add visualization and insights from NHL shot data
