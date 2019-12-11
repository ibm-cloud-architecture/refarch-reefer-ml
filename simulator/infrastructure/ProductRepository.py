'''
Product repository is here to define the products table in postgresql and add
some test data.
'''
import os, json
from urllib.parse import urlparse
import psycopg2

class ProductRepository:
    
    def __init__(self):
        self.parsedURL = urlparse(os.getenv('POSTGRES_URL','localhost:5432'))
        self.dbName = os.getenv('POSTGRES_DBNAME','ibmclouddb')
        self.tlsCert = os.getenv('POSTGRES_SSL_PEM','')
        print(self.parsedURL.hostname + ":" + str(self.parsedURL.port))
        print(self.dbName )

    def connect(self):
        if self.tlsCert != "" :
            print("Connect remote with ssl")
            self.conn = psycopg2.connect(host=self.parsedURL.hostname,
                                port=self.parsedURL.port,
                                user=self.parsedURL.username,
                                password=self.parsedURL.password,
                                sslmode='verify-full',
                                sslrootcert=self.tlsCert,
                                database=self.dbName)
        else:
            self.conn = psycopg2.connect(host=self.parsedURL.hostname,
                                port=self.parsedURL.port,
                                user=self.parsedURL.username,
                                password=self.parsedURL.password,
                                database=self.dbName
                                )
        return self.conn


    def getVersion(self):
        cur = self.conn.cursor()
        cur.execute('SELECT version()')
        return cur.fetchone()

    def createTables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
        product_id varchar(10) NOT NULL PRIMARY KEY,
        description varchar(100),
        target_temperature REAL,
        target_humidity_level REAL,
        content_type INT);
        """)

    def populateProductsReferenceData(self):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO products(product_id,description,content_type,target_temperature,target_humidity_level) VALUES 
            ('P01','Carrots',1,4,0.4),
            ('P02','Banana',2,6,0.6),
            ('P03','Salad',1,4,0.4),
            ('P04','Avocado',2,6,0.4),
            ('P05','Tomato',6,6,0.3);
            """)
        self.conn.commit()

    def getAllProducts(self):
        return self.getAll("products")
    
    def getAll(self,tableName):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM " + tableName)
        cursor_obj = cur.fetchall()
        # grabs column names from the table
        labels = [column[0] for column in cur.description]
        # makes a list from the dict of the zip of column names and the results object
        results_list = []
        for row in cursor_obj:
            results_list.append(dict(zip(labels, row)))
        return json.dumps(results_list,indent=4, sort_keys=True, default=str)

    def dropTable(self,tableName):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE " + tableName)
        self.conn.commit()

    def listTables(self):
        cur = self.conn.cursor()
        cur.execute("""
        SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
        """)
        cursor_obj = cur.fetchall()
        for row in cursor_obj:
            print(row)

if __name__ == '__main__':
    repo = ProductRepository()
    conn=repo.connect()
    v=repo.getVersion()
    print(v)
    repo.createTables()
    # repo.populateProductsReferenceData()
    products = repo.getAllProducts()
    print(products)
    # repo.dropTable("products")