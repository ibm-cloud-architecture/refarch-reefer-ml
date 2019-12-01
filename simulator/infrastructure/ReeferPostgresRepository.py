import os,sys, io
import psycopg2
import pandas as pd 
from urllib.parse import urlparse
import json

TABLE_COLUMNS = {"container_id", "measurement_time", "product_id",
                "temperature","target_temperature", "ambiant_temperature", 
                "kilowatts", "time_door_open",
                "content_type", "defrost_cycle",
                "oxygen_level", "nitrogen_level", "humidity_level","carbon_dioxide_level", 
                "vent_1", "vent_2", "vent_3", "maintenance_required"}
TABLE_METRICS="reefer_telemetries"

class ReeferRepository:

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
        """
        Create reefers and products tables as reference data. It can be done with psql too.
        Then create the reefer telemetries table to keep all the metrics for Machine learning work
        """
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS reefers (
            container_id varchar(64) NOT NULL PRIMARY KEY,
            reefer_model varchar(10),  -- 20RF, 40RH, 45RW
            last_maintenance_date TIMESTAMP
            ); """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reefer_telemetries (
                container_id varchar(64) NOT NULL,
                measurement_time TIMESTAMP NOT NULL,
                product_id varchar(10) NOT NULL,
                temperature REAL,
                target_temperature REAL,
                ambiant_temperature REAL, 
                kilowatts REAL,
                content_type INT,
                oxygen_level REAL,
                nitrogen_level REAL,
                carbon_dioxide_level REAL,
                humidity_level REAL,
                vent_1 BOOLEAN,
                vent_2 BOOLEAN,
                vent_3 BOOLEAN,
                time_door_open REAL,
                location POINT,
                defrost_cycle INT,
                maintenance_required INT,
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
        
    


    def addReeferTelemetries(self,dataFrame: pd.DataFrame):
        """
        Bulk load all the tuples from a data frame into the reefer telemetries table
        """
        cur = self.conn.cursor()
        csv_str = dataFrame[TABLE_COLUMNS].to_csv(index=False, header=False)
        csv_buf = io.StringIO(csv_str)
        cur.copy_from(csv_buf, TABLE_METRICS, columns=(TABLE_COLUMNS), sep=",")
        self.conn.commit()
        print("Done uploading telemetry records !")
        

    def addReeferTelemetry(self,telemetry:dict):
        cur = self.conn.cursor()
        keys = telemetry.keys()
        columns = ','.join(keys)
        values = [telemetry[k] for k in keys]
        values_as_str = ','.join(['%s' for i in range(len(values))])
        sql='INSERT INTO reefer_telemetries({}) VALUES ({})'.format(columns,values_as_str)
        print(sql)
        cur.mogrify(sql,telemetry)
        self.conn.commit()
        print("Done uploading telemetry record !")
        

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

    def getAllReefers(self):
        return self.getAll("reefers")



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
    repo = ReeferRepository()
    conn=repo.connect()
    v=repo.getVersion()
    print(v)
    repo.createTables()
    repo.populateReefersReferenceData()
    reefers = repo.getAllReefers()
    print(reefers)
   
    repo.listTables()
    telemetry =  {
        "container_id": "C02",
        "measurement_time": "2019-09-16 23:41:28.424611",
        "product_id": "P02",
        "temperature": 4.0,
        "target_temperature": 4.0,
        "ambiant_temperature": 18.0,
        "kilowatts": 10,
        "content_type": 2,
        "oxygen_level": .2,
        "nitrogen_level": .6,
        "carbon_dioxide_level": .2,
        "humidity_level": .4,
        "vent_1": 1,
        "vent_2": 1,
        "vent_3": 1,
        "time_door_open": 0,
        "location": None,
        "defrost_cycle": 1,
        "maintenance_required": 0
    }

    # repo.addReeferTelemetry(telemetry)
    print(repo.getAllReeferTelemetries())
    # repo.dropTable("reefer_telemetries")

    