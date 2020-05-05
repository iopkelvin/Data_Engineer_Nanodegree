## Data Modeling Project
# Sparkify Postgres ETL

The project consists in creating a Database Schema and ETL pipeline that is able to organize the data that Sparkify gathered from its customers.
The data is found in a JSON logs directory. It has the user activity on the Sparkify app.
 
### Files:
1. test.ipynb displays the first few rows of each table to check the database.
2. etl.ipynb reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.
3. sql_queries.py contains all your sql queries.
4. create_tables.py drops and creates your tables. Run this file to reset the tables before each time you run the ETL scripts. 
5. etl.py reads and processes files from song_data and log_data and loads them into your tables.

### Organization of Project
The main file is the sql_queries.py It has the sql queries used to DROP, CREATE, and INSERT tables.
The create_tables.py file creates and connects to the POSTGRES database. It also creates and drops the tables by calling the sql queries from the sql_queries.py file.
* Before making any action, the create_tables.py file has to be called to restart the database.
The etl.py file is the pipeline file. it has the architecture code that reads and processed the log and song data by using the sql_queries.py file, and it adds it to the new database schema.

#### etl.py
* The etl.py file first connects to the sparkify database and then processes the song and log data.
* Each JSON file is processed and then read into the read_json function.
* We select only a few columns and then add them to the created database tables.
* For the log file, we only select the rows where page='NextSong'.
* The log file data also has a column 'ts' that needs further processing. It is a timestamp that needs to be separated into (day,hour,week,day_of_week).
* Lastly, we join the song and artists created tables and insert them into the songplay fact table.

