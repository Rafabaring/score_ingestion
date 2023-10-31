## Start Application
This is an ETL application that combines ingestion of real-time data and batch processing. Its main purpose is to fetch data from the feed and make it readily available, in a normalized way, for consumption. Also, generate supporting analytics tables to facilitate research by analysts. It establishes a connection with a live feed providing `exam_score` data, evaluates its quality, stores it most efficiently, and makes it available for consumption downstream

It's a containerized application that was built having in mind an easy and simple start process

All you will need is (to download Docker if you haven't already), `cd` into the project folder and run the following bash command:

```
./entrypoint
```

In broad lines, the `./entrypoint` bash script will execute the following steps:
* STEP 1: Build and run the container making the application and the Postgres DB live
* STEP 2: Start the application from inside the container (run the `main.py` python script). `main.py` is where we open the feed and call all steps to process and store the data.

## Table Schema
The current application will create and populate a few tables. They could be divided into three groups:

* 1 - Events table: based on a star-schema, this group of tables has `EVENTS` as the <strong>FACT</strong> table with all the incoming messages normalized and the `EVENT_TYPE`, `STUDENTS` and `EXAM` being the <strong>DIMENSION</strong> tables to support the EVENTS/FACT table

* 2 - Data quality quarantine table: This is the `DATA_QUALITY_CHECKS_RESULTS` table and that will house any payload that hasn't passed the data quality check for further investigation

* 3 - Data analysis supporting table: `STUDENT_AVERAGE_SCORE` and `EXAM_AVERAGE_SCORE` are both analytics supporting tables, designed to support analysts on their research, generated through batch processing every minute

Here is the table schema

![Table Schema](/diagrams/table_schema.jpg?raw=true "Table Schema")

## Job Architecture
In this application, we have two main groups of jobs:

* 1 - Real-time message ingestion job: We can consider this the "main" job responsible for ingesting, pre-processing (running data quality checks), normalizing and storing data. Also responsible for generating the table_schema groups 1 (Events table) and 2 (Data quality), both described above. In this process, we establish the connection with the open live feed. The main "controller" of this job lives in the 'main.py' file and we can consider it a real-time-based data ingestion

* 2 - Batch analytics processing: This job runs every minute and is responsible for populating two supporting tables (`STUDENT_AVERAGE_SCORE` and `EXAM_AVERAGE_SCORE`). In broad terms, for every minute, it will read through all EVENT table, aggregate score data based on the subject (student or exam), and update the table with a summary of scores. The main file for these jobs lives under "./analytics_job"
 
![Job Architecture](/diagrams/job_architecture.jpg?raw=true "Job Architecture")

## Analyst support
In this section, I'll explain how this application aims to facilitate data consumption downstream. But before that, here is a premise I followed 

```
PREMISE: If the data exists in the live feed, it means that a user and the exam exist and the user has completed an exam. In other words, there's no way for the data to be
published without an exam or a user
```

What I mean with the above premise is if the user is in the `students` table, they have completed one exam. The same goes for the `exams` table. If there's an `exam_id` it means that the exam was taken by a student.

By making use of the `students` and `exams` <strong>DIMENSION</strong> table, we can answer questions 1 and 3 from the analyst with the following query:

1. List all users that have received at least one test score
~~~~sql
SELECT id, student_identification
FROM students
~~~~
The above query will return a table with unique students and all of them have completed at least one exam

3. List all the exams that have been recorded
~~~~sql
SELECT id, exam_identification
FROM exams
~~~~
The above query will return a table with unique exams and all of them have been completed by a student.

### Analytics supporting table
As part of the pipeline, two analytics_supporting jobs will be ignited (every minute according to the `crontab`). These two jobs will read from the `events` table, aggregate data, and generate other two supporting analytics tables. `student_average_score` and `exam_average_score`.
You can find the table definition under the `Table Schema` section in this README.md but, in broad lines, it is a table with:
- unique student_id (or exam_id)
- list of all scores a single student has
- average of the scores

To answer questions number 2 and 4, I would call these `analytics_supporting` tables and execute the following query:
2. List the test results for a specified student, and provides the student's average score across all exams
~~~~sql
SELECT student_id, scores_all, average_score
FROM student_average_score
~~~~
4. List all the results for the specified exam, and provides the average score across all students
~~~~sql
SELECT exam_id, scores_all, average_score
FROM exam_average_score
~~~~