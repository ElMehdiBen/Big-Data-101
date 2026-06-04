# Elasticsearch Transactions Bool And Aggregations Answers

Answers for `Elasticsearch Transactions Bool Aggregations Questions.md`.

Use this index pattern:

```http
app-transactions-*
```

Exercise day:

```text
2026-06-04T00:00:00Z to before 2026-06-05T00:00:00Z
```

## 1. Unique Card Users For The Day

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "payment_method": "card"
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": "2026-06-04T00:00:00Z",
              "lt": "2026-06-05T00:00:00Z"
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "unique_card_customers": {
      "cardinality": {
        "field": "customer_id"
      }
    }
  }
}
```

## 2. Status Breakdown For High-Value Card Payments

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "payment_method": "card"
          }
        },
        {
          "range": {
            "amount": {
              "gte": 500
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "by_status": {
      "terms": {
        "field": "status",
        "size": 10
      }
    }
  }
}
```

## 3. Captured Amounts By Currency

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "term": {
      "status": "captured"
    }
  },
  "aggs": {
    "by_currency": {
      "terms": {
        "field": "currency",
        "size": 10
      },
      "aggs": {
        "total_amount": {
          "sum": {
            "field": "amount"
          }
        },
        "average_amount": {
          "avg": {
            "field": "amount"
          }
        }
      }
    }
  }
}
```

## 4. High-Risk Failed Or Declined Transactions By Provider

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "terms": {
            "status": [
              "failed",
              "declined"
            ]
          }
        },
        {
          "range": {
            "risk_score": {
              "gte": 0.8
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "by_provider": {
      "terms": {
        "field": "provider",
        "size": 10
      }
    }
  }
}
```

## 5. Average Latency For Successful Transactions By Payment Method

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "terms": {
      "status": [
        "authorized",
        "captured"
      ]
    }
  },
  "aggs": {
    "by_payment_method": {
      "terms": {
        "field": "payment_method",
        "size": 10
      },
      "aggs": {
        "average_latency_ms": {
          "avg": {
            "field": "latency_ms"
          }
        }
      }
    }
  }
}
```

## 6. Fraud Transactions By Country

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "term": {
      "fraud_flag": true
    }
  },
  "aggs": {
    "by_country": {
      "terms": {
        "field": "country",
        "size": 10
      }
    }
  }
}
```

## 7. Status Breakdown For Web And Mobile Channels

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "terms": {
      "channel": [
        "web",
        "mobile"
      ]
    }
  },
  "aggs": {
    "by_channel": {
      "terms": {
        "field": "channel",
        "size": 10
      },
      "aggs": {
        "by_status": {
          "terms": {
            "field": "status",
            "size": 10
          }
        }
      }
    }
  }
}
```

## 8. Total Transaction Amount Per Hour

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "range": {
      "@timestamp": {
        "gte": "2026-06-04T00:00:00Z",
        "lt": "2026-06-05T00:00:00Z"
      }
    }
  },
  "aggs": {
    "transactions_per_hour": {
      "date_histogram": {
        "field": "@timestamp",
        "fixed_interval": "1h"
      },
      "aggs": {
        "total_amount": {
          "sum": {
            "field": "amount"
          }
        }
      }
    }
  }
}
```

## 9. Card Network Breakdown For Declines And Chargebacks

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "payment_method": "card"
          }
        },
        {
          "terms": {
            "status": [
              "declined",
              "chargeback"
            ]
          }
        }
      ]
    }
  },
  "aggs": {
    "by_card_network": {
      "terms": {
        "field": "card_network",
        "size": 10
      }
    }
  }
}
```

## 10. High-Value Suspicious Payments By Provider

```http
GET /app-transactions-*/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "terms": {
            "status": [
              "declined",
              "failed",
              "chargeback"
            ]
          }
        },
        {
          "range": {
            "amount": {
              "gte": 1000
            }
          }
        },
        {
          "range": {
            "risk_score": {
              "gte": 0.85
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "by_provider": {
      "terms": {
        "field": "provider",
        "size": 10
      },
      "aggs": {
        "average_amount": {
          "avg": {
            "field": "amount"
          }
        },
        "maximum_amount": {
          "max": {
            "field": "amount"
          }
        },
        "average_risk_score": {
          "avg": {
            "field": "risk_score"
          }
        },
        "by_status": {
          "terms": {
            "field": "status",
            "size": 10
          }
        }
      }
    }
  }
}
```
