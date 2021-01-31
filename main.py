import json
import os
import re
from config import Config
from data import DB
from postgre import PostGre


# The main client code entry point
if __name__ == '__main__':
    schema_name = ""
    table_name = ""

    # Iterate through the json directory
    # Each file will have a file format as "schema_table"
    # Thus, a file named "myschema_table1" will generate a table called "table1" in the "myschema" schema
    # Similarly, a file named "myschema_table2" will generate a table called "table2" in the "myschema" schema
    # This method allows different files to import into different tables
    for filename in os.listdir(Config.jsonDir):
        if filename.endswith(".json"):
            # Break filename into schema and table
            fn = re.sub("\..*", "", filename) # Removing the file extension
            schema_name = fn.split("_")[0]
            table_name = fn.split("_")[1]

            # Opening the file
            with open("{0}/{1}".format(Config.jsonDir, filename)) as f:
                data = json.load(f)  # Load the json as an object
                data = DB.getData(data)  # Flatten the data and get data types

            # Create the table based off of the data structure in "data"
            DB.createTable(data, schema_name, table_name)

            # Create the CSV and prepare for import using the COPY command
            DB.createCSV(data, schema_name, table_name)

            # Take the csv file and ingest into the database
            PostGre.ingestCSV(schema_name, table_name)
        else:
            continue

    # Sample query in code
    myResults = PostGre.query("Select * from myschema.table2")
    print(myResults)
