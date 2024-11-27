Apache NiFi Main Features and Use Cases
=======================================


Introduction
============

The main purpose of Apache NiFi is to automate data flow from a source to a destination. This data movement can consist of multiple steps of data processing. A step can consist of data ingestion, extraction, transformation, enrichment and routing. In a nutshell NiFi can be used to implement complex workflow of data transfer between two systems. All of this can be achieved with the help of built in processors and browser based visual programming interface. A processor is highly configurable component to read data from variety of sources, or process it, or write it to many different type of destinations.

Some of the high level data flow challenges NiFi tries to address are: system failures, big data, small data, very fast moving data, very slow moving data, data coming from many protocols and data coming in variety of formats.

Processor Types
===============

*   **Ingestion**: To read/write data from/to different data sources
    - _Protocols_: HTTP(S), AMQP, MQTT, UDP, TCP, CEF,JMS, (S)FTP, etc.
    - _Brokers_: Kafka, JMS, AMQP, MQTT etc.
    - _Databases_: JDBC, MongoDB, HBase, Cassandra, Elasticsearch etc.
    - Storage: File, S3, Azure Blob, GridFS, Google Drive, HDFS, Splunk etc.
*   **Extraction:** XML, JSON, Regex, Grok etc.
*   **Transformation :
    -** _Format conversion: J_SON to Avro, CSV to ORC, JSON to SQL, etc.
    - _Compression/decompression_, Merge, Split, encryption etc.
*   **Data enrichment:** Attribute, content, rules etc.
*   **Routing :** Priority, dynamic, static, content, metadata based routing
*   **Integrations:** Springboot, Spark

Main Features
=============

*   Queueing and back pressure support between processors.
*   Data traceability/audit support with full data history.
*   Restart from a failed processor.
*   Monitoring of data pipeline performance.
*   Monitoring of system resources (CPU/Memory/Disk)
*   Large open source community contributors.
*   Largest production deployments as compared to its competitors.
*   Good documentation and community support.
*   Around 500+ processors.
*   Writing custom processor is easy.
*   Horizontal scalability and cluster.
*   Batch and stream data processing.
*   Expression Language to reference, compare and manipulate metadata for routing and other purpose.
*   Ability to execute python, groovy and javascript code.
*   Ability to execute operating system command and capture output.
*   Scaled down version called MiNiFi for IOT devices.
*   Schema less data format so can support any kind of data including media files.

Use Cases
=========

*   Build complex, highly distributed, multi step, multi node, high performance data workflow/pipeline.
*   Data transfer from a source to a destination.
*   Multi step data transformation and enrichment.
*   Protocol transformation.
*   Application/System integration.
*   IOT device data ingestion.
*   Real time/batch data analytics/machine learning.
*   Visual programming.


Installation
============

```
docker run --name nifi -p 8443:8443 -v ./data:/data -d apache/nifi:latest

#run this to get credentials
docker logs nifi | grep Generated
```
