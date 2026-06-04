# Elasticsearch Query DSL Logs Exercises

One-hour beginner practice on Docker Compose logs indexed by Logstash into `app-logs-*`.

These exercises use the real Docker GELF log data sent by the remote stack. In this setup, Elasticsearch container logs are forwarded to Logstash, and Logstash indexes them into Elasticsearch.

## Data Fields

The logs look like this:

| Field | Example | Use |
| --- | --- | --- |
| `@timestamp` | `2026-06-04T10:41:09.196Z` | Event time |
| `created` | `2026-06-04T10:40:18.367943377Z` | Docker container creation time |
| `message` | `Profiling is enabled` | Log text |
| `level` | `INFO`, `WARN`, `ERROR` | Log severity created by Logstash |
| `gelf_level` | `6` | Original GELF numeric log level |
| `service` | `es-training-elasticsearch` | Service name added by Logstash |
| `container_service` | `es-training-elasticsearch` | Container/service name from Docker |
| `container_name` | `es-training-elasticsearch` | Docker container name |
| `tag` | `es-training-elasticsearch` | Docker logging tag |
| `com.docker.compose.service` | `elasticsearch` | Compose service name |
| `com.docker.compose.project` | `elasticsearch-training` | Compose project name |
| `event_source` | `docker-compose` | Source marker added by Logstash |
| `training_stack` | `elasticsearch-training` | Stack marker added by Logstash |
| `image_name` | `docker.elastic.co/elasticsearch/elasticsearch:8.13.0` | Docker image |
| `host` | `vmi2068386.contaboserver.net` | Remote server host |
| `source_host` | `172.19.0.1` | Docker bridge source host |

Use this index pattern:

```http
app-logs-*
```

If the mapping shows fields such as `service.keyword`, `level.keyword`, or `container_name.keyword`, use those fields for exact `term`, `terms`, and aggregation queries.

## Timing

| Time | Topic |
| --- | --- |
| 0-10 min | Mapping and first search |
| 10-25 min | `match`, `match_phrase`, `term` |
| 25-40 min | `terms`, `range`, `bool` |
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
GET /app-logs-*/_field_caps?fields=@timestamp,created,message,level,gelf_level,service,container_name,container_service,tag,event_source,training_stack,com.docker.compose.service,image_name,host
```

## 2. First Search With `match_all`

`match_all` returns logs without filtering.

### Exercise

Return logs from `app-logs-*`.

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

Find logs where the message contains `profiling`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "match": {
      "message": "profiling"
    }
  }
}
```

## 4. Phrase Search With `match_phrase`

Use `match_phrase` when words must appear together in the same order.

### Exercise

Find logs containing the exact phrase `Profiling is enabled`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "match_phrase": {
      "message": "Profiling is enabled"
    }
  }
}
```

## 5. Exact Match With `term`

Use `term` for exact values.

### Exercise

Find logs where `service` is `es-training-elasticsearch`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "term": {
      "service": "es-training-elasticsearch"
    }
  }
}
```

If your mapping uses keyword sub-fields:

```json
{
  "query": {
    "term": {
      "service.keyword": "es-training-elasticsearch"
    }
  }
}
```

## 6. Exact Match On Compose Service

Docker labels are also searchable.

### Exercise

Find logs where the Compose service is `elasticsearch`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "term": {
      "com.docker.compose.service": "elasticsearch"
    }
  }
}
```

If your mapping uses keyword sub-fields:

```json
{
  "query": {
    "term": {
      "com.docker.compose.service.keyword": "elasticsearch"
    }
  }
}
```

## 7. Multiple Exact Values With `terms`

Use `terms` when a field can match one value from a list.

### Exercise

Find logs where `level` is `INFO` or `WARN`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "terms": {
      "level": [
        "INFO",
        "WARN"
      ]
    }
  }
}
```

## 8. Date Range

Use `range` on `@timestamp` to search a time window.

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

## 9. Numeric Range

`gelf_level` is a number, so it can be queried with `range`.

### Exercise

Find logs where `gelf_level` is less than or equal to `6`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "range": {
      "gelf_level": {
        "lte": 6
      }
    }
  }
}
```

## 10. Combine Filters With `bool`

Use `bool` with `filter` when all conditions must be true.

### Exercise

Find logs that are:

- from service `es-training-elasticsearch`
- level `INFO`
- from the last 15 minutes

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "service": "es-training-elasticsearch"
          }
        },
        {
          "term": {
            "level": "INFO"
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": "now-15m",
              "lte": "now"
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

Find Elasticsearch service logs where the message contains `enabled`.

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "enabled"
          }
        }
      ],
      "filter": [
        {
          "term": {
            "service": "es-training-elasticsearch"
          }
        }
      ]
    }
  }
}
```

## 12. Count Logs By Level

Aggregations summarize logs instead of returning individual documents.

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

If your mapping uses keyword sub-fields:

```json
{
  "size": 0,
  "aggs": {
    "logs_by_level": {
      "terms": {
        "field": "level.keyword",
        "size": 10
      }
    }
  }
}
```

## 13. Count Logs By Container

### Exercise

Count logs by `container_name`.

### Answer

```http
GET /app-logs-*/_search
{
  "size": 0,
  "aggs": {
    "logs_by_container": {
      "terms": {
        "field": "container_name",
        "size": 10
      }
    }
  }
}
```

## 14. Average GELF Level

Metric aggregations calculate numeric values.

### Exercise

Calculate the average `gelf_level`.

### Answer

```http
GET /app-logs-*/_search
{
  "size": 0,
  "aggs": {
    "average_gelf_level": {
      "avg": {
        "field": "gelf_level"
      }
    }
  }
}
```

## 15. Count Logs Over Time

Use `date_histogram` to see how logs arrive over time.

### Exercise

Count logs per minute.

### Answer

```http
GET /app-logs-*/_search
{
  "size": 0,
  "aggs": {
    "logs_per_minute": {
      "date_histogram": {
        "field": "@timestamp",
        "fixed_interval": "1m"
      }
    }
  }
}
```

## 16. Final Recap Query

### Exercise

Find recent Elasticsearch logs:

- service is `es-training-elasticsearch`
- level is `INFO` or `WARN`
- message contains `enabled`
- event happened in the last hour

### Answer

```http
GET /app-logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "enabled"
          }
        }
      ],
      "filter": [
        {
          "term": {
            "service": "es-training-elasticsearch"
          }
        },
        {
          "terms": {
            "level": [
              "INFO",
              "WARN"
            ]
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
