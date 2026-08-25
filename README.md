# DELTA
## DB(D)  Endpoint(E)  Latency(L)  Testing(T)  Ammeter(A)

📣 Annoucing a new tool to calculate Cloud Database endpoint latency using SQL queries

📌 Introducing DELTA (DB Endpoint Latency Testing Ammeter). DELTA is a tool to test real-world latency against a remote database using execution of a query and calculating the network return time. The tool provides functions to test latency of Oracle, MySQL and Postgres databases.

The tool uses the oracledb, psycopg2 and pymysql packages to connect to the respective databases and execute a single query per request (you can specify multiple requests as well). The tool uses the time module to measure the time it takes to execute the query, fetch the results, and close the connection. It calculates the latency of each request and the average latency of all requests.



![Delta_Ammeter](https://user-images.githubusercontent.com/39692236/213663909-24aaf0cd-8abc-429b-811d-25303aa7063e.png)

🔧 DELTA is a cloud tool to test real-world latency against a remote database endpoint using execution of a query and calculating the network return time. 


🔧 Network tools like ping ,iperf or tcp ping can only give you network based latency which does not always translate well to an application running those queries on a remote database. 


🐍 DELTA uses Python client for Oracle, MySQL and PostgreSQL to run a query like “SELECT 1” or "SELECT 1 FROM DUAL". You can then specific the number of executions of the query and DELTA calculates the average network round-trip time for all the executions of the query on the remote database. The script also includes error handling to track failed requests. You can also include your own custom queries. 


## How it works
The function 'measure_latency_oracle' uses the oracledb package to connect to the Oracle database and execute a single query per request. The function uses the time module to measure the time it takes to execute the query, fetch the results, and close the connection. The function then calculates the latency of each request and the average latency of all requests. The function opens a new connection for every request and closes it after fetching the results, which will measure the time it takes to execute the query, transfer the data over the network, and close the connection. The query parameter is passed to the function, allowing you to test the performance of the database with different queries. The same logic applies to the functions of mysql and postgres

🔌 Databases Supported :

![image](https://user-images.githubusercontent.com/39692236/215261248-336bcc14-8e45-409e-abb2-b71cdff490f2.png)


 📌 Oracle : 

- Amazon RDS Oracle

- OCI Autonomous Database

- OCI VMDB

- OCI Exadata Cloud Service

- Oracle Database On-Premise


📌 MySQL : 

- Amazon RDS MySQL

- Amazon RDS Aurora MySQL

- OCI MySQL Database Service

- OCI MySQL Heatwave

- On-premise MySQL


📌 Postgres :

- Amazon RDS Postgres

- Amazon RDS Aurora Postgres

- On-premise Postgres


📌 URL :

- Check Public or Private URLs for latency

# Requirements

```
Docker 
```

# Installation

You can install and run DELTA as a Docker container

Build from source

```
git clone https://github.com/shadabshaukat/DELTA.git && cd DELTA/

docker build -t delta . --tag delta  --pull --no-cache --force-rm

```

# Usage

The tool can be run using the command line. You will need to provide the following arguments:

    dbtype : The type of database you want to test. Can be 'oracle', 'autonomous', 'mysql' or 'postgres'
    num_of_requests : The number of requests you want to make to the database
    username : The username to connect to the database
    password : The password to connect to the database
    hostname : The hostname or IP address of the database
    portnumber : The port number of the database
    databasename : The name of the database
    "SQL QUERY" : The SQL query you want to test

## Autonomous Database Latency Check using SQL Query

#### Note : This option uses python-oracledb package in thin mode


```
docker run -it delta python3 main.py \
autonomous \
1 \
admin \
YourP@ssw0rd \
'(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=*******.adb.ap-melbourne-1.oraclecloud.com))(connect_data=(service_name=********_testdelta_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))' \
"SELECT 1 from DUAL"
```

- In case of Oracle Autonomous database, the connecting string can be found in OCI Console > Autonomous Database > DB Connection
- Currently only non-mTLS connections are supported. mTLS with wallet should be available soon


## Oracle Database Latency Check using SQL Query

#### Note : This option uses python-oracledb package in thick mode

```
docker run -it delta python3 main.py \
oracle \
1 \
hr \
YourP@ssw0rd  \
'host:port/servicename' \
"SELECT 1 from DUAL" 
 ```
 
 
 ## Oracle Database Latency Check using OCIping()

#### Note : This option uses the Oracle Python driver in thick mode and can only be used for Non-Autonomous Oracle Database. It does not require a SQL query but sends multiple requests using connection.ping() method


```
 docker run -it delta python3 main.py \
 ociping \
 100 \
 hr \
 YourP@ssw0rd   \
 'host:port/servicename' 
 ```
 
This function uses ping() [1] in python-oracledb thick mode which is a wrapper around OCIPing() function [2] 

[1] https://python-oracledb.readthedocs.io/en/latest/api_manual/connection.html#Connection.ping

[2] https://docs.oracle.com/en/database/oracle/oracle-database/19/lnoci/miscellaneous-functions.html#GUID-033BF96D-D88D-4F18-909A-3AB7C2F6C70F


## Postgres Latency Check

```
docker run -it delta python3 main.py \
postgres \
1 \
admin \
YourP@ssw0rd  \
database-1.******ap-southeast-2.rds.amazonaws.com \
5432 \
demodb \
"SELECT 1"
```

## MySQL Latency Check

```
docker run -it delta python3 main.py \
mysql \
1 \
admin \
YourP@ssw0rd  \
mysqldemo.c******ap-southeast-2.rds.amazonaws.com \
3306 \
demodb \
"SELECT 1"
```

## URL Latency Check

Public URL check
```
docker run -it delta python3 main.py \
url \
10 \
https://www.google.com
```

Private URL check
```
docker run -it delta python3 main.py \
url \
1000 \
https://10.180.1.21:4443
```

## Check python-oracledb and Oracle Instantclient version
```
docker run -it delta python3 -c "import oracledb; print(oracledb.version)"
1.2.2
```

```
docker run -it delta ls /usr/lib/oracle
19.10
```


    


# Function Definitions

### Important Note on Oracle Database Python Package performance
By default, python-oracledb runs in a ‘Thin’ mode which connects directly to Oracle Database. This mode does not need Oracle Client libraries. However, some additional functionality is available when python-oracledb uses them. Python-oracledb is said to be in ‘Thick’ mode when Oracle Client libraries are used. Both modes have comprehensive functionality supporting the Python Database API v2.0 Specification.

There are two ways to create a connection to Oracle Database using python-oracledb:

    Standalone connections: Standalone connections are useful when the application needs a single connection to a database. Connections are created by calling oracledb.connect().

    Pooled connections: Connection pooling is important for performance when applications frequently connect and disconnect from the database. Pools support Oracle’s high availability features and are recommended for applications that must be reliable. Small pools can also be useful for applications that want a few connections available for infrequent use. Pools are created with oracledb.create_pool() at application initialization time, and then ConnectionPool.acquire() can be called to obtain a connection from a pool.


Please refer to the below links for more details to get better performance out of your connectivity to Oracle Database  : 

[1] https://python-oracledb.readthedocs.io/en/latest/user_guide/connection_handling.html

[2] https://download.oracle.com/ocomdocs/global/Application_Programming_Using_Pooling.pdf

## measure_latency_oracle(user,password,dsn,num_requests,query)

This function is used to measure the latency of an Oracle database in thick mode. It takes in the following parameters:

    user: The username to connect to the Oracle database.
    password: The password to connect to the Oracle database.
    dsn: The hostname and portnumber/servicename of the Oracle database.
    num_requests: The number of requests to be made to the database.
    query: The SQL query to be executed on the database.

It returns the average latency in seconds and milliseconds, the number of successful requests and any errors that occurred during the test. 

## measure_latency_autonomous(user,password,dsn,num_requests,query)

This function is used to measure the latency of an Oracle Autonomous Database with TLS (mTLS currently isn't supported) in thin mode. It takes in the following parameters:

    user: The username to connect to the Autonomous database.
    password: The password to connect to the Autonomous database.
    dsn: The connectivity string of the Autonomous database.
    num_requests: The number of requests to be made to the database.
    query: The SQL query to be executed on the database.

It returns the average latency in seconds and milliseconds, the number of successful requests and any errors that occurred during the test. 

## measure_latency_ociping(user,password,dsn,num_requests)

This function is used to measure the latency of an Oracle database in thick mode. It uses the ping() function in python-oracledb package and takes in the following parameters:

    user: The username to connect to the Oracle database.
    password: The password to connect to the Oracle database.
    dsn: The hostname and portnumber/servicename of the Oracle database.
    num_requests: The number of requests to be made to the database.

It returns the average latency in seconds and milliseconds, the number of successful requests and any errors that occurred during the test.

## measure_latency_mysql(user,password,host,port,database,num_requests,query)

This function is used to measure the latency of a MySQL Database. It takes in the following parameters:

    user: The username to connect to the MySQL database.
    password: The password to connect to the MySQL database.
    host : Hostname or IP to connect to the MySQL database
    port : Port number of the MySQL database
    database : Database name of the MySQL instance
    num_requests: The number of requests to be made to the database.
    query: The SQL query to be executed on the database.

It returns the average latency in seconds and milliseconds, the number of successful requests and any errors that occurred during the test. 

##  measure_latency_postgres(user, password, host, port, dbname, num_requests, query)

This function is used to measure the latency of a Postgres Database. It takes in the following parameters:

    user: The username to connect to the Postgres database.
    password: The password to connect to the Postgres database.
    host : Hostname or IP to connect to the Postgres database
    port : Port number of the Postgres database
    dbname : Database name of the Postgres instance
    num_requests: The number of requests to be made to the database.
    query: The SQL query to be executed on the database.

It returns the average latency in seconds and milliseconds, the number of successful requests and any errors that occurred during the test.

## measure_latency_url(url, num_requests)

This function is used to measure the latency of a URL. The function accepts the URL as a string and the number of requests as an integer. It uses the requests module to make GET requests to the URL and the time module to measure the latency. It then calculates the average latency of all requests and prints the results. If any errors occur, they are added to the error_list and the error count is incremented. It takes in the following parameters:

    url: The URL against which the latency is to be measure
    num_requests: The number of requests to be made to the URL

Note : The ssal verification flag is set to False to allow testing of private URL's. It is advised to turn on SSL verificaton by setting verify=True
 
# Contributing

    Fork it (https://github.com/your-github-username/DELTA/fork)
    Create your feature branch (git checkout -b feature/fooBar)
    Commit your changes (git commit -am 'Add some fooBar')


