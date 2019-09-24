import os,sys
import psycopg2
from urllib.parse import urlparse
import json

class ContainerMetricRepository:

    def __init__(self):
        self.parsedURL = urlparse(os.getenv('POSTGRESQL_URL','localhost:5432'))
        self.dbName = os.getenv('POSTGRESQL_DBNANE','ibmclouddb')
        self.sllCert = os.getenv('POSTGRESQL_SSL_PEM','')
        print(self.parsedURL.hostname + ":" + str(self.parsedURL.port))
        print(self.dbName )

    def connect(self):
        if self.sllCert != "" :
            print("Connect remote with ssl")
            self.conn = psycopg2.connect(host=self.parsedURL.hostname,
                                port=self.parsedURL.port,
                                user=self.parsedURL.username,
                                password=self.parsedURL.password,
                                sslmode='verify-full',
                                sslrootcert=self.sllCert,
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
        cur.execute("""CREATE TABLE IF NOT EXISTS reefers (
            container_id varchar(64) NOT NULL PRIMARY KEY,
            reefer_model varchar(10),  -- 20RF, 40RH, 45RW
            last_maintenance_date TIMESTAMP
            ); """)
        cur.execute("""CREATE TABLE IF NOT EXISTS products (
                product_id varchar(64) NOT NULL PRIMARY KEY,
                description varchar(100),
                target_temperature REAL,
                target_humidity_level REAL
            );""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reefer_telemetries (
                container_id varchar(64) NOT NULL,
                measurement_time TIMESTAMP NOT NULL,
                product_id varchar(64) NOT NULL,
                temperature REAL,
                target_temperature REAL,
                ambiant_temperature REAL, 
                kilowatts REAL,
                kilowatt_hours REAL,
                content_type INT,
                oxygen_level REAL,
                nitrogen REAL,
                vent_1 BOOLEAN,
                vent_2 BOOLEAN,
                vent_3 BOOLEAN,
                carbon_dioxide_level REAL,
                time_door_open REAL,
                location POINT,
                defrost_cycle INT,
                primary key (container_id, measurement_time), -- Duplicate measurements not allowed
                foreign key (container_id) references Reefers(container_id),
                foreign key (product_id) references Products(product_id)
            );""")

    def populateReefersReferenceData(self):
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO reefers(container_id, reefer_model) 
        VALUES ( 'C01','20RF'), ('C02','20RF'), ('C03','40RH'), ('C04','45RW');
        """)
        self.conn.commit()
        
    
    def populateProductsReferenceData(self):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO products(product_id,description,target_temperature,target_humidity_level) VALUES 
            ('P01','Carrots',4,0.4),
            ('P02','Banana',6,0.6),
            ('P03','Salad',4,0.4),
            ('P04','Avocado',6,0.4);
            """)
        self.conn.commit()

    def addReeferTelemetry(self,dataFrame):
        pass

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
        return json.dumps(results_list)

    def getAllReefers(self):
        return self.getAll("reefers")

    def getAllProducts(self):
        return self.getAll("products")

    def getAllReeferTelemetries(self):
        return self.getAll("reefer_telemetries")

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
    repo = ContainerMetricRepository()
    conn=repo.connect()
    v=repo.getVersion()
    print(v)
    repo.createTables()
    # repo.populateReefersReferenceData()
    repo.populateProductsReferenceData()
    reefers = repo.getAllReefers()
    print(reefers)
    products = repo.getAllProducts()
    print(products)
    repo.listTables()
    #repo.dropTable("reefer_telemetries")
    #repo.dropTable("products")
    