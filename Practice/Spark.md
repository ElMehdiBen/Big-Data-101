**Exemple 1**

```
data = [(1, “John”, “Doe”), (2, “Jane”, “Doe”), (3, “Bob”, “Smith”), \ 
        (4, “Alice”, “Johnson”), (5, “Charlie”, “Brown”), (6, “David”, “Jones”),\
        (7, “Eve”, “White”), (8, “Fred”, “Garcia”), (9, “Gina”, “Green”),\
        (10, “Harry”, “Harris”)]

df = spark.createDataFrame(data, ["id", "first_name", "last_name"])

df.show()
```

**Exemple 2**

```
mkdir /opt/sample_data
cd /opt/sample_data
wget https://raw.githubusercontent.com/metatron-app/metatron-doc-discovery/master/_static/data/sales-data-sample.csv

Use these commands to create a directory and copy data to the HDFS.

hdfs dfs -mkdir /sample_data
hdfs dfs -put /opt/sample_data/sales-data-sample.csv /sample_data/

sales_data = spark.read.option("header", True).csv("hdfs://namenode:8020/sample_data/sales-data-sample.csv")
sales_data.show()
```
