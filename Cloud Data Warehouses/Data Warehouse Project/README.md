# Data Warehouse Project
In this project I am given data from a company called 'Sparkify'.
I am provided with LOG and SONG data that is located in the data folder in JSON format.


### Data Format
e.g. song data files:
```
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```
e.g. song data file:
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

e.g log data files
```
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```

e.g. log data file
![](log-data.png)
 
---

### Task

Given then song and event datasets, I need to create a star schema optimized for queries on song play analysis.


### Files

* **create_table.py**

    Fact and dimension tables for the star schema in Redshift.
* **etl.py**
 
    Loads data from S3 into staging tables on Redshift and then processes that data into the analytics tables on Redshift.
* **sql_queries.py**
 
    Defines SQL statements, which is imported into the two other files above.

---

### Project Steps

**Create Table Schemas**

1. Design schemas for your fact and dimension tables
2. Write a SQL CREATE statement for each of these tables in sql_queries.py
3. Complete the logic in create_tables.py to connect to the database and create these tables
4. Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. This way, you can run create_tables.py whenever you want to reset your database and test your ETL pipeline.
5. Launch a redshift cluster and create an IAM role that has read access to S3.
6. Add redshift database and IAM role info to dwh.cfg.
7. Test by running create_tables.py and checking the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.

---

### Database Structure
**Fact Table**

1. ***songplays*** - records in event data associated with song plays i.e. records with page NextSong
    * songplay_id - IDENTITY(0,1) over SERIES and PRIMARY KEY
    * start_time - Good idea to use SORTKEYon timestamp REFERENCES time
    * user_id - REFERENCES users
    * level 
    * song_id - REFERENCES songs
    * artist_id - REFERENCES artists
    * session_id 
    * location
    * user_agent

**Dimension Tables**

2. users - users in the app
user_id, first_name, last_name, gender, level
3. songs - songs in music database
song_id, title, artist_id, year, duration
4. artists - artists in music database
artist_id, name, location, lattitude, longitude
5. time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday


### Process

1. First create the AIM role and Redshift cluster by running create_aim_cluster.py.
To do that you need to fill in the variables in the dwh.cfg file.
It asks for inputs to the AIM and Cluster. The file has to be run a few times, first to create the cluster, then once created it needs to be run again to obtain the ARN.
And then it should be run again to obtain the endpoint (host).
2. Run create_tables.py which uses the sql queries and the connection to the database.
3. Run etl.py to extract data from the files in the S3 and stage it in redshift cluster, and to then be able to store it in the dimensional tables