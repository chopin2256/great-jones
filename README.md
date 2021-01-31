# JSON to Data Project

## What the script does
This script will flatten and output a json file into objects.  Then it will create a table with appropriate data types, assumed by the values of the data.  Finally, we import the data into the tables using PostGre's COPY command.  The json files must be stored in the json directory and also must be in the format of:

<code>schemaname_tablename.json</code>

Following this format will recognize each file source as its own table in specified schemas.  The way this works is by splitting the filenames with the delimiter "_".

## Code Structure
* <b>main.py</b> - <i>entry point</i>
* <b>config.py</b> - <i>configurations</i>
* <b>data.py</b> - <i>creating our data structures</i>
* <b>postgre.py</b> - <i>postgre operations</i>

## Libraries used
* <b>json</b> - <i>convert our string json file to objects</i>
* <b>psycopg2</b> - <i>great low level library for postgre operations</i>
* <b>re</b> - <i>regular expressions to help us with string manipuation or matching</i>
* <b>csv</b> - <i>great low level library to aid us with csv operations</i>
* <b>os</b> - <i>file and directory creation/deletion etc</i>

## How to connect to the EC2 via SSH
#### First, store the pem key on your computer.  If you are using the mac terminal, use this string to make a connection:<br>
<code>ssh -i "python_box.pem" ec2-user@ec2-50-19-60-173.compute-1.amazonaws.com</code>
####If you are using Windows like me, you can use an SSH client called Bitvise

These are the data points required for bitvise
* host: ec2-50-19-60-173.compute-1.amazonaws.com
* port: 22
* user: ec2-user
* use included PEM key as a client key manager

## Once connected to the server
* Running the script, type
  * sudo su
  * cd /home/ec2-user/scripts && python3 main.py
    
This will execute the script and create 2 tables and insert 3 rows of data into each table upon every execution

## Database connection (using any client, I use dbeaver)
* dbname = "warehouse"
* host = "database-1.ct6awduawhlx.us-east-1.rds.amazonaws.com"
* port = 5432
* user = "postgres"
* password = "greatjones"

You can connect to the database, and run a sample query for testing:<p>
* SELECT * FROM myschema.table1
* SELECT * FROM myschema.table2
