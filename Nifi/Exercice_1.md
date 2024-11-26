Here are step-by-step tutorials for creating three practical and engaging Apache NiFi workflows. Each is designed to help you learn valuable concepts while building something useful:

---

## **Workflow 1: Real-Time Data Movement**

### Objective:
Create a NiFi flow to process log files, filter error messages, and save them to a separate file.

### Key Concepts Learned:
- File ingestion
- FlowFile manipulation
- Output routing

### Steps:
1. **Ingest Files**
   - Use **GetFile**:
     - Configure it to read log files from a directory (e.g., `/data/files`).
     - Set `Keep Source File` to `false` to move files after processing.

2. **Store Files**
   - Add a **PutFile** processor:
     - Configure it to store filtered logs in `/data/moved_files`.

3. **Add LogMessage**
   - Add a **LogMessage** processor:
     - Configure it to log everything.

4. **Test the Workflow**
   - Drop a log file into the source folder and verify that:
     - Errors are filtered and saved.
     - Non-error lines are saved separately.

---

## **Workflow 2: Real-Time Log Processing and Filtering**

### Objective:
Create a NiFi flow to process log files, filter error messages, and save them to a separate file.

### Key Concepts Learned:
- File ingestion
- Content filtering
- FlowFile manipulation
- Output routing

### Steps:
1. **Ingest Log Files**
   - Use **GetFile**:
     - Configure it to read log files from a directory (e.g., `/data/logs`).
     - Set `Keep Source File` to `false` to move files after processing.

2. **Filter Error Messages**
   - Add a **RouteText** processor:
     - Configure it to route FlowFiles containing the keyword `ERROR` to a specific relationship.
     - Use this regex for the `Routing Strategy`:
       ```
       ERROR.*
       ```

3. **Store Filtered Logs**
   - Add a **PutFile** processor:
     - Route the `matches` relationship to this processor.
     - Configure it to store filtered logs in `/data/filtered_logs`.

4. **Log Unfiltered Data**
   - Route the `unmatched` relationship to another **PutFile** processor.
     - Save logs that do not contain `ERROR` to `/data/other_logs`.

5. **Test the Workflow**
   - Drop a log file into the source folder and verify that:
     - Errors are filtered and saved.
     - Non-error lines are saved separately.

---

## **Workflow 3: Fetch Data from an API and Store in a Database**

### Objective:
Pull data from a REST API, convert it to a tabular format, and save it to a database.

### Key Concepts Learned:
- HTTP data ingestion
- JSON processing
- Data transformation
- Database integration

### Steps:
1. **Fetch Data from API**
   - Use **InvokeHTTP**:
     - Configure the processor to call an API (e.g., `https://jsonplaceholder.typicode.com/posts`).
     - Set the HTTP method to `GET`.

2. **Convert JSON to CSV**
   - Use **EvaluateJsonPath**:
     - Extract JSON attributes (e.g., `id`, `title`, `body`) into FlowFile attributes.
   - Use **ReplaceText**:
     - Replace the FlowFile content with the extracted attributes in CSV format.
     - Example template:
       ```
       ${id},${title},${body}
       ```

3. **Write to Database**
   - Use **PutDatabaseRecord**:
     - Configure it to connect to your database (e.g., MySQL or PostgreSQL).
     - Use a **RecordReader** (e.g., JSON or CSV reader) to parse incoming records.

4. **Error Handling**
   - Route the `failure` relationship to a **PutFile** processor to log failed records.

5. **Test the Workflow**
   - Run the workflow and verify that:
     - Data from the API is correctly fetched and stored in the database.
     - Errors are logged if any.

---

## **Workflow 4: Real-Time Twitter Data Sentiment Analysis**

### Objective:
Stream tweets from Twitter, analyze their sentiment, and store results in a NoSQL database (e.g., MongoDB).

### Key Concepts Learned:
- Streaming data sources
- External service integration
- Sentiment analysis with Python
- NoSQL database integration

### Steps:
1. **Fetch Tweets**
   - Use **ConsumeKafka** or **GetHTTP** (if using a third-party service to fetch Twitter data).
     - Configure the Kafka topic or HTTP endpoint to retrieve tweets in JSON format.

2. **Extract Tweet Text**
   - Use **EvaluateJsonPath**:
     - Extract the tweet text (`$.text`) from the JSON data.

3. **Analyze Sentiment**
   - Use **ExecuteScript**:
     - Write a Python or Groovy script to analyze sentiment using a library like TextBlob or NLTK.
     - Pass the sentiment score back as a FlowFile attribute.

4. **Store Results**
   - Use **PutMongo**:
     - Save the tweet data and its sentiment score in MongoDB.
     - Configure the connection to your MongoDB database and specify the collection name.

5. **Error Handling**
   - Route `failure` or invalid tweets to a **PutFile** processor for debugging.

6. **Test the Workflow**
   - Stream a batch of tweets and verify:
     - Sentiment scores are generated.
     - Data is saved correctly in MongoDB.

---

### Additional Resources:
- **Documentation**: Use the [NiFi Processor Documentation](https://nifi.apache.org/docs.html) for details on each processor.
- **Bulletins**: Monitor NiFi bulletins and provenance data to debug and understand the flow.
