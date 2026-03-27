# Which vegetables had the highest yield in the Netherlands over the past five years?

## Summary
This project analyzes CBS Open Data to identify which vegetables had the highest yield in the Netherlands between 2020 and 2024. Yield was calculated as harvest produced divided by cultivation area and expressed in ton per hectare (ton/ha). The analysis shows that champignons had by far the highest yield among Dutch vegetables in this period, but their yield declined over time, while the other top-yield vegetables remained much lower and relatively stable. This suggests that the most productive crop is not necessarily the most stable over time.

## Data source
The data comes from CBS Open Data, dataset 37738:  
https://opendata.cbs.nl/#/CBS/nl/dataset/37738/table

The dataset was accessed programmatically in Python using the `cbsodata` package.
https://pypi.org/project/cbsodata/

## Method
1. Load the CBS dataset in Python using `cbsodata`
2. Rename relevant columns for clarity
3. Filter the dataset to the years 2020–2024
4. Convert harvest and cultivation area columns to numeric values
5. Compute yield as:

   `ton/ha = (Harvest (mln kg) * 1000) / Cultivation area (hectare)`

6. Rank vegetables by their average yield across 2020–2024
7. Select the four vegetables with the highest average yield
8. Visualize their yield trends using a broken y-axis plot to preserve readability despite the large difference between champignons and the other vegetables

## Repository structure
- `main.py` — main analysis and plotting script
- `requirements.txt` — required Python packages
- `README.md` — project description and instructions
- `Figure_vegetables.png` — exported figure used in the submission

## Setup
Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## How to run
Run the script with:

```bash
python3 main.py
```

## Output
The script generates and displays a figure titled:

**Highest-yield vegetables in the Netherlands (2020–2024)**

It also saves the figure as:

`Figure_vegetables.png`

## Notes / limitations
- The analysis focuses only on the years 2020–2024.
- Vegetables were ranked based on average yield over this period.
- Yield per hectare is useful for comparing productivity, but it does not capture other factors such as value produced and resources consumed.