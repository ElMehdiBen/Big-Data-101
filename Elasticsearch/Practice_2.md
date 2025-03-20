Let’s dive into a practical, hands-on guide focused specifically on **Searching and Querying** in Elasticsearch. This will build on the foundational concepts from the previous guide (e.g., creating an index and mapping) and provide a set of practical exercises to help you understand how to search and query data effectively. We’ll cover different types of queries, filters, and techniques to retrieve and analyze data, with examples and explanations for each.

---

### Practical Guide to Searching and Querying in Elasticsearch

#### Prerequisites
- **Elasticsearch Running**: Ensure Elasticsearch is running on `localhost:9200`.
- **Sample Data**: We’ll use the `products` index from the previous guide. If you don’t have it, set it up with the following commands to create the index and add some sample data.

**Create the Index with Mapping**:
```bash
PUT /products
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "price": { "type": "float" },
      "in_stock": { "type": "boolean" },
      "category": { "type": "keyword" },
      "description": { "type": "text" }
    }
  }
}
```

**Index Sample Documents**:
```bash
PUT /products/_doc/1
{
  "name": "Laptop",
  "price": 999.99,
  "in_stock": true,
  "category": "Electronics",
  "description": "A high-performance laptop for gaming and work."
}

PUT /products/_doc/2
{
  "name": "Mouse",
  "price": 29.99,
  "in_stock": false,
  "category": "Electronics",
  "description": "A wireless mouse with ergonomic design."
}

PUT /products/_doc/3
{
  "name": "Desk Chair",
  "price": 149.99,
  "in_stock": true,
  "category": "Furniture",
  "description": "Comfortable chair for long working hours."
}

PUT /products/_doc/4
{
  "name": "Monitor",
  "price": 249.99,
  "in_stock": true,
  "category": "Electronics",
  "description": "4K monitor for crisp visuals."
}
```

---

### 1. Understanding Search Basics

#### 1.1 The `_search` Endpoint
- **Why**: The `_search` endpoint is the primary way to query data in Elasticsearch.
- **Command** (Basic Search for All Documents):
  ```bash
  GET /products/_search
  {
    "query": {
      "match_all": {}
    }
  }
  ```
- **Expected Response**:
  ```json
  {
    "hits": {
      "total": { "value": 4, "relation": "eq" },
      "hits": [
        { "_id": "1", "_source": { "name": "Laptop", ... } },
        { "_id": "2", "_source": { "name": "Mouse", ... } },
        { "_id": "3", "_source": { "name": "Desk Chair", ... } },
        { "_id": "4", "_source": { "name": "Monitor", ... } }
      ]
    }
  }
  ```
- **Explanation**:
  - `match_all`: Returns all documents in the index.
  - `hits`: Contains the matching documents, with `_source` showing the original document data.
  - `total.value`: The total number of matching documents.

---

### 2. Full-Text Search Queries

#### 2.1 Match Query (Full-Text Search)
- **Why**: Search for documents containing a specific term in a text field (e.g., `name` or `description`).
- **Command**:
  ```bash
  GET /products/_search
  {
    "query": {
      "match": {
        "description": "gaming"
      }
    }
  }
  ```
- **Expected Response**:
  ```json
  {
    "hits": {
      "total": { "value": 1, ... },
      "hits": [
        {
          "_id": "1",
          "_score": 0.2876821,
          "_source": {
            "name": "Laptop",
            "description": "A high-performance laptop for gaming and work."
          }
        }
      ]
    }
  }
  ```
- **Explanation**:
  - `match`: Performs a full-text search on the `description` field.
  - Elasticsearch tokenizes the text (e.g., "gaming" matches in the `description` of the laptop).
  - `_score`: Indicates relevance (higher score = better match).

#### 2.2 Multi-Match Query (Search Across Multiple Fields)
- **Why**: Search for a term across multiple fields (e.g., `name` and `description`).
- **Command**:
  ```bash
  GET /products/_search
  {
    "query": {
      "multi_match": {
        "query": "wireless",
        "fields": ["name", "description"]
      }
    }
  }
  ```
- **Expected Response**:
  ```json
  {
    "hits": {
      "total": { "value": 1, ... },
      "hits": [
        {
          "_id": "2",
          "_source": {
            "name": "Mouse",
            "description": "A wireless mouse with ergonomic design."
          }
        }
      ]
    }
  }
  ```

---

### 3. Exact Match Queries

#### 3.1 Term Query (Exact Match for Keyword Fields)
- **Why**: Use for exact matches on `keyword` fields like `category`.
- **Command**:
  ```bash
  GET /products/_search
  {
    "query": {
      "term": {
        "category": "Electronics"
      }
    }
  }
  ```
- **Expected Response**:
  ```json
  {
    "hits": {
      "total": { "value": 3, ... },
      "hits": [
        { "_id": "1", "_source": { "name": "Laptop", ... } },
        { "_id": "2", "_source": { "name": "Mouse", ... } },
        { "_id": "4", "_source": { "name": "Monitor", ... } }
      ]
    }
  }
  ```
- **Explanation**:
  - `term`: Matches exact values (case-sensitive for `keyword` fields).
  - Useful for structured fields like `category`, not for full-text fields like `description`.

#### 3.2 Terms Query (Match Multiple Values)
- **Why**: Find documents matching any of a list of values.
- **Command**:
  ```bash
  GET /products/_search
  {
    "query": {
      "terms": {
        "category": ["Electronics", "Furniture"]
      }
    }
  }
  ```
