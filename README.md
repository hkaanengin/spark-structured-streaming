# Spark Structured Streaming

## Table of Contents
- [Introduction](#introduction)
- [Project Architecture](#project-architecture)

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