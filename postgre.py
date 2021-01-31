import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config


# All postgre characteristics here
# - Making the database connection
# - Executing queries
# - Executing Copy command (for data ingestion)
class PostGre:
    # The database connection
    @staticmethod
    def __conn():
        try:
            return psycopg2.connect(
                dbname=Config.PostGre.dbname,
                host=Config.PostGre.host,
                port=Config.PostGre.port,
                user=Config.PostGre.user,
                password=Config.PostGre.password
            )
        except Exception as e:
            print(e)

    # This method will enable us to query a select statement or execute a non select query
    @staticmethod
    def query(query_text, isSelectQuery: bool = True):
        cur = PostGre.__conn().cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(query_text)

            # Return results if select query
            if isSelectQuery:
                f_all = cur.fetchall()
                cur.close()
                return f_all
            # Execute Non Results query (such as an insert)
            else:
                cur.connection.commit()
                cur.close()
        except Exception as e:
            print(e)
        finally:
            if PostGre.__conn is not None:
                PostGre.__conn().close()

    # We can ingest a csv formatted text file here
    @staticmethod
    def ingestCSV(schema, table):
        cur = PostGre.__conn().cursor()  # The database we are posting to

        f = open("{0}/{1}_{2}.csv".format(Config.csvDir, schema, table), 'r')
        try:
            cur.copy_from(file=f, table="{0}.{1}".format(schema, table), null="")
        except Exception as e:
            print(e)
        f.close()
        cur.close()
        cur.connection.commit()
        PostGre.__conn().close()
