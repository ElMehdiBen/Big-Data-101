Let’s dive into a practical set of elements for an intermediate Elasticsearch (ES) user, focusing on **aggregations**, **aliases**, and other useful features that can enhance your ability to search, analyze, and manage data effectively. I’ll provide examples, explanations, and practical use cases to help you apply these concepts in real-world scenarios. Since you’re already working with Elasticsearch, Logstash, and Kibana in a Docker setup, I’ll tailor the examples to fit that context and assume you’re comfortable with basic indexing and querying.

---

### 1. Aggregations: Analyzing and Summarizing Data

Aggregations in Elasticsearch allow you to analyze and summarize your data, such as calculating metrics (e.g., averages, sums), grouping data into buckets (e.g., by category or time), or building complex analytics pipelines. They’re particularly useful for dashboards, reports, and data exploration in Kibana.

#### Practical Example: Analyze Log Data
Let’s assume your `logstash-*` indices (from your Logstash setup) contain log data with fields like `message`, `timestamp`, `@timestamp`, and a custom field `log_level` (e.g., `INFO`, `WARN`, `ERROR`).

**Goal**: Analyze the distribution of log levels over time and calculate the average message length per log level.

**Aggregation Query**:
```json
GET logstash-*/_search
{
  "query": {
    "bool": {
      "filter": [
        { "range": { "@timestamp": { "gte": "now-7d/d", "lte": "now-7d/d" } } }
      ]
    }
  },
  "aggs": {
    "by_date": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "day"
      },
      "aggs": {
        "by_log_level": {
          "terms": {
            "field": "log_level.keyword"
          },
          "aggs": {
            "avg_message_length": {
              "avg": {
                "field": "message_length"  // Assuming you have a field for message length
              }
            }
          }
        }
      }
    }
  },
  "size": 0
}
```

- **Explanation**:
  - **Query**: Filters logs from the last 7 days (`now-7d/d`).
  - **Aggregations**:
    - `date_histogram`: Groups logs by day based on the `@timestamp` field.
    - `terms`: Within each day, groups logs by `log_level` (e.g., `INFO`, `WARN`, `ERROR`).
    - `avg`: Calculates the average message length for each log level.
  - `size: 0`: Excludes individual search hits, returning only the aggregation results.

**Sample Response**:
```json
{
  "aggregations": {
    "by_date": {
      "buckets": [
        {
          "key_as_string": "2025-03-18T00:00:00.000Z",
          "key": 1742256000000,
          "doc_count": 1000,
          "by_log_level": {
            "buckets": [
              {
                "key": "INFO",
                "doc_count": 600,
                "avg_message_length": { "value": 45.3 }
              },
              {
                "key": "ERROR",
                "doc_count": 200,
                "avg_message_length": { "value": 78.9 }
              },
              {
                "key": "WARN",
                "doc_count": 200,
                "avg_message_length": { "value": 62.1 }
              }
            ]
          }
        },
        ...
      ]
    }
  }
}
```

**Use Case**:
- Visualize this in Kibana by creating a **Time Series Visual Builder (TSVB)** or **Lens** chart to show the distribution of log levels over time and their average message lengths.

#### Practical Tip: Pipeline Aggregations
Pipeline aggregations allow you to perform calculations on the results of other aggregations. For example, let’s calculate the maximum average message length across all log levels per day.

**Pipeline Aggregation Query**:
```json
GET logstash-*/_search
{
  "query": {
    "bool": {
      "filter": [
        { "range": { "@timestamp": { "gte": "now-7d/d", "lte": "now-7d/d" } } }
      ]
    }
  },
  "aggs": {
    "by_date": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "day"
      },
      "aggs": {
        "by_log_level": {
          "terms": {
            "field": "log_level.keyword"
          },
          "aggs": {
            "avg_message_length": {
              "avg": {
                "field": "message_length"
              }
            }
          }
        },
        "max_avg_message_length": {
          "max_bucket": {
            "buckets_path": "by_log_level>avg_message_length"
          }
        }
      }
    }
  },
  "size": 0
}
```

- **Explanation**:
  - `max_bucket`: A pipeline aggregation that finds the maximum value of `avg_message_length` across all `by_log_level` buckets for each day.

