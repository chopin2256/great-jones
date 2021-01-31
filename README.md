# JSON to Data Project

## What the script does
This script will create a table with appropriate data types, assumed by the values of the data. If the json file is different, a very simple technique is used to create a new table.  The following technique is:

<code>CREATE TABLE IF NOT EXISTS</code>

This let's us run the above command on every json run, and if the table al

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
###If you are using the mac terminal, use this string to make a connection:
<i>ssh -i "python_box.pem" ec2-user@ec2-50-19-60-173.compute-1.amazonaws.com</I>

###If you are using Windows like me, you can use a great SSH client called Bitvise

These are the data points required for bitvise
* host: ec2-50-19-60-173.compute-1.amazonaws.com
* port: 22
* user: ec2-user
* use included PEM key as a client key manager

## Once connected to the server
* Running the script, type
  * sudo su
  * cd /home/ec2-user/scripts && python3 main.py
    
This will execute the script and create and insert 3 rows of data into the database each time

## Database connection (using any client, I use dbeaver)
You can connect to the database, and run a sample query for testing:
<i>select * from test_schema.test_table</i>
* dbname = "warehouse"
* host = "database-1.ct6awduawhlx.us-east-1.rds.amazonaws.com"
* port = 5432
* user = "postgres"
* password = "greatjones"
