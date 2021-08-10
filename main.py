import pandas as pd

census_codebook = pd.read_csv("census_codebook.csv")
code_total = census_codebook.loc[census_codebook["sex"] == "total", "variable_name"][0]
codes_65_plus = census_codebook.loc[
    census_codebook["min_age"] >= 65, "variable_name"
].to_numpy()

pop_by_block = pd.read_csv("population_by_blockgroup.csv")
population_boston = pop_by_block.loc[pop_by_block["city"] == "Boston", code_total].sum()


population_boston_65_plus = 0

for code in codes_65_plus:
    population_boston_65_plus += pop_by_block.loc[
        pop_by_block["city"] == "Boston", code
    ].sum()

dist_school_block = pd.read_csv("distance_from_school_to_blockgroup_in_miles.csv")
geo_codes_one_mile_to_fenway = dist_school_block.loc[
    (dist_school_block["school_name"] == "Fenway High School")
    & (dist_school_block["distance"] <= 1),
    "GEOID10",
].to_numpy()

population_boston_one_mile_to_fenway_65_plus = 0

for geo_code in geo_codes_one_mile_to_fenway:
    geo_code_pop = 0
    for code in codes_65_plus:
        geo_code_pop += pop_by_block.loc[
            (pop_by_block["city"] == "Boston") & (pop_by_block["GEOID10"] == geo_code),
            code,
        ].sum()
    population_boston_one_mile_to_fenway_65_plus += geo_code_pop

pop_by_block_boston = pop_by_block[pop_by_block["city"] == "Boston"]
pop_by_block_boston["65_plus"] = pop_by_block_boston[codes_65_plus].sum(axis=1)

merged = pop_by_block_boston.merge(dist_school_block, on="GEOID10")
pd.set_option("mode.use_inf_as_na", True)
merged.dropna(inplace=True)
merged["distance_times_65_plus"] = merged["distance"] * merged["65_plus"]

print(pop_by_block_boston.head())
print(merged.head())
print(merged.describe())
print(merged["distance_times_65_plus"].sum())

# dist_per_resident_65_plus = 0

# for index, row in pop_by_block_boston.iterrows():
#     geo_code = row["GEOID10"]
#     distance = dist_school_block.loc[
#         dist_school_block["GEOID10"] == geo_code, "distance"
#     ]
#     pop_65_plus = 0
#     for code in codes_65_plus:
#         pop_65_plus += row[code]
#     dist_per_resident_65_plus += distance * pop_65_plus

# mean_dist_65_plus_to_school = dist_per_resident_65_plus / population_boston_65_plus

print("pop boston", population_boston)
print("pop boston 65+", population_boston_65_plus)
print(
    "pop boston 65+ one mile from Fenway High School",
    population_boston_one_mile_to_fenway_65_plus,
)
# print("mean distance 65+ to nearest school", mean_dist_65_plus_to_school)
