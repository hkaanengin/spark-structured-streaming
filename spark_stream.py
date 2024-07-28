import logging
from datetime import datetime
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

current_date = datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(filename=f'spark_stream_logs/{current_date}', level=logging.INFO)

def create_keyspace(session):
    """
        Creates Cassandra keypspace. Keyspaces are like databases in SQL/Snowflake etc with the replication factor feature added to them
    """
    session.execute(
        """
            CREATE KEYSPACE IF NOT EXISTS demo_dev
            WITH replication = {'class': 'SimpleStrategy', 
                                'replication_factor': '1'
                            };
        """
    )
    logging.info('Keyspace created successfuly!')

def create_table(session):
    """
        Creates Cassandra table
    """
    session.execute(
        """
            CREATE TABLE IF NOT EXISTS demo_dev.people_information (
            person_id UUID PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT,
            address TEXT,
            city TEXT,
            country TEXT,
            longitude TEXT,
            latitude TEXT
            );
        """
    )
    logging.info("Table created successfuly!")

def insert_data(session, **kwargs):
    #insert stuff to cassandra
    return None

def create_spark_connection(): #check mvn repository change checj 55mins realtime data streaming codewithyu
    """
        Creates the spark session with cassandra and spark connection. Make sure versions of the connectors matches with your downloaded jar.
        You may checkout the available packages here on MVN ..... : 
    """
    try:
        spark_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.13:3.5.1,"
                                           "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.1") \
            .config('spark.cassandra.connection.host', 'localhost') \
            .getOrCreate()
        logging.info("Spark connection established successfuly!")
        logging.info(spark_conn)
    except Exception as e:
        logging.error(f"Couldn't create spark session due to {e}")
        spark_conn = None
    return spark_conn

def create_kafka_dataframe(spark_conn):
    """
        Subscribes to the topic and read streaming data. Creates the initial dataframe
    """
    try: #checout "spark apache structure streaming kafka integration" page for multiple topics
        spark_df = spark_conn.readStream \
                .format('kafka') \
                .option('kafka.bootstrap.servers', 'localhost:9095') \
                .option('subscribe', 'people_topic') \
                .option('startingOffsets', 'earliest') \
                .load()
        logging.info("Initial kafka dataframe created successfuly!:")
        logging.info(spark_df)
    except Exception as e:
        logging.warning(f"Couldn't initialize kafka dataframe due to {e}")
        spark_df = None
    return spark_df

def create_cassandra_connection():
    """
        Creates Cassandra connection
    """
    try:
        cluster = Cluster(['localhost'])
        
        return cluster.connect()
    except Exception as e:
        logging.error(f"Couldn't create Cassandra connection due to {e}")
        return None
    
def create_selected_kafka_df(spark_df):
    """
        Modifies the initial dataframe and creates the final dataframe.
    """
    schema = StructType([
        StructField('person_id', StringType(), False),
        StructField('name', StringType(), False),
        StructField('age', IntegerType(), False),
        StructField('email', StringType(), True),
        StructField('address', StringType(), True),
        StructField('city', StringType(), True),
        StructField('country', StringType(), True),
        StructField('longitude', StringType(), True),
        StructField('latitude', StringType(), True)
    ])

    selected_df = spark_df.selectExpr("CAST(value as STRING)") \
                        .select(F.from_json(F.col('value'), schema).alias('data')).select('data.*')
    logging.info("Selected kafka dataframe:")
    logging.info(selected_df)

    return selected_df


if __name__ == '__main__':
    spark_conn = create_spark_connection()

    if spark_conn:
        spark_df = create_kafka_dataframe(spark_conn)
        selected_df = create_selected_kafka_df(spark_df)

        cass_session = create_cassandra_connection()
        if cass_session:
            create_keyspace(cass_session)
            create_table(cass_session)

            logging.info("Streaming is getting started...")

            streaming_query = (selected_df.writeStream.format('org.apache.spark.sql.cassandra')
                                        .option('checkpointLocation', '/tmp/checkpoint')
                                        .option('keyspace', 'demo_dev')
                                        .option('table', 'people_information')
                                        .start()
                                        )
            streaming_query.awaitTermination()