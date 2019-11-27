# Define the products data into postgresql

We are using a Postgresql instance on IBM Cloud. So once you create your own instance get the credential for the URL and the certificate.

```

```

First be sure to set at least the following environment variables in the setenv.sh file

```
POSTGRES_URL,  POSTGRES_DBNAME,
```

If you use POSTGRESQL on IBM Cloud or any deployment using SSL, you need to get the SSL certificate as `postgres.pem` file, or set `POSTGRES_SSL_PEM` variable to the path where to find this file.


You should see:
```
Connect remote with ssl
('PostgreSQL 10.10 on x86_64-pc-linux-gnu, compiled by gcc (Debian 6.3.0-18+deb9u1) 6.3.0 20170516, 64-bit',)
[
    {
        "container_id": "C01",
        "last_maintenance_date": null,
        "reefer_model": "20RF"
    },
    {
        "container_id": "C02",
        "last_maintenance_date": null,
        "reefer_model": "20RF"
    },
    {
        "container_id": "C03",
        "last_maintenance_date": null,
        "reefer_model": "40RH"
    },
    {
        "container_id": "C04",
        "last_maintenance_date": null,
        "reefer_model": "45RW"
    }
]
[
    {
        "content_type": 1,
        "description": "Carrots",
        "product_id": "P01",
        "target_humidity_level": 0.4,
        "target_temperature": 4.0
    },
    {
        "content_type": 2,
        "description": "Banana",
        "product_id": "P02",
        "target_humidity_level": 0.6,
        "target_temperature": 6.0
    },
    {
        "content_type": 1,
        "description": "Salad",
        "product_id": "P03",
        "target_humidity_level": 0.4,
        "target_temperature": 4.0
    },
    {
        "content_type": 2,
        "description": "Avocado",
        "product_id": "P04",
        "target_humidity_level": 0.4,
        "target_temperature": 6.0
    }
]
```
