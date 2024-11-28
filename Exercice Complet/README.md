Getting the data
================

Download and move to a known directory the following files:

companies.csv: https://examples.citusdata.com/tutorial/companies.csv

Building The Flow
=================

We will build it step by step

- Let's add a header to the file
```
id, name, image_url, created_at, updated_at

# we can also use the script to create the database
CREATE TABLE companies (
    id bigint NOT NULL,
    name text NOT NULL,
    image_url text,
    created_at text,
    updated_at text
);
```
- Let's start with **GetFile**
- Then we add a **SplitRecord**
- We will need to configure **CSVReader**
![image](https://github.com/user-attachments/assets/a7501fd4-fd0f-4f99-bbba-96463a02fda7)
- We will need to configure **CSVRecordSetWriter**
![image](https://github.com/user-attachments/assets/de03e7aa-98a0-4715-888b-855eff045376)
- We should have this result by the end
![image](https://github.com/user-attachments/assets/43a37be2-7307-4874-a967-f47425c130e2)
- We will then add **PutDatabaseRecord**
![image](https://github.com/user-attachments/assets/c48b7b8c-5462-41f8-96bb-7e0743c95524)
- We should then download the **Postgresql JAR** from this link : https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
- And we should configure the added **DBCPConnectionPool**
![image](https://github.com/user-attachments/assets/94c9234b-0c17-4a15-af46-a84da32f0514)
- Connection URL : jdbc:postgresql://20.119.81.84:5432/postgres
- Driver Class Name : org.postgresql.Driver
