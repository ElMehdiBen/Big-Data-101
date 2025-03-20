Let’s create a simple `docker-compose.yml` file to set up Elasticsearch, Logstash, and Kibana (the core components of the Elastic Stack, often referred to as the ELK Stack). This setup will allow you to run all three services in a single Docker Compose configuration, with minimal configuration for a beginner-friendly experience. I’ll also include explanations for each part and provide steps to get it running.

---

### Simple Docker Compose for Elasticsearch, Logstash, and Kibana

#### `docker-compose.yml`
Below is a minimal `docker-compose.yml` file that sets up Elasticsearch, Logstash, and Kibana with basic networking and volume configurations.

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es-data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl --silent --fail http://localhost:9200/_cluster/health || exit 1"]
      interval: 10s
      timeout: 10s
      retries: 3
    networks:
      - elastic-network

  logstash:
    image: docker.elastic.co/logstash/logstash:8.12.0
    container_name: logstash
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      elasticsearch:
        condition: service_healthy
    command: >
      bash -c "sleep 30 && /usr/share/logstash/bin/logstash -f /usr/share/logstash/pipeline/logstash.conf"
    networks:
      - elastic-network

  kibana:
    image: docker.elastic.co/kibana/kibana:8.12.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - elastic-network

volumes:
  es-data:
    driver: local

networks:
  elastic-network:
    driver: bridge
```

---

#### Explanation of the Configuration

1. **Version**:
   - `version: '3.8'`: Specifies the Docker Compose file format. Version 3.8 is compatible with most recent Docker installations.

2. **Services**:
   - **Elasticsearch**:
     - `image`: Uses the official Elasticsearch image (version 8.12.0, the latest stable as of early 2025).
     - `environment`:
       - `discovery.type=single-node`: Runs Elasticsearch in single-node mode (no clustering).
       - `xpack.security.enabled=false`: Disables security features (e.g., authentication) for simplicity. In production, you should enable this.
       - `ES_JAVA_OPTS`: Limits memory usage to 512 MB for both minimum and maximum heap size (suitable for small setups).
     - `ports`: Maps port 9200 on the host to 9200 in the container (Elasticsearch’s default port).
     - `volumes`: Persists Elasticsearch data in a named volume `es-data`.

   - **Logstash**:
     - `image`: Uses the official Logstash image (same version as Elasticsearch for compatibility).
     - `volumes`: Mounts a `logstash.conf` file (you’ll create this next) to define a simple pipeline.
     - `depends_on`: Ensures Elasticsearch starts before Logstash.

   - **Kibana**:
     - `image`: Uses the official Kibana image (same version).
     - `environment`: Configures Kibana to connect to Elasticsearch at `http://elasticsearch:9200`.
     - `ports`: Maps port 5601 (Kibana’s default) to the host.
     - `depends_on`: Ensures Elasticsearch starts before Kibana.

3. **Volumes**:
   - `es-data`: A named volume to persist Elasticsearch data, so it’s not lost when the container stops.

4. **Networks**:
   - `elastic-network`: A bridge network to allow the services to communicate with each other using their service names (e.g., `elasticsearch`).

---

#### Logstash Configuration (`logstash.conf`)
Logstash needs a pipeline configuration to process data. For this simple setup, let’s create a basic pipeline that reads from a file (or standard input) and sends data to Elasticsearch.

Create a file named `logstash.conf` in the same directory as your `docker-compose.yml`:

```conf
input {
  stdin { }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "logstash-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}
```

- **Explanation**:
  - `input { stdin { } }`: Reads input from the terminal (you can type messages to test).
  - `output { elasticsearch { ... } }`: Sends data to Elasticsearch, creating an index named `logstash-` followed by the date (e.g., `logstash-2025.03.20`).
  - `output { stdout { ... } }`: Prints the processed data to the console for debugging.

---

#### Steps to Run the Setup

1. **Save the Files**:
   - Save the `docker-compose.yml` file in a directory (e.g., `elastic-stack`).
   - Save the `logstash.conf` file in the same directory.

2. **Start the Services**:
   - Open a terminal in the directory containing `docker-compose.yml`.
   - Run:
     ```bash
     docker-compose up -d
     ```
   - The `-d` flag runs the containers in the background.

3. **Verify the Services**:
   - **Elasticsearch**: Check if it’s running by accessing `http://localhost:9200` in a browser or with `curl`:
     ```bash
     curl http://localhost:9200
     ```
     You should see a JSON response like:
     ```json
     {
       "name": "d5a5b5e5f5e5",
       "cluster_name": "docker-cluster",
       "version": { "number": "8.12.0", ... },
       ...
     }
     ```
   - **Kibana**: Open `http://localhost:5601` in a browser. You should see the Kibana UI.
   - **Logstash**: Check the logs to ensure it started:
     ```bash
     docker logs logstash
     ```

4. **Test Logstash**:
   - Attach to the Logstash container to send some test data:
     ```bash
     docker exec -it logstash bash
     ```
   - Inside the container, run:
     ```bash
     /usr/share/logstash/bin/logstash -f /usr/share/logstash/pipeline/logstash.conf
     ```
   - Type a message (e.g., `Hello, Elasticsearch!`) and press Enter. Logstash will process it and send it to Elasticsearch.

5. **Verify Data in Elasticsearch**:
   - Check if the data was indexed:
     ```bash
     curl -X GET "http://localhost:9200/logstash-*/_search?pretty"
     ```
   - You should see your message in the results.

6. **Explore in Kibana**:
   - In Kibana (`http://localhost:5601`), go to **Discover**.
   - Create an index pattern for `logstash-*` to view the data Logstash sent.

---

#### Stopping the Services
To stop the services, run:
```bash
docker-compose down
```
To also remove the persisted data (e.g., Elasticsearch indices), add the `-v` flag:
```bash
docker-compose down -v
```

---

#### Tips for Beginners
- **Version Matching**: Ensure all components (Elasticsearch, Logstash, Kibana) use the same version (e.g., 8.12.0) to avoid compatibility issues.
- **Memory Usage**: If your system has limited resources, adjust `ES_JAVA_OPTS` in the Elasticsearch service to lower values (e.g., `-Xms256m -Xmx256m`).
- **Logstash Pipelines**: This example uses a simple `stdin` input. In a real setup, you might configure Logstash to read from files, Kafka, or other sources.
- **Security**: This setup disables security for simplicity. In production, enable `xpack.security` and set up usernames/passwords (e.g., for the `elastic` user).

---

#### Troubleshooting
- **Elasticsearch Not Starting**: Check the logs (`docker logs elasticsearch`). Common issues include insufficient memory or port conflicts (ensure 9200 is free).
- **Kibana Can’t Connect**: Ensure Elasticsearch is running and the `ELASTICSEARCH_HOSTS` URL is correct.
- **Logstash Errors**: Verify the `logstash.conf` file syntax and ensure Elasticsearch is accessible from the Logstash container.

---

This setup provides a simple, functional ELK Stack for learning and experimentation. You can now index data via Logstash, query it in Elasticsearch, and visualize it in Kibana. Let me know if you’d like to expand this setup (e.g., add Beats, enable security, or configure a more complex Logstash pipeline)!
