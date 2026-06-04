# Elasticsearch Dev Tools Examples

Copy one block at a time into Kibana -> Dev Tools.

These examples follow the same training story as the slides: application logs from services such as `checkout`, `auth`, `search`, `payments`, and `recommendations`.

## 1. Cluster and Index Checks

```http
GET /

GET /_cluster/health

GET /_cat/nodes?v

GET /_cat/indices?v

GET /_cat/aliases?v
```

## 2. Clean Up Training Indices

Use this when you want to reset the hands-on examples.

```http
DELETE /app-logs-000001?ignore_unavailable=true

DELETE /app-logs-000002?ignore_unavailable=true

DELETE /mapping-conflict-demo?ignore_unavailable=true

DELETE /system-events?ignore_unavailable=true

DELETE /security-events?ignore_unavailable=true
```

## 3. Create an Index with Settings, Mapping, and Aliases

```http
PUT /app-logs-000001
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "aliases": {
    "app-logs": {},
    "app-logs-write": {
      "is_write_index": true
    }
  },
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "service": {
        "type": "keyword"
      },
      "env": {
        "type": "keyword"
      },
      "level": {
        "type": "keyword"
      },
      "message": {
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "latency_ms": {
        "type": "integer"
      },
      "status_code": {
        "type": "short"
      },
      "trace_id": {
        "type": "keyword"
      },
      "client_ip": {
        "type": "ip"
      },
      "location": {
        "type": "geo_point"
      }
    }
  }
}

GET /app-logs-000001/_mapping

GET /_cat/aliases/app-logs*?v
```

## 4. Index Single Documents

```http
POST /app-logs-write/_doc/evt-001
{
  "@timestamp": "2026-06-03T09:00:00Z",
  "service": "checkout",
  "env": "training",
  "level": "WARN",
  "message": "Payment gateway timeout after 2400ms",
  "latency_ms": 2400,
  "status_code": 504,
  "trace_id": "trc-1001",
  "client_ip": "41.92.113.12",
  "location": {
    "lat": 33.5731,
    "lon": -7.5898
  }
}

POST /app-logs-write/_doc/evt-002
{
  "@timestamp": "2026-06-03T09:01:30Z",
  "service": "search",
  "env": "training",
  "level": "INFO",
  "message": "Index refresh completed in 42ms",
  "latency_ms": 42,
  "status_code": 200,
  "trace_id": "trc-1002",
  "client_ip": "196.12.221.10",
  "location": {
    "lat": 34.0209,
    "lon": -6.8416
  }
}

POST /app-logs-write/_doc/evt-003
{
  "@timestamp": "2026-06-03T09:02:10Z",
  "service": "auth",
  "env": "training",
  "level": "ERROR",
  "message": "Suspicious login burst blocked",
  "latency_ms": 310,
  "status_code": 403,
  "trace_id": "trc-1003",
  "client_ip": "41.140.44.8",
  "location": {
    "lat": 31.6295,
    "lon": -7.9811
  }
}
```

## 5. CRUD Operations

```http
GET /app-logs/_doc/evt-001

POST /app-logs-write/_doc/evt-temp
{
  "@timestamp": "2026-06-03T09:03:00Z",
  "service": "payments",
  "env": "training",
  "level": "INFO",
  "message": "Temporary payment audit event",
  "latency_ms": 130,
  "status_code": 200,
  "trace_id": "trc-temp",
  "client_ip": "41.92.113.12",
  "location": {
    "lat": 33.5731,
    "lon": -7.5898
  }
}

POST /app-logs/_update/evt-temp
{
  "doc": {
    "level": "WARN",
    "message": "Temporary payment audit event updated"
  }
}

GET /app-logs/_doc/evt-temp

DELETE /app-logs/_doc/evt-temp
```

## 6. Bulk Index More Logs

