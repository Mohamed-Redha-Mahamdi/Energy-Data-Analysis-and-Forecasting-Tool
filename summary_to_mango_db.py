import pandas as pd
import os
import pymongo

# Get the list of all files in directory
dir_path = "/path/to/retrieved-data/"
list_of_files = os.listdir(dir_path)

# Get the most recent file
latest_file = max(list_of_files, key=lambda x: os.path.getmtime(dir_path + x))

# Load the JSON file into a pandas dataframe
df = pd.read_json(dir_path + latest_file)

# Extract the dictionaries in the 'history' column into a new dataframe
df_history = pd.json_normalize(df["history"])

# Select the required columns
df_selected = df_history[
    [
        "datetime",
        "powerConsumptionTotal",
        "powerProductionTotal",
        "powerImportTotal",
        "powerExportTotal",
        "powerConsumptionBreakdown.nuclear",
        "powerConsumptionBreakdown.geothermal",
        "powerConsumptionBreakdown.wind",
        "powerConsumptionBreakdown.gas",
        "powerConsumptionBreakdown.oil",
        "powerConsumptionBreakdown.solar",
    ]
]

df_sorted = df_selected.sort_values("datetime", ascending=False)

# Create a connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Create a database called "mydatabase"
mydb = client["your_database"]

# Create a collection
mycollection = mydb["your_collection"]

# Drop the collection if it exists
#mydb.drop_collection("energy")

# Create the collection again
#mycollection = mydb["energy"]

# Convert your DataFrame to a list of dictionaries for insertion into MongoDB
data_dict = df_sorted.to_dict("records")

# Insert the list of dictionaries into the collection
mycollection.insert_many(data_dict, ordered=False)
