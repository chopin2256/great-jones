import json
from config import Config
from data import DB
from postgre import PostGre


# The main client code entry point
if __name__ == '__main__':
    with open("sample.json") as f:
        data = json.load(f)  # Load the json as an object
        data = DB.getData(data)  # Flatten the data and get data types

        # Create the table based off of the data structure in "data"
        DB.createTable(data, Config.schema_name, Config.table_name)

        # Create the CSV and prepare for import using the COPY command
        DB.createCSV(data, Config.schema_name, Config.table_name)

        # Take the csv file and ingest into the database
        PostGre.ingestCSV(Config.schema_name, Config.table_name)

        # Sample query in code
        myResults = PostGre.query("Select * from test_schema.test_table")
        print(myResults)
