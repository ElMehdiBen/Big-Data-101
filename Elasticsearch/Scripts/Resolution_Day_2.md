
# Elasticsearch Training Exercise: Query Resolutions

This document provides the Elasticsearch Query DSL resolutions for the questions in the training exercise. Test these queries against the `transactions` index to verify the results.

## Query Questions

### 1. How many transactions used the "PayPal" payment method?
```json
{
  "query": {
    "match": {
      "payment_method": "PayPal"
    }
  }
}
```
- Use the `hits.total.value` from the response to get the count.

### 2. Find all transactions with a status of "shipped".
```json
{
  "query": {
    "term": {
      "status.keyword": "shipped"
    }
  }
}
```
- Use `.keyword` if `status` is a text field with an analyzer; otherwise, omit it.

### 3. How many transactions occurred on "8/21/2022"?
```json
{
  "query": {
    "match": {
      "transaction_date": "8/21/2022"
    }
  }
}
```
- Assumes `transaction_date` is indexed as a text or date field. For exact date matching, ensure proper date formatting in the index.

### 4. Which transactions have a total price greater than $5000?
```json
{
  "query": {
    "range": {
      "total_price": {
        "gt": 5000
      }
    }
  }
}
```

### 5. Find all transactions for customer ID 5.
```json
{
  "query": {
    "term": {
      "customer_id": 5
    }
  }
}
```

### 6. How many transactions have a quantity less than 50?
```json
{
  "query": {
    "range": {
      "quantity": {
        "lt": 50
      }
    }
  }
}
```
- Use `hits.total.value` for the count.

### 7. List all transactions where the payment method is "debit card" and the status is "delivered".
```json
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"payment_method.keyword": "debit card"}},
        {"term": {"status.keyword": "delivered"}}
      ]
    }
  }
}
```

### 8. Find the transaction with the highest total price.
```json
{
  "sort": [
    {
      "total_price": {
        "order": "desc"
      }
    }
  ],
  "size": 1
}
```

### 9. How many transactions have a unit price between $500 and $800?
```json
{
  "query": {
    "range": {
      "unit_price": {
        "gte": 500,
        "lte": 800
      }
    }
  }
}
```
- Use `hits.total.value` for the count.

### 10. List all transactions with a shipping address containing the word "Park".
```json
{
  "query": {
    "wildcard": {
      "shipping_address": "*Park*"
    }
  }
}
```
- Alternatively, use `match` if `shipping_address` is analyzed: `"query": {"match": {"shipping_address": "Park"}}`.

## Aggregation Questions

### 1. What is the total revenue (sum of `total_price`) for each payment method?
```json
{
  "aggs": {
    "by_payment_method": {
      "terms": {
        "field": "payment_method.keyword"
      },
      "aggs": {
        "total_revenue": {
          "sum": {
            "field": "total_price"
          }
        }
      }
    }
  }
}
```
- Results in `aggregations.by_payment_method.buckets` with `key` (payment method) and `total_revenue.value`.

### 2. What is the average `quantity` of items per transaction status?
```json
{
  "aggs": {
    "by_status": {
      "terms": {
        "field": "status.keyword"
      },
      "aggs": {
        "avg_quantity": {
          "avg": {
            "field": "quantity"
          }
        }
      }
    }
  }
}
```
- Results in `aggregations.by_status.buckets` with `key` (status) and `avg_quantity.value`.

### 3. Group transactions by month (based on `transaction_date`) and calculate the total number of transactions per month.
```json
{
  "aggs": {
    "by_month": {
      "date_histogram": {
        "field": "transaction_date",
        "calendar_interval": "month",
        "format": "MM/yyyy"
      }
    }
  }
}
```
- Assumes `transaction_date` is a date field. Results in `aggregations.by_month.buckets` with `key_as_string` (month) and `doc_count` (number of transactions).

---

### Notes
- If fields like `payment_method` or `status` are analyzed text fields, append `.keyword` to use the unanalyzed version for exact matching.
- For date-based queries/aggregations, ensure `transaction_date` is mapped as a `date` type in Elasticsearch. If it’s a string, you may need to reindex with proper mapping.
- We will test these queries in Elasticsearch environment (e.g., via Kibana Dev Tools) to validate against the sample data.
