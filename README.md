# DELTA
## DB(D)  Endpoint(E)  Latency(L)  Testing(T)  Ammeter(A)


![Delta_Ammeter](https://user-images.githubusercontent.com/39692236/213663909-24aaf0cd-8abc-429b-811d-25303aa7063e.png)

DELTA is a tool to test real-world latency against a remote database using execution of a query and calculating the network return time. The function 'measure_latency_oracle' uses the cx_Oracle package to connect to the Oracle database and execute a single query per request. The function uses the time module to measure the time it takes to execute the query, fetch the results, and close the connection. The function then calculates the latency of each request and the average latency of all requests.

The function opens a new connection for every request and closes it after fetching the results, which will measure the time it takes to execute the query, transfer the data over the network, and close the connection. The query parameter is passed to the function, allowing you to test the performance of the database with different queries. The same logic applies to the functions of  mysql and postgres(COMING SOON)

# Deployment

$ git clone https://github.com/shadabshaukat/DELTA.git

$ cd DELTA

$ sudo pip3 install -r requirements.txt

# Test Oracle Latency 
  ## Autonomous DB ##
  #### python3 main.py oracle <num_of_requests> <username> <password> 'hostname:portnumber/servicename' "SQL QUERY"
  $ python3 main.py oracle 10 admin YourP@ssw0rd1234#  '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=******.adb.ap-melbourne-1.oraclecloud.com))(connect_data=(service_name=*********_testdelta_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))' "SELECT 1 from DUAL"
  
  ## Non-Autonomous DB ##
  #### python3 main.py oracle <num_of_requests> <username> <password> 'connectingstring' "SQL QUERY"
  $ python3 main.py oracle 10 admin YourP@ssw0rd '10.10.1.10:1521/orcldev' "SELECT 1 from DUAL"

# Test MySQL Latency

