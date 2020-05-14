import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    '''
    This functions creates or connects to a Spark Session
    '''
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    '''
    This function extracts song data from S3, processes the data, and loads it back into S3
    :param spark: Spark Session
    :param input_data: Location of song data as JSON in the S3
    :param output_data:  Location where S3 will be loaded, in the S3 bucket
    '''
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)

    # Enable SQL querying
    df.createOrReplaceTempView('song_data_table')

    # extract columns to create songs table
    songs_table = spark.sql("""
        SELECT song_id,
                title,
                artist_id,
                year,
                duration
        FROM song_data_table 
        WHERE song_id IS NOT NULL
    """)
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy('year', 'artist_id').parquet(output_data + 'artists_table/')

    # extract columns to create artists table
    artists_table = spark.sql("""
        SELECT DISTINCT a.artist_id,
                        a.artist_name,
                        a.artist_location,
                        a.artist_latitude,
                        a.artist_longitude
                        FROM song_data_table a
                        WHERE a.artist_id IS NOT NULL
    """)
    
    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(output_data + 'artist_table/')


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data = input_data + 'log_data/*.json'

    # read log data file
    df = spark.read.json(log_path)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # Enable SQL querying
    df.createOrReplaceTempView('log_data')

    # extract columns for users table    
    users_table = spark.sql("""
        SELECT DISTINCT l.useriD AS user_id,
                        l.firstName AS first_name,
                        l.lastName AS last_name,
                        l.gender AS gender,
                        l.level AS level
                        FROM log_data l
                        WHERE l.userId IS NOT NULL
    """)
    
    # write users table to parquet files
    users_table.write.mode('overwrite').parquet(output_data + 'users_table/')

    # create timestamp column from original timestamp column
    # get_timestamp = udf()
    # df =
    #
    # create datetime column from original timestamp column
    # get_datetime = udf()
    # df =
    
    # extract columns to create time table
    time_table = spark.sql("""
        SELECT t.datetime AS start_time,
                hour(t.datetime) AS hour,
                dayofmonth(t.datetime) AS day,
                weekofyear(t.datetime) AS week,
                month(t.datetime) AS month,
                year(t.datetime) AS year,
                dayofweek(t.datetime) AS weekday
        FROM
            (SELECT to_timestamp(ts / 1000) AS datetime
            FROM log_data 
            WHERE ts IS NOT NULL) t
    """)
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy('year', 'month').parquet(output_data, 'time_table/')

    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data + 'songs_table/')

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql("""
        SELECT monotonically_increasing_id() AS songplay_id,
                to_timestamp(log.ts / 1000) AS start_time,
                month(to_timestamp(log.ts / 1000)) AS month,
                year(to_timestamp(log.ts / 1000)) AS year,
                log.userId AS user_id,
                log.level AS level,
                song.song_id as song_id,
                song.artist_id AS artist_id,
                log.sessionId AS session_id,
                log.location AS location,
                log.userAgent AS user_agent
        FROM log_data log
        JOIN song_data song 
        ON log.artist = song.artist_name 
        AND log.song = song.title
    """)

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode('overwrite').partitionBy('year', 'month').parquet(output_data + 'songplays_table/')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    # Path to bucket to deposit data after processing
    output_data = ""
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
