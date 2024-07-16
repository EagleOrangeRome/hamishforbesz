import sys
import cx_Oracle
import pymysql
import time

##############################################################
# DELTA
# DB(D)  Endpoint(E)  Latency(L)  Testing(T) Ammeter(A)
#
##############################################################
# Explanation :
# DELTA is a tool to test real-world latency against a remote database using execution of a query and calculating the network return time. The function 'measure_latency_oracle' uses the cx_Oracle package to connect to the Oracle database and execute a single query per request. The function uses the time module to measure the time it takes to execute the query, fetch the results, and close the connection. The function then calculates the latency of each request and the average latency of all requests.

#The function opens a new connection for every request and closes it after fetching the results, which will measure the time it takes to execute the query, transfer the data over the network, and close the connection. The query parameter is passed to the function, allowing you to test the performance of the database with different queries.

# The same logic applies to the functions of  mysql and postgres(COMING SOON)
# Install
# pip3 install psycopg2-binary (COMING SOON)
# pip3 install cx_Oracle
# pip3 install pymysql
###############################

### Example Usage ###
### MySQL Database ###
# python3 main.py <dbtype> <num_of_requests> <username> <password> <hostname> <portnumber> <databasename> "SQL QUERY"
# eg : python3 main.py mysql 1 appuser YourP@ssw0rd 10.10.1.20 3306 demo "SELECT 1"
#
#### Oracle Database ####
# Non-Autonomous Database
# python3 main.py oracle <num_of_requests> <username> <password> '<hostname>:<portnumber>/<servicename>' "SQL QUERY"
# eg :  python3 main.py oracle 10 admin YourP@ssw0rd '10.10.1.10:1521/orcldev' "SELECT 1 from DUAL"
# ## Oracle Latency ##
#Average Latency in Seconds: 0.10436289310455323
#Average Latency in Milliseconds: 104.36289310455322
#Successful requests:  10
#
# Autonomous Database
# python3 main.py oracle <num_of_requests> <username> <password> 'connectingstring' "SQL QUERY"
# eg : python3 main.py oracle 10 admin YourP@ssw0rd1234#  '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=******.adb.ap-melbourne-1.oraclecloud.com))(connect_data=(service_name=*********_testdelta_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))' "SELECT 1 from DUAL"
# ## Oracle Latency ##
#Average Latency in Seconds: 0.18985347747802733
#Average Latency in Milliseconds: 189.85347747802734
#Successful requests:  10
##

def measure_latency_oracle(user,password,dsn,num_requests,query):
    total_latency = 0
    success_count = 0
    error_count = 0
    error_list = []
    num_requests = int(num_requests)
    for i in range(num_requests):
        try:
            # Connect to Oracle
            start_time = time.time()
            connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            end_time = time.time()
            connection.close()

            # Calculate the latency
            latency = end_time - start_time
            total_latency += latency
            success_count += 1
        except cx_Oracle.Error as e:
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

if len(sys.argv) < 3:
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
    elif db_type == "mysql":
        user = sys.argv[3]
        password = sys.argv[4]
        host = sys.argv[5]
        port = sys.argv[6]
        database = sys.argv[7]
        query = sys.argv[8]
        measure_latency_mysql(user,password,host,port,database,num_requests,query)
    else:
        print("Invalid db_type argument passed")