```http
POST /app-logs-write/_bulk
{ "index": { "_id": "evt-004" } }
{ "@timestamp": "2026-06-03T09:04:00Z", "service": "recommendations", "env": "training", "level": "INFO", "message": "Recommendation cache warmed in 87ms", "latency_ms": 87, "status_code": 200, "trace_id": "trc-1004", "client_ip": "102.50.11.8", "location": { "lat": 35.7595, "lon": -5.8340 } }
{ "index": { "_id": "evt-005" } }
{ "@timestamp": "2026-06-03T09:05:00Z", "service": "payments", "env": "training", "level": "ERROR", "message": "Card authorization failed after retry", "latency_ms": 1620, "status_code": 502, "trace_id": "trc-1005", "client_ip": "41.77.118.2", "location": { "lat": 33.9716, "lon": -6.8498 } }
{ "index": { "_id": "evt-006" } }
{ "@timestamp": "2026-06-03T09:06:00Z", "service": "checkout", "env": "training", "level": "INFO", "message": "Checkout completed in 180ms", "latency_ms": 180, "status_code": 200, "trace_id": "trc-1006", "client_ip": "105.158.22.44", "location": { "lat": 32.2994, "lon": -9.2372 } }
{ "index": { "_id": "evt-007" } }
{ "@timestamp": "2026-06-03T09:07:00Z", "service": "search", "env": "training", "level": "WARN", "message": "Search query took 1180ms for empty result set", "latency_ms": 1180, "status_code": 200, "trace_id": "trc-1007", "client_ip": "41.248.12.88", "location": { "lat": 34.0331, "lon": -5.0003 } }

GET /app-logs/_count
```

## 7. Inspect Mappings and Field Capabilities

```http
GET /app-logs/_mapping

GET /app-logs/_field_caps?fields=service,level,message,latency_ms,status_code,location

GET /app-logs/_search
{
  "size": 1,
  "_source": false,
  "fields": [
    "@timestamp",
    "service",
    "level",
    "latency_ms"
  ]
}
```

## 8. Mapping Conflict Demo

This demonstrates why explicit mappings matter.

```http
DELETE /mapping-conflict-demo?ignore_unavailable=true

POST /mapping-conflict-demo/_doc/1
{
  "service": "checkout",
  "latency_ms": "fast",
  "message": "Checkout completed quickly"
}

GET /mapping-conflict-demo/_mapping

POST /mapping-conflict-demo/_doc/2
{
  "service": "checkout",
  "latency_ms": 2400,
  "message": "Payment gateway timeout after 2400ms"
}
```

Fix the conflict by creating the mapping first.

```http
DELETE /mapping-conflict-demo?ignore_unavailable=true

PUT /mapping-conflict-demo
{
  "mappings": {
    "properties": {
      "service": {
        "type": "keyword"
      },
      "latency_ms": {
        "type": "integer"
      },
      "message": {
        "type": "text"
      }
    }
  }
}

POST /mapping-conflict-demo/_doc/1
{
  "service": "checkout",
  "latency_ms": 2400,
  "message": "Payment gateway timeout after 2400ms"
}

GET /mapping-conflict-demo/_search
```

## 9. Analyzer and Tokenization Examples

```http
GET /_analyze
{
  "analyzer": "standard",
  "text": "Payment gateway timeout after 2400ms"
}

GET /_analyze
{
  "analyzer": "english",
  "text": "The black cats are searching"
}

GET /app-logs-000001/_analyze
{
  "field": "message",
  "text": "Payment gateway timeout after 2400ms"
}
```

## 10. Basic Search Queries

```http
GET /app-logs/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "@timestamp": "asc"
    }
  ]
}

GET /app-logs/_search
{
  "query": {
    "match": {
      "message": "timeout"
    }
  }
}

GET /app-logs/_search
{
  "query": {
    "match_phrase": {
      "message": "gateway timeout"
    }
  }
}

GET /app-logs/_search
{
  "query": {
    "term": {
      "service": "checkout"
    }
  }
}

GET /app-logs/_search
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

## 11. Range, Exists, Wildcard, and Multi Match

```http
GET /app-logs/_search
{
  "query": {
    "range": {
      "latency_ms": {
        "gte": 1000
      }
    }
  }
}

