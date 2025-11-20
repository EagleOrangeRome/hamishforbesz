FROM ghcr.io/oracle/oraclelinux:8

RUN yum install -y oracle-release-el8 \
    && yum-config-manager --enable ol8_oracle_instantclient \
    && yum install -y oracle-instantclient19.10-basic


RUN dnf -y module disable python36 && \
    dnf -y module enable python39 && \
    dnf -y install python39 python39-pip python39-setuptools python39-wheel && \
    rm -rf /var/cache/dnf

RUN yum install -y postgresql-devel

RUN yum install -y gcc \
    && yum install -y libaio-devel

RUN pip3 install pymysql
RUN pip3 install oracledb
RUN pip3 install psycopg2-binary


# Set the environment variable for LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH /usr/lib/oracle/19.10/client64/lib/

ADD main.py .
COPY main.py ./main.py

CMD ["python3", "./main.py"]
