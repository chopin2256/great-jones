import re
import csv
import os
from postgre import PostGre
from config import Config


#  Create the data structures
#  Examples:
#
#  Creating a table
#  Creating a csv
#  Flattening a json file
class DB:
    @staticmethod
    # Create our table from the json file, if applicable
    def createTable(data, schema, table):
        # This list comprehension is not easy to read but I like them because they are one liners
        # This can be broken down into a traditional loop for debugging purposes and readability
        # What this loop does is reads the field_name (x) and removes the keyword "object_" from the field names
        # Then we append y[0] which is the first element of the value which corresponds to the data type
        # Now since this is a list, we can use a python function "join" to turn into a concatenated string of commas
        fields = ", ".join([x.replace("object_", "") + " " + y[0] for x, y in dict(data[0]).items()])

        # The below code here is equivalent to the above one liner
        # This is how I would debug if the above was giving me problems
        # I prefer the above method because it is cleaner, and if it is well tested, there is no reason to keep
        # the 7 lines of code.  But I do agree, the above is not easy to read!

        ##################################################
        # fields = []
        # for x, y in dict(data).items():
        #     field_name = x.replace("object_", "")
        #     data_type = y[0]
        #     fields.append(field_name + " " + data_type)
        # fields = ", ".join(fields)
        ##################################################

        # The sql string that is executed to create the table
        sql = "CREATE SCHEMA IF NOT EXISTS {0}; CREATE TABLE IF NOT EXISTS {0}.{1} ({2});".format(schema, table, fields)
        PostGre.query(sql, False)

    # This method simply turns the json data into a csv file
    # We could just run an Insert command if the data comes in as one line updates, but if the data comes in a larger
    # Feed, Inserts are not advisable.  It would slow down the database greatly.  Thus
    # A csv file must be created in order to import efficiently into PostGres using its native COPY command.
    # We effectively are utilizing this native command via the psycopg2 module
    @staticmethod
    def createCSV(data, schema, table):
        # Create our csv directory
        if not os.path.exists(Config.csvDir):
            os.makedirs(Config.csvDir)

        # Create our csv file here for import
        with open("{0}\{1}_{2}.{3}".format(Config.csvDir, schema, table, "csv"), "w", newline="", encoding='utf-8') as f:
            w = csv.writer(f, quotechar='\"', quoting=csv.QUOTE_MINIMAL, delimiter='\t')
            for rows in data:
                w.writerow([y[1] for x, y in dict(rows).items()])

    #  This is just a simple recursive function that flattens a hierarchical dataset
    #  Returns a dictionary of lists.  The key portion = field_name, and the value portion is a list that contains 2 elements
    #  First element 0 contains the data type, the second element 1 contains the value of that data
    @staticmethod
    def getData(data):
        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    # If result set is dictionary, append the field name
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    # If result set is list, append the field name
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                # We are at the end of the node
                # Determine the data type here
                out[name[:-1]] = [DB.__dataType(x), x]

        # Traverse the list/dict
        final = []
        for y in data:
            out = {}
            flatten(y)
            final.append(out)  # Store our flattened data by "rows" here
        return final

    # A very basic function to determine the datatypes
    # This would ideally be expanded as we come across more weird data types
    # For example, there may be more date formats I could be missing, so the regular expressions
    # for dates are not comprehensive here
    @staticmethod
    def __dataType(x):
        # If we match a date format, return date
        if type(x) is str and bool(re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", x)):
            return "date"
        # Numeric
        elif type(x) is int:
            return "numeric"
        # All else, return varchar
        else:
            return "varchar"
