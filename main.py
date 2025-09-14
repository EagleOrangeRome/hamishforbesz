import sys
import oracledb
import pymysql
import psycopg2
import time

##############################################################
#
# DELTA
# DB(D)  Endpoint(E)  Latency(L)  Testing(T) Ammeter(A)
#
##############################################################

def measure_latency_oracle(user,password,dsn,num_requests,query):
    total_latency = 0
    success_count = 0
    error_count = 0
    error_list = []
    num_requests = int(num_requests)
    for i in range(num_requests):
        try:
            # Connect to Oracle
            oracledb.init_oracle_client()
            start_time = time.time()
            connection = oracledb.connect(user=user, password=password, dsn=dsn)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            end_time = time.time()
            connection.close()

            # Calculate the latency
            latency = end_time - start_time
            total_latency += latency
            success_count += 1
        except oracledb.Error as e:
            print("Cannot connect to Oracle Instance")
            error_count += 1
            error_list.append(e)
    if success_count > 0:
        avg_latency = total_latency / success_count
        # Print the average latency
        print("## Oracle Latency ##")
        print("Average Latency in Seconds:", avg_latency)
        print("Average Latency in Milliseconds:", avg_latency*1000)
        print("Successful requests: ", success_count)
        if error_count > 0:
            print("Unsuccessful requests: ", error_count)
            print("Error List: ", error_list)
        return avg_latency
    else:
        print("No Successful requests were made, Error List: ", error_list)

def measure_latency_autonomous(user,password,dsn,num_requests,query):
    total_latency = 0
    success_count = 0
    error_count = 0
    error_list = []
    num_requests = int(num_requests)
    for i in range(num_requests):
        try:
            # Connect to Oracle
            start_time = time.time()
            connection = oracledb.connect(user=user, password=password, dsn=dsn)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            end_time = time.time()
            connection.close()

            # Calculate the latency
            latency = end_time - start_time
            total_latency += latency
            success_count += 1
        except oracledb.Error as e:
            print("Cannot connect to Oracle Instance")
            error_count += 1
            error_list.append(e)
    if success_count > 0:
        avg_latency = total_latency / success_count
        # Print the average latency
        print("## Oracle Latency ##")
        print("Average Latency in Seconds:", avg_latency)
        print("Average Latency in Milliseconds:", avg_latency*1000)
        print("Successful requests: ", success_count)
        if error_count > 0:
            print("Unsuccessful requests: ", error_count)
            print("Error List: ", error_list)
        return avg_latency
    else:
        print("No Successful requests were made, Error List: ", error_list)


def measure_latency_mysql(user,password,host,port,database,num_requests,query):
    total_latency = 0
    success_count = 0
    error_count = 0
    port=int(port)
    error_list = []
    num_requests = int(num_requests)
    for i in range(num_requests):
        try:
            # Connect to MySQL
            start_time = time.time()
            connection = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            end_time = time.time()
            connection.close()

            # Calculate the latency
            latency = end_time - start_time
            total_latency += latency
            success_count += 1
        except pymysql.Error as e:
            print("Cannot connect to MySQL Instance")
            error_count += 1
            error_list.append(e)
    if success_count > 0:
        avg_latency = total_latency / success_count
        # Print the average latency
        print("## MYSQL Latency ##")
        print("Average Latency in Seconds:", avg_latency)
        print("Average Latency in Milliseconds:", avg_latency*1000)
        print("Successful requests: ", success_count)
        if error_count > 0:
            print("Unsuccessful requests: ", error_count)
            print("Error List: ", error_list)
        return avg_latency
    else:
        print("No Successful requests were made, Error List: ", error_list)


def measure_latency_postgres(user, password, host, port, dbname, num_requests, query):
    total_latency = 0
    success_count = 0
    error_count = 0
    error_list = []
    num_requests = int(num_requests)
    for i in range(num_requests):
        try:
            # Connect to Postgres
            start_time = time.time()
            connection = psycopg2.connect(user=user, password=password, host=host, port=port, dbname=dbname)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            end_time = time.time()
            connection.close()

            # Calculate the latency
            latency = end_time - start_time
            total_latency += latency
            success_count += 1
        except psycopg2.Error as e:
            print("Cannot connect to Postgres")
            error_count += 1
            error_list.append(e)
    if success_count > 0:
        avg_latency = total_latency / success_count
        # Print the average latency
        print("## Postgres Latency ##")
        print("Average Latency in Seconds:", avg_latency)
        print("Average Latency in Milliseconds:", avg_latency*1000)
        print("Successful requests: ", success_count)
        if error_count > 0:
            print("Unsuccessful requests: ", error_count)
            print("Error List: ", error_list)
        return avg_latency
    else:
        print("No Successful requests were made, Error List: ", error_list)


if len(sys.argv) < 4:
    print("Invalid number of arguments passed")
else:
    db_type = sys.argv[1]
    num_requests = sys.argv[2]
    if db_type == "oracle":
        user = sys.argv[3]
        password = sys.argv[4]
        dsn = sys.argv[5]
        query = sys.argv[6]
        measure_latency_oracle(user,password,dsn,num_requests,query)
    if db_type == "autonomous":
        user = sys.argv[3]
        password = sys.argv[4]
        dsn = sys.argv[5]
        query = sys.argv[6]
        measure_latency_autonomous(user,password,dsn,num_requests,query)
    elif db_type == "mysql":
        user = sys.argv[3]
        password = sys.argv[4]
        host = sys.argv[5]
        port = sys.argv[6]
        database = sys.argv[7]
        query = sys.argv[8]
        measure_latency_mysql(user,password,host,port,database,num_requests,query)
    elif db_type == "postgres":
        user = sys.argv[3]
        password = sys.argv[4]
        host = sys.argv[5]
        port = sys.argv[6]
        database = sys.argv[7]
        query = sys.argv[8]
        measure_latency_postgres(user,password,host,port,database,num_requests,query)
    else:
        print("Invalid db_type argument passed")
