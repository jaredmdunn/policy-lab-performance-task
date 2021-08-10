import pandas as pd

# initial dataframes
census_codebook = pd.read_csv("data/census_codebook.csv")
pop_by_block = pd.read_csv("data/population_by_blockgroup.csv")
dist_school_to_block = pd.read_csv(
    "data/distance_from_school_to_blockgroup_in_miles.csv"
)

# Question 1: How many people live in Boston?
pop_by_block_boston = pop_by_block[pop_by_block["city"] == "Boston"]
code_total = census_codebook.loc[census_codebook["sex"] == "total", "variable_name"][0]

pop_boston = pop_by_block_boston[code_total].sum()

# Question 2: How many people who are at least 65 years old live in Boston?
codes_65_plus = census_codebook.loc[
    census_codebook["min_age"] >= 65, "variable_name"
].to_numpy()

pop_by_block_boston["65_plus"] = pop_by_block_boston[codes_65_plus].sum(axis=1)

pop_boston_65_plus = pop_by_block_boston["65_plus"].sum()

# Question 3: How many people who are at least 65 years old live within
# one mile of Fenway High School in Boston?
geo_codes = dist_school_to_block.loc[
    (dist_school_to_block["school_name"] == "Fenway High School")
    & (dist_school_to_block["distance"] <= 1),
    "GEOID10",
].to_numpy()

pop_boston_65_plus_one_mile_to_fenway = pop_by_block_boston.loc[
    pop_by_block["GEOID10"].isin(geo_codes), "65_plus"
].sum()

# Question 4: What is the mean distance a resident of Boston who is
# at least 65 years old lives from their nearest school?