GET /app-logs/_search
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "2026-06-03T09:00:00Z",
        "lte": "2026-06-03T09:10:00Z"
      }
    }
  }
}

GET /app-logs/_search
{
  "query": {
    "exists": {
      "field": "trace_id"
    }
  }
}

GET /app-logs/_search
{
  "query": {
    "wildcard": {
      "service": "check*"
    }
  }
}

GET /app-logs/_search
{
  "query": {
    "multi_match": {
      "query": "cache timeout",
      "fields": [
        "message",
        "service"
      ]
    }
  }
}
```

## 12. Bool Query: Full Text plus Structured Filters

```http
GET /app-logs/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "timeout"
          }
        }
      ],
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
        }
      ],
      "must_not": [
        {
          "term": {
            "service": "search"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "latency_ms": "desc"
    }
  ]
}
```

## 13. Source Filtering, Pagination, and Highlighting

```http
GET /app-logs/_search
{
  "_source": [
    "@timestamp",
    "service",
    "level",
    "message",
    "latency_ms"
  ],
  "query": {
    "match": {
      "message": "timeout"
    }
  },
  "highlight": {
    "fields": {
      "message": {}
    }
  }
}

GET /app-logs/_search
{
  "from": 0,
  "size": 3,
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "@timestamp": "asc"
    }
  ]
}
```

## 14. Aggregations

```http
GET /app-logs/_search
{
  "size": 0,
  "aggs": {
    "events_by_service": {
      "terms": {
        "field": "service",
        "size": 10
      }
    }
  }
}

GET /app-logs/_search
{
  "size": 0,
  "aggs": {
    "by_service": {
      "terms": {
        "field": "service",
        "size": 10
      },
      "aggs": {
        "avg_latency": {
          "avg": {
            "field": "latency_ms"
          }
        },
        "p95_latency": {
          "percentiles": {
            "field": "latency_ms",
            "percents": [
              95
            ]
          }
        }
      }
    }
  }
}

GET /app-logs/_search
{
  "size": 0,
  "aggs": {
    "events_over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "fixed_interval": "1m"
      }
    }
  }
}

GET /app-logs/_search
{
  "size": 0,
  "aggs": {
    "by_level": {
      "filters": {
        "filters": {
          "errors": {
            "term": {
              "level": "ERROR"
            }
          },
          "warnings": {
            "term": {
              "level": "WARN"
            }
          },
          "infos": {
            "term": {
              "level": "INFO"
            }
          }
        }
      }
    }
  }
}
```

## 15. Geospatial Query

```http
GET /app-logs/_search
{
  "query": {
    "geo_distance": {
      "distance": "100km",
      "location": {
        "lat": 33.5731,
        "lon": -7.5898
      }
    }
  },
  "_source": [
    "@timestamp",
    "service",
    "message",
    "client_ip",
    "location"
  ]
}
```

## 16. Nested Documents

Create a small index where each health check must stay attached to its own status.

```http
DELETE /system-events?ignore_unavailable=true

PUT /system-events
{
  "mappings": {
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "service": {
        "type": "keyword"
      },
      "message": {
        "type": "text"
      },
      "checks": {
        "type": "nested",
        "properties": {
          "name": {
            "type": "keyword"
          },
          "status": {
            "type": "keyword"
          },
          "value": {
            "type": "integer"
          }
        }
      }
    }
  }
}

POST /system-events/_doc/sys-001
{
  "@timestamp": "2026-06-03T09:08:00Z",
  "service": "checkout",
  "message": "Service health snapshot",
  "checks": [
    {
      "name": "cpu",
      "status": "ok",
      "value": 37
    },
    {
      "name": "disk",
      "status": "critical",
      "value": 92
    }
  ]
}

