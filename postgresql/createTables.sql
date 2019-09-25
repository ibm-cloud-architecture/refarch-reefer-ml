-- Containers and container metrics DDL to create tables and index
-- used 
CREATE TABLE reefers (
    container_id varchar(64) NOT NULL PRIMARY KEY,
    reefer_model varchar(10),  -- 20RF, 40RH, 45RW
    last_maintenance_date TIMESTAMP
);

CREATE TABLE products (
    product_id varchar(64) NOT NULL PRIMARY KEY,
    description varchar(100),
    target_temperature REAL,
    target_humidity_level REAL
);


CREATE TABLE reefer_telemetries (
    container_id varchar(64) NOT NULL,
    measurement_time TIMESTAMP NOT NULL,
    product_id varchar(64) NOT NULL,
    temperature REAL,
    target_temperature REAL,
    ambiant_temperature REAL, 
    kilowatts REAL,
    time_door_open REAL,
    content_type INT,
    defrost_cycle INT,
    oxygen_level REAL,
    nitrogen_level REAL,
    carbon_dioxide_level REAL,
    humidity_level REAL,
    vent_1 BOOLEAN,
    vent_2 BOOLEAN,
    vent_3 BOOLEAN,
    carbon_dioxide_level REAL,
    location POINT,
    maintenance_required INT,
    primary key (container_id, measurement_time), -- Duplicate measurements not allowed
    foreign key (container_id) references Reefers(container_id),
    foreign key (product_id) references Products(product_id)
);