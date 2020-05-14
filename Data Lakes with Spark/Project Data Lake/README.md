## Data Lake Project
We are working for the Sparkify music streaming company.
They have accumulated data from their customers, but need help organizing their data in order to make meaningful decisions.

The company has collected data in two datasets: (Both in JSON format)
* Songs: Contains data about songs and the artist
* Logs: User generated data in relation to their streaming activity.

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
 
 ### Database Structure
**Fact Table**

1. **songplays** - records in event data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

**Dimension Tables**

2. **users** - users in the app
user_id, first_name, last_name, gender, level
3. **songs** - songs in music database
song_id, title, artist_id, year, duration
4. **artists** - artists in music database
artist_id, name, location, lattitude, longitude
5. **time** - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday
 
 ---
 
The task at hand is to:
 1. build an ETL pipeline which extracts the data from S3. (Transform into a Star Schema optimized for queries on song play analysis.)
 2. Processes the data using Spark.
 3. Loads the data back into S3 as a set of dimensional tables.
 
 ----
 
 ### Project Files
 
 * etl.py - Reads data from S3, processes that data using Spark, and writes them back to S3.
 * dl.cfg - Contains AWS credentials
 
 ---
 
 
 