GET /system-events/_search
{
  "query": {
    "nested": {
      "path": "checks",
      "query": {
        "bool": {
          "filter": [
            {
              "term": {
                "checks.name": "disk"
              }
            },
            {
              "term": {
                "checks.status": "critical"
              }
            }
          ]
        }
      }
    }
  }
}
```

## 17. Alias Rollover Concept

This is a manual version of what a rollover workflow automates.

```http
PUT /app-logs-000002
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "service": {
        "type": "keyword"
      },
      "env": {
        "type": "keyword"
      },
      "level": {
        "type": "keyword"
      },
      "message": {
        "type": "text"
      },
      "latency_ms": {
        "type": "integer"
      },
      "status_code": {
        "type": "short"
      },
      "trace_id": {
        "type": "keyword"
      },
      "client_ip": {
        "type": "ip"
      },
      "location": {
        "type": "geo_point"
      }
    }
  }
}

POST /_aliases
{
  "actions": [
    {
      "remove": {
        "index": "app-logs-000001",
        "alias": "app-logs-write"
      }
    },
    {
      "add": {
        "index": "app-logs-000002",
        "alias": "app-logs-write",
        "is_write_index": true
      }
    },
    {
      "add": {
        "index": "app-logs-000002",
        "alias": "app-logs"
      }
    }
  ]
}

POST /app-logs-write/_doc/evt-008
{
  "@timestamp": "2026-06-03T09:09:00Z",
  "service": "checkout",
  "env": "training",
  "level": "INFO",
  "message": "Write alias now points to app-logs-000002",
  "latency_ms": 95,
  "status_code": 200,
  "trace_id": "trc-1008",
  "client_ip": "41.92.113.12",
  "location": {
    "lat": 33.5731,
    "lon": -7.5898
  }
}

GET /_cat/aliases/app-logs*?v

GET /app-logs/_search
{
  "sort": [
    {
      "@timestamp": "desc"
    }
  ]
}
```

## 18. Index Template for Logstash-Created Daily Indices

Use this before starting the Docker Compose stack if you want Logstash-created `app-logs-*` indices to receive predictable field types.

```http
PUT /_index_template/app_logs_template
{
  "index_patterns": [
    "app-logs-*"
  ],
  "priority": 100,
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    },
    "mappings": {
      "dynamic": true,
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "service": {
          "type": "keyword"
        },
        "level": {
          "type": "keyword"
        },
        "message": {
          "type": "text",
          "fields": {
            "raw": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "latency_ms": {
          "type": "integer"
        },
        "status_code": {
          "type": "short"
        },
        "trace_id": {
          "type": "keyword"
        },
        "container_service": {
          "type": "keyword"
        }
      }
    }
  }
}

GET /_index_template/app_logs_template
```

## 19. Validate the Live Logstash Pipeline

Run these after `docker compose up -d`.

```http
GET /app-logs-*/_count

GET /app-logs-*/_search
{
  "size": 5,
  "sort": [
    {
      "@timestamp": "desc"
    }
  ]
}

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
          "range": {
            "latency_ms": {
              "gte": 1000
            }
          }
        }
      ]
    }
  },
  "sort": [
    {
      "@timestamp": "desc"
    }
  ]
}

GET /app-logs-*/_search
{
  "query": {
    "exists": {
      "field": "container_service"
    }
  },
  "size": 5
}
```

## 20. Useful Troubleshooting Queries

```http
GET /_cat/indices/app-logs*?v

GET /app-logs-*/_mapping

GET /app-logs-*/_search
{
  "query": {
    "exists": {
      "field": "tags"
    }
  },
  "size": 10
}

GET /app-logs-*/_search
{
  "query": {
    "match": {
      "message": "parse failure"
    }
  }
}
```