**Use Case**:
- Use this to identify days with unusually verbose logs (e.g., high average message length for `ERROR` logs).

---

### 2. Index Aliases: Managing Indices Flexibly

Index aliases in Elasticsearch allow you to create a virtual name for one or more indices, making it easier to manage and query data without worrying about the underlying index names. Aliases are particularly useful for rolling indices (like `logstash-YYYY.MM.dd`), reindexing, and zero-downtime index updates.

#### Practical Example: Create and Use an Alias
**Goal**: Create an alias `logs` that points to all `logstash-*` indices, so you can query them as a single entity.

**Step 1: Create the Alias**:
```json
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "logstash-*",
        "alias": "logs"
      }
    }
  ]
}
```

- **Explanation**:
  - `index: "logstash-*"`: Matches all indices starting with `logstash-` (e.g., `logstash-2025.03.20`).
  - `alias: "logs"`: Creates an alias named `logs` that points to these indices.

**Step 2: Query Using the Alias**:
Now you can query the `logs` alias instead of specifying individual indices:
```json
GET logs/_search
{
  "query": {
    "match": {
      "log_level": "ERROR"
    }
  }
}
```

**Use Case**:
- Simplifies querying in Kibana: Instead of creating an index pattern for `logstash-*`, you can create one for `logs`.
- Makes it easier to manage rolling indices: If you delete old indices or add new ones, the alias automatically updates to include the matching indices.

#### Practical Example: Zero-Downtime Reindexing with Aliases
**Goal**: Reindex data from `logstash-2025.03.20` into a new index with updated mappings, without downtime.

**Step 1: Create a New Index with Updated Mappings**:
```json
PUT logstash-2025.03.20-reindexed
{
  "mappings": {
    "properties": {
      "message": { "type": "text" },
      "log_level": { "type": "keyword" },
      "message_length": { "type": "integer" },
      "@timestamp": { "type": "date" },
      "new_field": { "type": "keyword" }  // New field added
    }
  }
}
```

**Step 2: Reindex Data**:
```json
POST _reindex
{
  "source": {
    "index": "logstash-2025.03.20"
  },
  "dest": {
    "index": "logstash-2025.03.20-reindexed"
  }
}
```

**Step 3: Update the Alias**:
Swap the alias to point to the new index:
```json
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "logstash-2025.03.20",
        "alias": "logs"
      }
    },
    {
      "add": {
        "index": "logstash-2025.03.20-reindexed",
        "alias": "logs"
      }
    }
  ]
}
```

- **Explanation**:
  - The `logs` alias now points to the reindexed data, and queries continue to work seamlessly.
  - You can delete the old index (`logstash-2025.03.20`) after verifying the new index is correct.

**Use Case**:
- Update mappings or settings without interrupting applications that query the `logs` alias.

---

### 3. Other Practical Elements for Intermediate Users

Here are additional intermediate-level features and techniques to enhance your Elasticsearch usage.

#### 3.1. Index Templates: Automate Index Creation
Index templates allow you to define settings and mappings that are automatically applied to new indices matching a pattern. This is useful for your `logstash-*` indices.

**Example: Create an Index Template**:
```json
PUT _index_template/logstash_template
{
  "index_patterns": ["logstash-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "message": { "type": "text" },
        "log_level": { "type": "keyword" },
        "message_length": { "type": "integer" },
        "@timestamp": { "type": "date" }
      }
    }
  }
}
```

- **Explanation**:
  - `index_patterns`: Applies this template to any new index matching `logstash-*`.
  - `settings`: Configures the number of shards and replicas.
  - `mappings`: Defines the field types for new indices.

**Use Case**:
- Ensures consistent settings and mappings for all `logstash-*` indices created by Logstash.

#### 3.2. Ingest Pipelines: Preprocess Data
Ingest pipelines allow you to preprocess documents before indexing them, such as adding fields, parsing data, or transforming values.

**Example: Add a Field with the Ingest Pipeline**:
```json
PUT _ingest/pipeline/add_message_length
{
  "description": "Add message length field",
  "processors": [
    {
      "script": {
        "source": "ctx.message_length = ctx.message != null ? ctx.message.length() : 0"
      }
    }
  ]
}
```

