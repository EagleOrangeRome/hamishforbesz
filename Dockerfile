FROM oraclelinux:7-slim

RUN yum install -y oracle-release-el7 \
    && yum-config-manager --enable ol7_oracle_instantclient \
    && yum install -y oracle-instantclient19.10-basic

RUN yum install -y python3

RUN yum install -y python3-devel
RUN yum install -y postgresql-devel

RUN yum install -y gcc \
    && yum install -y libaio-devel

RUN pip3 install setuptools_rust
RUN pip3 install --upgrade pip
RUN pip3 install oracledb
RUN pip3 install pymysql
RUN pip3 install psycopg2-binary


# Set the environment variable for LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH /usr/lib/oracle/19.10/client64/lib/

ADD main.py .
COPY main.py ./main.py

CMD ["python3", "./main.py"]
