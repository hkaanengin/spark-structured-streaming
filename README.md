# Spark Structured Streaming

## Table of Contents
- [Introduction](#introduction)
- [Project Architecture](#project-architecture)
- [Container Creation!](#container-creation)

## Introduction

This project serves as an illustration to how to build an end-to-end data pipeline. It covers real-time aspects of data ingestion, processing and lastly storage using various tech stacks that include Python, Apache Kafka, Apache Airflow, Apache Spark, Apache Zookeeper and Cassandra. Last but not least, Docker is used to containerize each of the services essential for this project.

## Project Architecture

![System Architecture](<path-to-image>)

Essential components for this project are:
- **Data Source**: [randomuser.me](https://randomuser.me/) API as the starting point of the project to generate random user data.
- **Apache Airflow**: Responsible for orchestrating the pipeline and storing fetched data in a PostgreSQL database.
- **Apache Kafka and Zookeeper**: Used for streaming data from PostgreSQL to the processing engine.
    - **Kafka UI**: Review and controll the Kafka clusters&Schema registriesi
    - **Control Centre**:  Monitoring the Kafka streams(topics&partitions&production).
    - **Schema Registry**: Schema management of the Kafka streams.
- **Apache Spark**: Data processor unit of the system. Contains one master&worker.
- **Cassandra**: Where the data will be stored.

## Container Creation

Before getting the container up, two Jar files need to be downloaded for Spark configuration. You may do that via issuing the commands below in your terminal:

```bash
cd jars
curl -O https://repo1.maven.org/maven2/com/datastax/spark/spark-cassandra-connector_2.12/3.3.0/spark-cassandra-connector_2.12-3.3.0.jar
curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.13/3.3.0/spark-sql-kafka-0-10_2.13-3.3.0.jar
```
Or simply going to Maven Repository and downloading them manually. Don't forget to move them to the root path of the project:
- [Spark Cassandra Connector](https://mvnrepository.com/artifact/com.datastax.spark/spark-cassandra-connector_2.13/3.5.0)
- [Spark SQL Kafka](https://mvnrepository.com/artifact/org.apache.spark/spark-sql-kafka-0-10_2.13/3.5.1)

Now, we can get the container up and running with the necessary services by issuing the command below, in your terminal :

```bash
docker compose -f docker-compose-infra.yml up
```

If you encounter any permission error about accessing the entrypoint.sh(I did on my Mac), use the command below as your Airflow webservice command:

```bash
bash -c "chmod +x /opt/airflow/script/entrypoint.sh"
```
