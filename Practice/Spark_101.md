# Essential Spark DataFrame Functions

This document covers some of the most important Spark DataFrame functions to know when working with data in PySpark.

---

### 1. Creating DataFrames

- **`spark.createDataFrame(data, schema=None)`**: Creates a DataFrame from a list of tuples, RDD, or Pandas DataFrame.
  
  ```python
  data = [(1, "Alice"), (2, "Bob")]
  df = spark.createDataFrame(data, ["id", "name"])
  ```

---

### 2. Showing and Printing Data

- **`df.show(n=20, truncate=True)`**: Displays the first `n` rows of the DataFrame.
  
  ```python
  df.show(5)
  ```

- **`df.printSchema()`**: Prints the schema of the DataFrame in a tree format.
  
  ```python
  df.printSchema()
  ```

---

### 3. Selecting Data

- **`df.select(*cols)`**: Selects specific columns in the DataFrame.

  ```python
  df.select("name").show()
  ```

- **`df.selectExpr(*expr)`**: Selects with SQL expressions, useful for complex transformations.
  
  ```python
  df.selectExpr("name as user_name", "id + 1 as incremented_id").show()
  ```

---

### 4. Filtering Rows

- **`df.filter(condition)`**: Filters rows based on a condition.

  ```python
  df.filter(df["id"] > 1).show()
  ```

- **`df.where(condition)`**: Another way to filter rows (same as `filter`).

  ```python
  df.where("id > 1").show()
  ```

---

### 5. Sorting Data

- **`df.orderBy(*cols, ascending=True)`**: Sorts the DataFrame by specified columns.
  
  ```python
  df.orderBy("name", ascending=False).show()
  ```

- **`df.sort(*cols, ascending=True)`**: Alias for `orderBy`.

---

### 6. Aggregating Data

- **`df.groupBy(*cols).agg(*exprs)`**: Groups data by columns and applies aggregation functions.

  ```python
  df.groupBy("id").count().show()
  ```

- **`df.agg(*exprs)`**: Applies aggregate functions without grouping.

  ```python
  from pyspark.sql import functions as F
  df.agg(F.avg("id")).show()
  ```

---

### 7. Joins

- **`df.join(other, on=None, how="inner")`**: Joins two DataFrames based on a condition.

  ```python
  df1.join(df2, df1["id"] == df2["id"], "inner").show()
  ```

- Common join types include `inner`, `left`, `right`, `outer`.

---

### 8. Adding and Renaming Columns

- **`df.withColumn(colName, col)`**: Adds a new column or replaces an existing one.

  ```python
  df.withColumn("new_col", F.lit("constant_value")).show()
  ```

- **`df.withColumnRenamed(existing, new)`**: Renames a column.

  ```python
  df.withColumnRenamed("name", "first_name").show()
  ```

---

### 9. Removing Columns

- **`df.drop(*cols)`**: Drops specified columns.

  ```python
  df.drop("column_name").show()
  ```

---

### 10. Window Functions

Window functions allow for calculations across specific "windows" or subsets of rows.

- **`F.row_number().over(windowSpec)`**: Assigns a row number within a window.
  
  ```python
  from pyspark.sql.window import Window
  windowSpec = Window.partitionBy("name").orderBy("id")
  df.select("id", "name", F.row_number().over(windowSpec)).show()
  ```

---

### 11. Handling Missing Data

- **`df.fillna(value, subset=None)`**: Replaces `NULL` values with a specified value.

  ```python
  df.fillna({"name": "unknown"}).show()
  ```

- **`df.dropna(how="any", subset=None)`**: Drops rows containing `NULL` values. The parameter `how` can be `any` or `all`.

  ```python
  df.dropna().show()
  ```

---

### 12. DataFrame Metadata

- **`df.count()`**: Returns the number of rows in the DataFrame.

  ```python
  df.count()
  ```

- **`df.columns`**: Returns the list of column names.

  ```python
  df.columns
  ```

- **`df.dtypes`**: Returns the column names and types.

  ```python
  df.dtypes
  ```

---

### 13. SQL Queries

- **`df.createOrReplaceTempView(name)`**: Creates a temporary SQL view for the DataFrame.

  ```python
  df.createOrReplaceTempView("people")
  spark.sql("SELECT * FROM people WHERE id > 1").show()
  ```

---

This guide provides a foundation for working with Spark DataFrames in PySpark. Practice each function to become familiar with its syntax and capabilities!