- **Expected Response**:
  - Returns all 4 documents since they all belong to either "Electronics" or "Furniture".

---

### 4. Combining Queries (Boolean Queries)

#### 4.1 Bool Query (Must, Should, Must Not)
- **Why**: Combine multiple conditions for more complex searches.
- **Command** (Find in-stock electronics under $500):
  ```bash
  GET /products/_search
  {
    "query": {
      "bool": {
        "must": [
          { "term": { "category": "Electronics" } },
          { "term": { "in_stock": true } },
          { "range": { "price": { "lte": 500 } } }
        ]
      }
    }
  }
  ```
- **Expected Response**:
  ```json
  {
    "hits": {
      "total": { "value": 1, ... },
      "hits": [
        {
          "_id": "4",
          "_source": {
            "name": "Monitor",
            "price": 249.99,
            "in_stock": true,
            "category": "Electronics"
          }
        }
      ]
    }
  }
  ```
- **Explanation**:
  - `bool`: Combines conditions.
  - `must`: All conditions must match (AND).
  - `range`: Filters `price` to be less than or equal to 500 (`lte`).
  - You can also use `should` (OR) or `must_not` (NOT).

---

### 5. Filtering Results

#### 5.1 Filter Context (Efficient Filtering)
- **Why**: Filters are faster than queries because they don’t calculate relevance scores.
- **Command** (Filter for in-stock products):
  ```bash
  GET /products/_search
  {
    "query": {
      "bool": {
        "filter": [
          { "term": { "in_stock": true } }
        ]
      }
    }
  }
  ```
- **Expected Response**:
  - Returns the Laptop, Desk Chair, and Monitor (all have `in_stock: true`).
- **Explanation**:
  - `filter`: Applies conditions without affecting the score.
  - Ideal for yes/no conditions like `in_stock`.

---

### 6. Sorting and Pagination

#### 6.1 Sort Results
- **Why**: Order results by a field (e.g., `price`).
- **Command** (Sort by price, ascending):
  ```bash
  GET /products/_search
  {
    "query": { "match_all": {} },
    "sort": [
      { "price": { "order": "asc" } }
    ]
  }
  ```
- **Expected Response**:
  - Returns documents in order: Mouse ($29.99), Desk Chair ($149.99), Monitor ($249.99), Laptop ($999.99).

#### 6.2 Paginate Results
- **Why**: Limit the number of results and fetch them in chunks.
- **Command** (Get 2 results, starting from the 2nd result):
  ```bash
  GET /products/_search
  {
    "query": { "match_all": {} },
    "from": 1,
    "size": 2
  }
  ```
- **Explanation**:
  - `from`: Starting position (0-based index).
  - `size`: Number of results to return.
  - This skips the first result and returns the next 2.

---

### 7. Highlighting Search Results

#### 7.1 Highlight Matching Terms
- **Why**: Show which parts of the document matched the query.
- **Command**:
  ```bash
  GET /products/_search
  {
    "query": {
      "match": {
        "description": "ergonomic"
      }
    },
    "highlight": {
      "fields": {
        "description": {}
      }
    }
  }
  ```
- **Expected Response**:
  ```json
  {
    "hits": {
      "hits": [
        {
          "_id": "2",
          "_source": { "name": "Mouse", ... },
          "highlight": {
            "description": ["A wireless mouse with <em>ergonomic</em> design."]
          }
        }
      ]
    }
  }
  ```
- **Explanation**:
  - `highlight`: Wraps matching terms in `<em>` tags (customizable).

---

### 8. Aggregations with Search

#### 8.1 Combine Search with Aggregations
- **Why**: Search for documents and analyze the results (e.g., count by category).
- **Command** (Find in-stock products and group by category):
  ```bash
  GET /products/_search
  {
    "query": {
      "bool": {
        "filter": [
          { "term": { "in_stock": true } }
        ]
      }
    },
    "aggs": {
      "by_category": {
        "terms": {
          "field": "category"
        }
      }
    }
  }
  ```
- **Expected Response**:
  ```json
  {
    "hits": { ... },
    "aggregations": {
      "by_category": {
        "buckets": [
          { "key": "Electronics", "doc_count": 2 },
          { "key": "Furniture", "doc_count": 1 }
        ]
      }
    }
  }
  ```

---

### 9. Tips for Effective Searching

- **Use `explain` to Debug**:
  ```bash
  GET /products/_search
  {
    "explain": true,
    "query": { "match": { "description": "gaming" } }
  }
  ```
  - Shows how the score was calculated.

- **Analyze Text Fields**:
  - Use `GET /products/_analyze` to see how text is tokenized (e.g., `{"text": "gaming laptop"}`).

- **Boost Fields**:
  - In a `multi_match` query, boost a field’s importance:
    ```json
    "fields": ["name^2", "description"]
    ```
    - `^2` makes matches in `name` twice as important.

---

### 10. Common Querying Pitfalls

- **Text vs. Keyword**: Don’t use `term` on `text` fields (e.g., `description`)—it won’t match due to tokenization. Use `match` instead.
- **Case Sensitivity**: `term` queries on `keyword` fields are case-sensitive. Use `match` for case-insensitive searches.
- **Performance**: Avoid deep pagination (`from` > 10,000); use `search_after` for large datasets.

---

This guide provides a practical set of exercises for searching and querying in Elasticsearch, covering full-text search, exact matches, filtering, sorting, and aggregations. Practice these examples, tweak the queries, and explore the results to build confidence. Let me know if you’d like to dive deeper into a specific query type or advanced topics like fuzzy search or scripting!
