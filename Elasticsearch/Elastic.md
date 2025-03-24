Here’s a step-by-step Markdown tutorial for beginners to set up Elasticsearch and Kibana using the provided Docker Compose configuration. This guide will help you get both services running and verify that they’re working together.

---

# Setting Up Elasticsearch and Kibana: A Beginner's Tutorial

This tutorial will guide you through setting up Elasticsearch and Kibana using Docker Compose. Elasticsearch is a powerful search and analytics engine, and Kibana is a visualization tool that works with it. By the end, you’ll have both running and be able to access Kibana to explore your Elasticsearch instance!

## Prerequisites
- **Docker** and **Docker Compose** installed on your system.
- Basic familiarity with terminal commands.

## Step 1: Set Up Your Project Directory
1. Create a new directory for your project:
   ```bash
   mkdir elasticsearch-kibana-tutorial
   cd elasticsearch-kibana-tutorial
   ```
2. Inside this directory, you’ll create the Docker Compose file.

## Step 2: Create the Docker Compose File
1. Create a file named `docker-compose.yml` in your project directory.
2. Copy and paste the following content into `docker-compose.yml`:
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
3. Save the file. This defines two services:
   - `elasticsearch`: A single-node Elasticsearch instance.
   - `kibana`: A Kibana instance connected to Elasticsearch.

## Step 3: Start the Services
1. In your project directory, run:
   ```bash
   docker-compose up -d
   ```
2. This starts Elasticsearch and Kibana in the background. Docker Compose will:
   - Create a bridge network named `elastic-network`.
   - Start Elasticsearch and ensure it’s healthy before starting Kibana.
3. Check that the containers are running:
   ```bash
   docker ps
   ```
   You should see `elasticsearch` and `kibana` listed.

## Step 4: Verify Elasticsearch is Running
1. Wait a few seconds for Elasticsearch to fully start.
2. Test it by running:
   ```bash
   curl -X GET "http://localhost:9200/?pretty"
   ```
   Or open `http://localhost:9200` in your browser.
3. You should see a JSON response like this:
   ```json
   {
     "name": "elasticsearch",
     "cluster_name": "docker-cluster",
     "version": {
       "number": "8.12.0",
       ...
     },
     ...
   }
   ```
   This confirms Elasticsearch is up and running.

## Step 5: Access Kibana
1. Open your web browser and go to:
   ```
   http://localhost:5601
   ```
2. Kibana should load its welcome page. Since `xpack.security.enabled` is set to `false`, no login is required.
3. If the page doesn’t load immediately, wait a minute—Kibana takes a little time to connect to Elasticsearch.

## Step 6: Explore Kibana
1. On the Kibana welcome page, click **Explore on my own**.
2. In the left sidebar, go to **Management** > **Dev Tools**.
3. In the Dev Tools console, run this command to create a sample index:
   ```json
   PUT my-first-index
   ```
   Click the green "Run" triangle. You should see a response like:
   ```json
   {
     "acknowledged": true,
     "shards_acknowledged": true,
     "index": "my-first-index"
   }
   ```
4. Add some sample data:
   ```json
   POST my-first-index/_doc
   {
     "message": "Hello from Kibana!",
     "date": "2025-03-24"
   }
   ```
   Run it, and you’ll get a response confirming the document was created.

## Step 7: Search Your Data
1. In the Dev Tools console, search for your data:
   ```json
   GET my-first-index/_search
   ```
2. Run it, and you’ll see your document in the response:
   ```json
   {
     "hits": {
       "total": {
         "value": 1,
         ...
       },
       "hits": [
         {
           "_source": {
             "message": "Hello from Kibana!",
             "date": "2025-03-24"
           },
           ...
         }
       ]
     }
   }
   ```

## Step 8: Shut Down
When you’re done, stop and remove the containers:
```bash
docker-compose down
```
To also remove the stored Elasticsearch data, use:
```bash
docker-compose down -v
```

## Troubleshooting
- **Elasticsearch not starting?**
  - Check logs with `docker logs elasticsearch`. Look for errors like insufficient memory (adjust `ES_JAVA_OPTS` if needed).
- **Kibana not connecting?**
  - Ensure Elasticsearch is healthy (`docker ps` should show it as `healthy`).
  - Verify the network with `docker network inspect elastic-network`.
- **Port conflicts?**
  - If ports 9200 or 5601 are in use, stop the conflicting process or change the ports in `docker-compose.yml`.

## Next Steps
- Enable security (`xpack.security.enabled=true`) and set up users/passwords for production use.
- In Kibana, try **Discover** to visualize your data or create dashboards.
- Combine this setup with the Logstash/Filebeat tutorial to send logs to Elasticsearch!

Congratulations! You now have Elasticsearch and Kibana running. Enjoy exploring your data!

---

This tutorial is beginner-friendly and ensures you can get started quickly. Let me know if you need clarification or additional steps!