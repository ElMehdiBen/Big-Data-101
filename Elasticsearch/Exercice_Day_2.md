# Elasticsearch Training Exercise

In this exercise, you will:
1. Use a script to read transaction data from a URL and index it into Elasticsearch.
2. Answer a set of query and aggregation questions to analyze the data.

## Part 1: Indexing Data into Elasticsearch

Create a small script that reads JSON data from the given URL and sends it to an Elasticsearch instance.

### Sample Data
The data is a list of transactions in JSON format. Here's an excerpt (full data provided separately):

```json
[
  {
    "transaction_id": 1,
    "transaction_date": "9/17/2022",
    "customer_id": 1,
    "product_id": 1,
    "quantity": 53,
    "unit_price": 804.34,
    "total_price": 2520.4,
    "payment_method": "PayPal",
    "shipping_address": "2282 Meadow Vale Trail",
    "status": "pending"
  }
]
```

## Part 2: Querying and Aggregating Data

Now that the data is indexed, use Elasticsearch queries to answer the following questions. Write the queries in the Elasticsearch Query DSL (JSON format).

### Query Questions
1. How many transactions used the "PayPal" payment method?
2. Find all transactions with a status of "shipped".
3. How many transactions occurred on "8/21/2022"?
4. Which transactions have a total price greater than $5000?
5. Find all transactions for customer ID 5.
6. How many transactions have a quantity less than 50?
7. List all transactions where the payment method is "debit card" and the status is "delivered".
8. Find the transaction with the highest total price.
9. How many transactions have a unit price between $500 and $800?
10. List all transactions with a shipping address containing the word "Park".

### Aggregation Questions
1. What is the total revenue (sum of `total_price`) for each payment method?
2. What is the average `quantity` of items per transaction status (e.g., pending, shipped, delivered)?
3. Group transactions by month (based on `transaction_date`) and calculate the total number of transactions per month.

### Submission
- Provide the Elasticsearch Query DSL for each question.
- Test your queries against the indexed data to ensure correctness.
- Submit your answers in a separate Markdown file or as part of this document.

### Notes for You
- The questions are designed to cover basic queries (match, range, term) and aggregations (terms, sum, avg), which are suitable for Elasticsearch beginners.


Happy querying!