**Apply the Pipeline During Indexing**:
- Update your Logstash `output` configuration to use the pipeline:
  ```conf
  output {
    elasticsearch {
      hosts => ["http://elasticsearch:9200"]
      index => "logstash-%{+YYYY.MM.dd}"
      data_stream => "false"
      pipeline => "add_message_length"
    }
    stdout { codec => rubydebug }
  }
  ```

- **Explanation**:
  - The `script` processor calculates the length of the `message` field and stores it in `message_length`.
  - The pipeline is applied automatically when Logstash indexes documents.

**Use Case**:
- Enrich documents with derived fields (e.g., message length, parsed timestamps) without modifying your Logstash configuration.

#### 3.3. Search Templates: Reusable Queries
Search templates allow you to define reusable query templates with parameters, making it easier to run complex searches repeatedly.

**Example: Create a Search Template**:
```json
POST _scripts/log_level_search
{
  "script": {
    "lang": "mustache",
    "source": {
      "query": {
        "bool": {
          "filter": [
            { "term": { "log_level.keyword": "{{log_level}}" } },
            { "range": { "@timestamp": { "gte": "{{start_date}}", "lte": "{{end_date}}" } } }
          ]
        }
      }
    }
  }
}
```

**Use the Search Template**:
```json
GET logs/_search/template
{
  "id": "log_level_search",
  "params": {
    "log_level": "ERROR",
    "start_date": "now-7d/d",
    "end_date": "now-7d/d"
  }
}
```

**Use Case**:
- Reuse common queries in scripts or applications, reducing the need to hardcode complex queries.

#### 3.4. Snapshot and Restore: Backup and Recovery
Snapshots allow you to back up your indices to a repository (e.g., a shared filesystem) and restore them if needed.

**Example: Set Up a Snapshot Repository**:
1. Configure a shared filesystem repository:
   ```json
   PUT _snapshot/my_backup
   {
     "type": "fs",
     "settings": {
       "location": "/mnt/backup"
     }
   }
   ```
   - Note: You’ll need to mount a shared filesystem into your Elasticsearch container at `/mnt/backup` and ensure the Elasticsearch user has write permissions.

2. Take a Snapshot:
   ```json
   PUT _snapshot/my_backup/snapshot_2025_03_20
   {
     "indices": "logstash-*",
     "ignore_unavailable": true,
     "include_global_state": false
   }
   ```

3. Restore a Snapshot:
   ```json
   POST _snapshot/my_backup/snapshot_2025_03_20/_restore
   {
     "indices": "logstash-2025.03.20"
   }
   ```

**Use Case**:
- Back up your log data before performing risky operations (e.g., reindexing, deleting old indices).

---

### Practical Workflow: Putting It All Together

Here’s a practical workflow using the elements above:

1. **Set Up Index Template**:
   - Create a template for `logstash-*` indices to ensure consistent mappings and settings.

2. **Create an Ingest Pipeline**:
   - Add a pipeline to calculate `message_length` for each log entry.

3. **Use Filebeat and Logstash**:
   - Filebeat monitors `sample.log` and sends data to Logstash.
   - Logstash applies the ingest pipeline and indexes data into `logstash-YYYY.MM.dd`.

4. **Create an Alias**:
   - Create a `logs` alias for all `logstash-*` indices.

5. **Run Aggregations**:
   - Use Kibana to create visualizations based on aggregations (e.g., log level distribution over time).

6. **Backup Data**:
   - Set up a snapshot repository and take regular backups of your indices.

---

### Tips for Intermediate Users

- **Optimize Aggregations**:
  - Use `execution_hint: map` in `terms` aggregations for better performance on high-cardinality fields:
    ```json
    "terms": {
      "field": "log_level.keyword",
      "execution_hint": "map"
    }
    ```

- **Monitor Performance**:
  - Use the `_cat/indices` API to check index sizes and health:
    ```bash
    GET _cat/indices?v
    ```

- **Kibana Integration**:
  - Use Kibana’s **Discover** tab to explore data, and create **Visualize** dashboards with your aggregations.

- **Security**:
  - In a production setup, enable `xpack.security` in Elasticsearch and configure users/roles for Logstash and Kibana.

---

This set of practical elements should give you a solid foundation for intermediate Elasticsearch usage. Let me know if you’d like to dive deeper into any of these topics or explore additional features!