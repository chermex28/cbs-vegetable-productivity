import pandas as pd
import cbsodata
import matplotlib.pyplot as plt

### DATA HANDLING
# Load CBS dataset
datasetid = "37738"
df_raw = pd.DataFrame(cbsodata.get_data(datasetid))

# Create working copy and rename columns
df = df_raw.rename(columns={
    "Groenten": "Vegetables",
    "Perioden": "Period",
    "Oogst_1": "Harvest (mln kg)",
    "Teeltoppervlakte_2": "Cultivation area (hectare)"
}).copy()

# Clean column names
df.columns = df.columns.str.strip()

# Keep only the last 5 years (2020–2024)
df["Period"] = pd.to_numeric(df["Period"], errors="coerce")
df = df[df["Period"].between(2020, 2024)].copy()

# Convert numeric columns and calculate yield (ton/ha)
df["Harvest (mln kg)"] = pd.to_numeric(df["Harvest (mln kg)"], errors="coerce")
df["Cultivation area (hectare)"] = pd.to_numeric(df["Cultivation area (hectare)"], errors="coerce")
df["ton/ha"] = (df["Harvest (mln kg)"] * 1000) / df["Cultivation area (hectare)"]

# Select top vegetables with highest yield
# Choosing 4, as the 5th vegetable is a general category not a specific vegetable
top_vegetables = (
    df.groupby("Vegetables")["ton/ha"]
    .mean()
    .sort_values(ascending=False)
    .head(4)
    .index
    .tolist()
)

df_sorted = df[df["Vegetables"].isin(top_vegetables)].copy()

### VISUALIZATION
# Matplotlib documentation example to create a broken axis plot:
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/broken_axis.html

# Create 2 plots and plotting the same information in both
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6), gridspec_kw={"height_ratios": [2, 1], "hspace": 0.05})

for vegetable in df_sorted["Vegetables"].unique():
    temp = df_sorted[df_sorted["Vegetables"] == vegetable]
    ax1.plot(temp["Period"], temp["ton/ha"], marker="o", label=vegetable)
    ax2.plot(temp["Period"], temp["ton/ha"], marker="o")

# Define y-axis limits for both plots according to data values
ax1.set_ylim(2200, 4500)
ax2.set_ylim(350, 760)

# Remove upper and lower edges to "merge" both plots and adjust ticks
ax1.spines["bottom"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax1.tick_params(axis="x", bottom=False, labelbottom=False)
years = sorted(df_sorted["Period"].unique())
ax2.set_xticks(years)

# Set legend and titles
ax1.set_title("Highest-yield vegetables in the Netherlands (2020–2024)", fontsize=14)
ax1.legend(title="Vegetable", bbox_to_anchor=(1.02, 1), loc="upper left")
ax2.set_xlabel("Year",fontsize=14)

# Set break marks (Matplotlib documentation)
d = 0.5
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)

# Set grid lines
ax1.grid(True, alpha=0.3)
ax2.grid(True, alpha=0.3)

# Set a shared y-axis title
fig.text(0.05,0.5,"Yield (ton/ha)", rotation=90, va="center", ha="center", fontsize=14)

# Saving final figure
plt.savefig("Figure_vegetables.png", dpi=300, bbox_inches="tight")