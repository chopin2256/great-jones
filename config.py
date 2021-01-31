# Our configs go here
# Really not a good idea to store user/pass info here.  I normally hide data in a config.ini (which is gitignored)
# Or better yet, pull config vals from Airflow encrypted values
class Config:
    # Csv Directory
    csvDir = "csvs"
    jsonDir = "json"

    # Postgre attributes
    class PostGre:
        dbname = "warehouse"
        host = "database-1.ct6awduawhlx.us-east-1.rds.amazonaws.com"
        port = 5432
        user = "postgres"
        password = "greatjones"


