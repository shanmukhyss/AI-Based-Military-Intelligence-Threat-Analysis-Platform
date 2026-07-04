from utils.data_loader import load_data
import plotly.express as px
import plotly.figure_factory as ff

# Load Dataset
df = load_data()

# Remove Unknown Terrorist Groups
known_groups = df[df["gname"] != "Unknown"]

print("=" * 80)
print("GENERATING EDA VISUALIZATIONS...")
print("=" * 80)

# =============================================================================
# 1. Global Terrorist Attacks Per Year
# =============================================================================
yearly = (
    df.groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)

fig = px.line(
    yearly,
    x="iyear",
    y="Attacks",
    markers=True,
    title="Global Terrorist Attacks Per Year"
)

fig.show()

# =============================================================================
# 2. Top 10 Most Affected Countries
# =============================================================================
country = (
    df["country_txt"]
    .value_counts()
    .head(10)
    .reset_index()
)

country.columns = ["Country", "Attacks"]

fig = px.bar(
    country,
    x="Country",
    y="Attacks",
    text="Attacks",
    title="Top 10 Most Affected Countries"
)

fig.show()

# =============================================================================
# 3. Attack Distribution by Region
# =============================================================================
region = (
    df["region_txt"]
    .value_counts()
    .reset_index()
)

region.columns = ["Region", "Attacks"]

fig = px.pie(
    region,
    names="Region",
    values="Attacks",
    title="Attack Distribution by Region"
)

fig.show()

# =============================================================================
# 4. Attack Type Distribution
# =============================================================================
attack = (
    df["attacktype1_txt"]
    .value_counts()
    .reset_index()
)

attack.columns = ["Attack Type", "Count"]

fig = px.bar(
    attack,
    x="Attack Type",
    y="Count",
    text="Count",
    title="Attack Type Distribution"
)

fig.show()

# =============================================================================
# 5. Top Weapon Types
# =============================================================================
weapon = (
    df["weaptype1_txt"]
    .value_counts()
    .head(10)
    .reset_index()
)

weapon.columns = ["Weapon Type", "Count"]

fig = px.bar(
    weapon,
    x="Weapon Type",
    y="Count",
    text="Count",
    title="Top Weapon Types Used"
)

fig.show()

# =============================================================================
# 6. Top Terrorist Groups (Unknown Removed)
# =============================================================================
groups = (
    known_groups["gname"]
    .value_counts()
    .head(15)
    .reset_index()
)

groups.columns = ["Group", "Attacks"]

fig = px.bar(
    groups,
    x="Group",
    y="Attacks",
    text="Attacks",
    title="Top Terrorist Organizations"
)

fig.show()

# =============================================================================
# 7. Success vs Failure
# =============================================================================
success = (
    df["success"]
    .value_counts()
    .reset_index()
)

success.columns = ["Success", "Count"]

success["Success"] = success["Success"].replace({
    0: "Failed",
    1: "Successful"
})

fig = px.pie(
    success,
    names="Success",
    values="Count",
    title="Attack Success Rate"
)

fig.show()

# =============================================================================
# 8. Countries with Highest Fatalities
# =============================================================================
deaths = (
    df.groupby("country_txt")["nkill"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    deaths,
    x="country_txt",
    y="nkill",
    text="nkill",
    title="Top Countries by Fatalities"
)

fig.show()

# =============================================================================
# 9. Global Terrorism Map
# =============================================================================
sample = df.sample(5000, random_state=42)

fig = px.scatter_geo(
    sample,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="country_txt",
    hover_data=[
        "city",
        "gname",
        "nkill"
    ],
    title="Global Terrorism Incidents"
)

fig.show()

# =============================================================================
# 10. Correlation Matrix
# =============================================================================
corr = df[
    [
        "nkill",
        "nwound",
        "success",
        "property"
    ]
].corr()

fig = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=corr.round(2).values,
    showscale=True
)

fig.update_layout(
    title="Correlation Matrix"
)

fig.show()

# =============================================================================
# 11. Most Targeted Categories
# =============================================================================
target = (
    df["targtype1_txt"]
    .value_counts()
    .head(10)
    .reset_index()
)

target.columns = ["Target Type", "Count"]

fig = px.bar(
    target,
    x="Target Type",
    y="Count",
    text="Count",
    title="Top Target Categories"
)

fig.show()

# =============================================================================
# 12. Monthly Attack Trend
# =============================================================================
monthly = (
    df.groupby("imonth")
    .size()
    .reset_index(name="Attacks")
)

fig = px.line(
    monthly,
    x="imonth",
    y="Attacks",
    markers=True,
    title="Monthly Terrorist Attacks"
)

fig.show()

print("=" * 80)
print("EDA VISUALIZATION COMPLETED")
print("=" * 80)