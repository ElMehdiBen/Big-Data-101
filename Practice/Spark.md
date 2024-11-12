**Exemple 1**

```
data = [(1, "John", "Doe"), (2, "Jane", "Doe"), (3, "Bob", "Smith"), \ 
        (4, "Alice", "Johnson"), (5, "Charlie", "Brown"), (6, "David", "Jones"),\
        (7, "Eve", "White"), (8, "Fred", "Garcia"), (9, "Gina", "Green"),\
        (10, "Harry", "Harris")]

df = spark.createDataFrame(data, ["id", "first_name", "last_name"])

df.show()
```

**Exemple 2**

```
sales_data = spark.read.option("header", True).csv("hdfs://namenode:8020/training/sales-data-sample.csv")
sales_data.show()
```
