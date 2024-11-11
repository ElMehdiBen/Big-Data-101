PySpark DataFrame Functions: A Comprehensive Guide
==================================================

PySpark, the Python API for Apache Spark, provides a powerful and versatile platform for processing and analyzing large datasets. In this article, we’ll explore key PySpark DataFrame functions, essential for performing various data manipulation tasks.

![captionless image](https://miro.medium.com/v2/resize:fit:1164/format:webp/1*CL6pcE-bb8x_kKZC9XlmAw.png)

**Creating a DataFrame in PySpark:**

Before discussing the functions, let’s start by creating a DataFrame. A DataFrame in PySpark is a distributed collection of data, organized into named columns, similar to a table in a relational database.

**Example:**

```
from pyspark.sql import SparkSession
# Initialize SparkSession
spark = SparkSession.builder.appName("example").getOrCreate()
# Data as a list of tuples
data = [("James", "Smith", "USA", "CA"), 
         ("Michael", "Rose", "USA", "NY"),
         ("Robert", "Williams", "USA", "CA"), 
         ("Maria", "Jones", "USA", "NY")]
# Columns
columns = ["firstname", "lastname", "country", "state"]
# Create DataFrame
df = spark.createDataFrame(data, schema=columns)
# Show DataFrame
df.show()
```

Output:

![captionless image](https://miro.medium.com/v2/resize:fit:998/format:webp/1*qEXMlYx-tFMYhWQsRJeFQg.png)

**DataFrame — groupBy():**

Now that we have our DataFrame, let’s move on to the ‘groupBy()’ function. The ‘groupBy()’ function is used to group the DataFrame by one or more columns and then apply aggregation functions on the grouped data. This is particularly useful for summarizing data.

**Example:**

Let’s group the DataFrame by the ‘country’ column and count the number of occurrences for each country:

```
# Group by 'country' and count the number of occurrences
df.groupBy("country").count().show()
```

**Output:**

![captionless image](https://miro.medium.com/v2/resize:fit:456/format:webp/1*TsAdE_nDxFFWBWlNLhL_ZA.png)

In this example, all rows in our DataFrame have the ‘country’ set as ‘USA’, so the count result is 4.

**DataFrame — join():**

The join() function is used to combine two DataFrames based on a condition, similar to SQL JOIN operations. It supports different join types like inner, outer, left, and right.

**Example:**

Let’s create a second DataFrame and perform an inner join on the ‘state’ column:

```
# Data for the second DataFrame
data2 = [("CA", "California"), ("NY", "New York")]
columns2 = ["state", "state_name"]
# Create second DataFrame
df2 = spark.createDataFrame(data2, schema=columns2)
# Perform an inner join on 'state'
df.join(df2, on="state", how="inner").show()
```

Output:

![captionless image](https://miro.medium.com/v2/resize:fit:1254/format:webp/1*RTQv0OAUJ1Hkb-EWBzBCJQ.png)

**DataFrame — map() vs mapPartitions():**

**map():** Applies a function to each element of the DataFrame individually. This is suitable for element-wise operations.
**mapPartitions():** Applies a function to each partition of the DataFrame. This is beneficial for operations that can be optimized by processing data in chunks.

Before using map() or mapPartitions(), we need to convert our DataFrame to an RDD:

Example:

```
# Convert DataFrame to RDD
rdd = df.rdd.map(lambda row: row.state)
# map example
mapped_rdd = rdd.map(lambda x: x + "_mapped")
print(mapped_rdd.collect())
# mapPartitions example
partitioned_rdd = rdd.mapPartitions(lambda iter: [sum(len(x) for x in iter)])
print(partitioned_rdd.collect())
```

**Output:**

[‘CA_mapped’, ‘NY_mapped’, ‘CA_mapped’, ‘NY_mapped’]
[4, 4] # Sum of string lengths in each partition

**DataFrame — foreach() vs foreachPartition():**

**foreach():** Applies a function to each row of the DataFrame. Suitable for operations that need to be applied to each row individually.
**foreachPartition():** Applies a function to each partition of the DataFrame. Useful for operations that benefit from processing data in chunks, like batch updates.

**Example:**

```
# foreach example
df.foreach(lambda row: print(row))
# foreachPartition example
df.foreachPartition(lambda iter: [print(row) for row in iter])
```

**Output:**

Row(firstname=’James’, lastname=’Smith’, country=’USA’, state=’CA’)
Row(firstname=’Michael’, lastname=’Rose’, country=’USA’, state=’NY’)

**DataFrame — pivot():**

The pivot() function is used to rotate data in a DataFrame, transforming rows into columns. This is useful for creating contingency tables or cross-tabulations.

**Example:**

```
# Pivot the DataFrame by 'country' and 'state'
df.groupBy("country").pivot("state").count().show()
```

**Output:**

![captionless image](https://miro.medium.com/v2/resize:fit:572/format:webp/1*JM-YgSYvvqkcgSCB1F-cTw.png)

**DataFrame — union():**

The union() function is used to combine two DataFrames with the same schema, appending the rows of one DataFrame to another.

**Example:**

```
# Create two DataFrames
data1 = [("James", "Smith", "USA", "CA"), ("Michael", "Rose", "USA", "NY")]
data2 = [("Robert", "Williams", "USA", "CA"), ("Maria", "Jones", "USA", "NY")]
df1 = spark.createDataFrame(data1, schema=columns)
df2 = spark.createDataFrame(data2, schema=columns)
# Union the DataFrames
df_union = df1.union(df2)
df_union.show()
```

**Output:**

![captionless image](https://miro.medium.com/v2/resize:fit:996/format:webp/1*ZrKqG2W_qG2UwCiyiMEQfg.png)

**DataFrame — collect():**

The collect() function retrieves all elements of the DataFrame to the driver node as a list of rows. This is useful for small datasets or for debugging but should be used cautiously with large datasets as it can lead to memory issues.

Example:

```
# Collect the data to the driver
collected_data = df.collect()
print(collected_data)
```

**Output:**

[Row(firstname=’James’, lastname=’Smith’, country=’USA’, state=’CA’),
Row(firstname=’Michael’, lastname=’Rose’, country=’USA’, state=’NY’),
Row(firstname=’Robert’, lastname=’Williams’, country=’USA’, state=’CA’),
Row(firstname=’Maria’, lastname=’Jones’, country=’USA’, state=’NY’)]

**DataFrame — udf():**

A udf() (User-Defined Function) allows you to define custom functions to apply on DataFrame columns. UDFs are useful when you need to apply complex logic that isn’t supported by PySpark’s built-in functions.

**Example:**

```
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
# Define a custom function
def to_upper(s):
 return s.upper()
# Register the function as a UDF
udf_upper = udf(to_upper, StringType())
# Apply the UDF
df = df.withColumn("state_upper", udf_upper(col("state")))
df.show()
```

**Output:**

![captionless image](https://miro.medium.com/v2/resize:fit:1320/format:webp/1*XbrvYt3tWo8AMsPYTl9y-Q.png)

**Conclusion:**

In this article, we’ve explored some of the most essential PySpark DataFrame functions that are crucial for data manipulation and analysis in a distributed environment. Starting from creating a DataFrame, we demonstrated how to group, join, map, and transform data using powerful functions like groupBy(), join(), map(), and pivot(). We also discussed the use of union(), collect(), and udf() functions, each serving a specific purpose in the data processing pipeline.

Stay tuned for more data engineering and spark related articles.
