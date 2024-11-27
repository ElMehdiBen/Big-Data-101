Step-by-step tutorials for creating three practical and engaging Apache NiFi workflows. Each is designed to help you learn valuable concepts while building something useful:

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

## **Workflow 2: Real-Time Data Movement + Matching **

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
    
2. **Match File Names**
   - Add a **RouteOnAttribute** processor:
     - Configure it to filter by matching the name.

3. **Store Files**
   - Add a **PutFile** processor:
     - Configure it to store filtered logs in `/data/moved_files`.

4. **Add LogMessage**
   - Add a **LogMessage** processor:
     - Configure it to log everything.

5. **Test the Workflow**
   - Drop a log file into the source folder and verify that:
     - Errors are filtered and saved.
     - Non-error lines are saved separately.
    
---

## **Workflow 3: Real-Time Log Processing and Filtering**

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

### Additional Resources:
- **Documentation**: Use the [NiFi Processor Documentation](https://nifi.apache.org/docs.html) for details on each processor.
- **Bulletins**: Monitor NiFi bulletins and provenance data to debug and understand the flow.
