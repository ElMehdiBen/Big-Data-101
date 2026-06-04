# Elasticsearch Query DSL Logs Exercises

One-hour beginner practice on Docker Compose logs indexed by Logstash into `app-logs-*`.

The goal is to discover Elasticsearch Query DSL using simple log examples. Each exercise has the answer directly below it.

## Data Fields

The Logstash pipeline sends logs with these main fields:

| Field | Example | Use |
| --- | --- | --- |
| `@timestamp` | `2026-06-04T10:00:00Z` | Time filtering |
| `service` | `checkout`, `auth`, `search`, `payments` | Exact service filtering |
| `level` | `INFO`, `WARN`, `ERROR` | Exact severity filtering |
| `message` | `Payment gateway timeout after 2400ms` | Full-text search |
| `latency_ms` | `2400` | Numeric range queries and metrics |
| `status_code` | `200`, `409`, `503`, `504` | Numeric filtering |
| `trace_id` | `trc-pay-2400` | Exact lookup |

Use this index pattern:

```http
app-logs-*
```

If the mapping shows fields such as `service.keyword` or `level.keyword`, use those fields for exact `term`, `terms`, and aggregation queries.

## Timing

| Time | Topic |
| --- | --- |
| 0-10 min | Mapping and first search |
| 10-25 min | `match`, `term`, `terms` |
| 25-40 min | `range` and `bool` |
| 40-55 min | Aggregations |
| 55-60 min | Final recap |

## 1. Inspect The Mapping

Before writing queries, check which fields exist and how Elasticsearch mapped them.

### Exercise

Inspect the mapping for `app-logs-*`.

### Answer

```http
GET /app-logs-*/_mapping
```

Optional compact view:

```http
GET /app-logs-*/_field_caps?fields=@timestamp,service,level,message,latency_ms,status_code,trace_id
```

## 2. First Search With `match_all`

`match_all` returns documents without filtering.

### Exercise

Return any logs from `app-logs-*`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "match_all": {}
  }
}
```

## 3. Full-Text Search With `match`

Use `match` for text fields such as `message`.

### Exercise

Find logs where the message contains `timeout`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "match": {
      "message": "timeout"
    }
  }
}
```

## 4. Phrase Search With `match_phrase`

Use `match_phrase` when the words must appear together in the same order.

### Exercise

Find logs containing the phrase `gateway timeout`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "match_phrase": {
      "message": "gateway timeout"
    }
  }
}
```

## 5. Exact Match With `term`

Use `term` for exact values.

### Exercise

Find logs from the `checkout` service.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "term": {
      "service": "checkout"
    }
  }
}
```

If your mapping uses keyword sub-fields:

```json
{
  "query": {
    "term": {
      "service.keyword": "checkout"
    }
  }
}
```

## 6. Multiple Exact Values With `terms`

Use `terms` when a field can match one value from a list.

### Exercise

Find logs where `level` is `WARN` or `ERROR`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "terms": {
      "level": [
        "WARN",
        "ERROR"
      ]
    }
  }
}
```

## 7. Numeric Range On Latency

Use `range` for numeric comparisons.

### Exercise

Find logs where `latency_ms` is greater than or equal to `1000`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "range": {
      "latency_ms": {
        "gte": 1000
      }
    }
  }
}
```

## 8. Numeric Range On Status Code

Status codes from `500` to `599` usually represent server errors.

### Exercise

Find logs where `status_code` is between `500` and `599`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "range": {
      "status_code": {
        "gte": 500,
        "lte": 599
      }
    }
  }
}
```

## 9. Date Range

`range` also works with date fields.

### Exercise

Find logs from the last 15 minutes.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-15m",
        "lte": "now"
      }
    }
  }
}
```

## 10. Combine Filters With `bool`

Use `bool` with `filter` when all conditions must be true.

### Exercise

Find logs that are:

- from service `checkout`
- level `WARN`
- latency greater than or equal to `1000`

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "service": "checkout"
          }
        },
        {
          "term": {
            "level": "WARN"
          }
        },
        {
          "range": {
            "latency_ms": {
              "gte": 1000
            }
          }
        }
      ]
    }
  }
}
```

## 11. Combine Text Search And Filter

Use `must` for text search and `filter` for exact conditions.

### Exercise

Find logs from the `payments` service where the message contains `failed`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "failed"
          }
        }
      ],
      "filter": [
        {
          "term": {
            "service": "payments"
          }
        }
      ]
    }
  }
}
```

## 12. Count Logs By Service

Aggregations summarize documents instead of focusing on individual hits.

### Exercise

Count logs by `service`.

### Answer

```http
GET /app-logs-*/_search
{
  "size": 0,
  "aggs": {
    "logs_by_service": {
      "terms": {
        "field": "service",
        "size": 10
      }
    }
  }
}
```

If your mapping uses keyword sub-fields:

```json
{
  "size": 0,
  "aggs": {
    "logs_by_service": {
      "terms": {
        "field": "service.keyword",
        "size": 10
      }
    }
  }
}
```

## 13. Count Logs By Level

### Exercise

Count logs by `level`.

### Answer

```http
GET /app-logs-*/_search
{
  "size": 0,
  "aggs": {
    "logs_by_level": {
      "terms": {
        "field": "level",
        "size": 10
      }
    }
  }
}
```

## 14. Average Latency

Metric aggregations calculate numeric values.

### Exercise

Calculate the average `latency_ms`.

### Answer

```http
GET /app-logs-*/_search
{
  "size": 0,
  "aggs": {
    "average_latency": {
      "avg": {
        "field": "latency_ms"
      }
    }
  }
}
```

## 15. Average Latency By Service

You can put a metric aggregation inside a bucket aggregation.

### Exercise

For each service, calculate average latency.

### Answer

```http
GET /app-logs-*/_search
{
  "size": 0,
  "aggs": {
    "by_service": {
      "terms": {
        "field": "service",
        "size": 10
      },
      "aggs": {
        "average_latency": {
          "avg": {
            "field": "latency_ms"
          }
        }
      }
    }
  }
}
```

## 16. Final Recap Query

### Exercise

Find important slow logs:

- `level` is `WARN` or `ERROR`
- `latency_ms` is greater than or equal to `1000`
- event happened in the last hour

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "terms": {
            "level": [
              "WARN",
              "ERROR"
            ]
          }
        },
        {
          "range": {
            "latency_ms": {
              "gte": 1000
            }
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": "now-1h",
              "lte": "now"
            }
          }
        }
      ]
    }
  }
}
```
