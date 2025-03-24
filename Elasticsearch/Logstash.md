This is a step-by-step tutorial to set up and use Logstash based on docker to move data from a file to Elasticsearch using Filebeat. This guide assumes you have Docker and Docker Compose installed and that an Elasticsearch instance is already running.

---

# Moving Data from a File to Elasticsearch: A Beginner's Tutorial

This tutorial will walk you through setting up a simple data pipeline using Filebeat, Logstash, and Elasticsearch. Filebeat will read data from a log file, send it to Logstash for processing, and Logstash will forward it to Elasticsearch for storage and indexing. By the end, you’ll see your data in Elasticsearch!

## Prerequisites
- **Docker** and **Docker Compose** installed on your system.
- An **Elasticsearch** instance running on your machine, accessible at `http://localhost:9200`.
- Basic familiarity with terminal commands.

## Step 1: Set Up Your Project Directory
1. Create a new directory for your project:
   ```bash
   mkdir logstash-filebeat-tutorial
   cd logstash-filebeat-tutorial
   ```
2. Inside this directory, you’ll create the necessary configuration files and the Docker Compose file.

## Step 2: Create the Docker Compose File
1. Create a file named `docker-compose.yml` in your project directory.
2. Copy and paste the following content into `docker-compose.yml`:
   ```yaml
   version: '3.8'

   services:
     logstash:
       image: docker.elastic.co/logstash/logstash:8.12.0
       container_name: logstash
       volumes:
         - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
       environment:
         - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
         - XPACK_MONITORING_ENABLED=false
       ports:
         - "5044:5044"
       networks:
         - elastic-network

     filebeat:
       image: docker.elastic.co/beats/filebeat:8.12.0
       container_name: filebeat
       volumes:
         - ./filebeat.yml:/usr/share/filebeat/filebeat.yml
         - ./sample.log:/usr/share/filebeat/sample.log
       depends_on:
         - logstash
       networks:
         - elastic-network

   volumes:
     logstash-data:
       driver: local

   networks:
     elastic-network:
       external: true
       name: elasticsearchcourse_elastic-network
   ```
3. Save the file. This defines two services: `logstash` (to process data) and `filebeat` (to read the log file), connecting them to an external Elasticsearch network.

## Step 3: Configure Logstash
1. Create a file named `logstash.conf` in the same directory.
2. Add the following configuration to `logstash.conf`:
   ```conf
   input {
     beats {
       port => 5044
     }
   }

   filter {
     # Optional: Add filters here if you want to process the data
   }

   output {
     elasticsearch {
       hosts => ["${ELASTICSEARCH_HOSTS}"]
       index => "sample-logs-%{+YYYY.MM.dd}"
     }
   }
   ```
3. Save the file. This tells Logstash to:
   - Accept input from Filebeat on port 5044.
   - Send the data to Elasticsearch, storing it in an index named `sample-logs` with a daily suffix (e.g., `sample-logs-2025.03.24`).

## Step 4: Configure Filebeat
1. Create a file named `filebeat.yml` in the same directory.
2. Add the following configuration to `filebeat.yml`:
   ```yaml
   filebeat.inputs:
   - type: log
     enabled: true
     paths:
       - /usr/share/filebeat/sample.log

   output.logstash:
     hosts: ["logstash:5044"]
   ```
3. Save the file. This tells Filebeat to:
   - Read logs from `sample.log`.
   - Send them to Logstash on port 5044.

## Step 5: Create a Sample Log File
1. Create a file named `sample.log` in the same directory.
2. Add a few sample log lines, like this:
   ```
   2025-03-24 10:00:00 INFO Starting application
   2025-03-24 10:00:01 ERROR Something went wrong
   2025-03-24 10:00:02 DEBUG Debugging info
   ```
3. Save the file. This is the data Filebeat will read and send to Elasticsearch via Logstash.

## Step 6: Set Up the Network
The Docker Compose file uses an external network named `elasticsearchcourse_elastic-network`. You need to create this network if it doesn’t already exist:
1. Run this command in your terminal:
   ```bash
   docker network create elasticsearchcourse_elastic-network
   ```
2. Ensure your Elasticsearch instance is connected to this network. If it’s running in Docker, you can connect it with:
   ```bash
   docker network connect elasticsearchcourse_elastic-network elasticsearch
   ```
   (Replace `elasticsearch` with your Elasticsearch container name.)

## Step 7: Start the Services
1. In your project directory, run:
   ```bash
   docker-compose up -d
   ```
2. This starts Filebeat and Logstash in the background. You should see the containers starting with:
   ```bash
   docker ps
   ```

## Step 8: Verify Data in Elasticsearch
1. Wait a few seconds for the pipeline to process the data.
2. Check Elasticsearch to see if the data arrived. Use a tool like `curl` or a browser:
   ```bash
   curl -X GET "http://localhost:9200/sample-logs-2025.03.24/_search?pretty"
   ```
   Or visit `http://localhost:9200/sample-logs-2025.03.24/_search?pretty` in your browser (if Elasticsearch is unsecured).
3. You should see your log lines in the `_source` field of the response, like:
   ```json
   {
     "message": "2025-03-24 10:00:00 INFO Starting application",
     ...
   }
   ```

## Step 9: Add More Data
1. Open `sample.log` and append more lines, such as:
   ```
   2025-03-24 10:00:03 INFO New event occurred
   ```
2. Save the file. Filebeat will automatically detect the changes and send the new data to Elasticsearch via Logstash.
3. Re-run the search command to confirm the new data appears.

## Step 10: Shut Down
When you’re done, stop and remove the containers:
```bash
docker-compose down
```

## Troubleshooting
- **No data in Elasticsearch?**
  - Ensure Elasticsearch is running and accessible at `http://elasticsearch:9200` from the containers.
  - Check container logs with `docker logs logstash` or `docker logs filebeat`.
- **Network issues?**
  - Verify the `elasticsearchcourse_elastic-network` exists and all services (including Elasticsearch) are connected.

## Next Steps
- Explore Logstash filters to parse and transform your logs (e.g., splitting timestamps).
- Use Kibana to visualize your data in Elasticsearch.

Congratulations! You’ve set up a basic pipeline to move data from a file to Elasticsearch. Happy logging!
