Apache NiFi in a Nutshell
=========================

Overview
========

Apache NiFi is an open-source, easy to use, and reliable system to process and distribute data. The data can be propagated from almost any source to any destination. NiFi operates on the principle of _Configuration over Coding_. That means it is possible to create simple ETL to complex data lack without even writing a single line of code. NiFi can operate on batch as well as stream of data. NiFi seamlessly ingests data from multiple data sources and provides mechanisms to handle different schema in the data.

NiFi can be a data logistics platform which enables easy collection, curation, analysis and action on any data anywhere (edge, cloud, data center) with built-in end-to-end security and provenance. This unique set of features makes NiFi the best choice for implementing new data centric use cases that require geographically distributed architectures and high levels of SLA.

Flow-Based Programming (FBP) paradigm of NiFi tries to have a natural way of abstracting logic and visualizing each of its elements. The business logic in the application is abstracted like a “black box” process and the processes in the network communicate to each other through message passing.

NiFi consists of atomic elements that can be combined into groups to build simple or complex data flow. It provides a web-based User Interface for creating, monitoring, & controlling data flows. NiFi was donated by the NSA to the Apache Foundation in 2014 and current development and support are provided mostly by Hortonworks.

**Common terminologies in NiFi**
================================

Before digging deeper into what is NiFi and how it works, let’s get to know some common terminologies used in NiFi.

**FlowFile** represents the atomic object moving through the system and for each one, NiFi keeps track of its attribute and associated content.

**Processor**s are similar to the black box of FBP. Processors have access to attributes of a given FlowFile and its content stream. Processors can operate on zero or more FlowFiles in a given unit of work and either commit that work or rollback.

**Connection** provides the actual linkage between processors. Connections act as queues and allow various processes to interact at differing rates. These queues can be prioritized dynamically and can have upper bounds on load, which enable _back pressure_.

**Flow Controller** acts as the broker facilitating the exchange of FlowFiles between processors. It allocates and manages threads for processors. It’s what executes the data flow.

**Process Group** is a combination of a set of processes and their connections. When you have a complex dataflow, it’s better to combine processors into logical process groups. These process groups receive data via _input ports_ and send data out via _output ports_.

**Controller Service** are shared services that can be used by reporting tasks, processors, and other services that can be used for configuration or task execution. It provides the ability to configure keystore and/or truststore properties once and reuse that configuration throughout the application. The idea is that, rather than configure this information in every processor that might need it, the controller service provides it for any processor to use as needed.

**Back Pressure:** NiFi supports buffering of all queued data as well as the ability to provide back pressure as those queues reach specified limits. NiFi provides two configuration elements for Back Pressure, _Back pressure object threshold_ and _Back pressure data size threshold._ The first configuration option provided is the number of FlowFiles that can be in the queue before back pressure is applied and later specifies the maximum amount of data (in size) that should be queued up before applying back pressure.

This concept of back pressure allows the system to avoid being overrun with data.

![captionless image](https://miro.medium.com/v2/resize:fit:1244/format:webp/0*DRPQ3KcodPIFNmBD)

By default each new connection added will have a default Back Pressure Object Threshold of 10,000 objects and Back Pressure Data Size Threshold of 1 GB. This means maximum 10,000 objects or Threshold data size of 1GB will be allowed to queue before back pressure is applied. The progress bars shown in the image change color based on the queue percentage: Green (0–60%), Yellow (61–85%) and Red (86–100%).

**flow.xml.gz:** Everything we put onto the NiFi User Interface canvas is written, in real time, to one file called the flow.xml.gz. This file is located in the _nifi/conf_ directory by default. Any change made on the canvas is automatically saved to this file. In addition, NiFi automatically creates a backup copy of this file in the archive directory when it is updated. You can use these archived files to rollback flow configuration. To do so, stop NiFi, replace flow.xml.gz with the desired backup copy, then restart NiFi. In a clustered environment, stop the entire NiFi cluster, replace the flow.xml.gz of one of the nodes, and restart the node also remove flow.xml.gz from other nodes. Once you confirm the node starts up as a one-node cluster, start the other nodes. The replaced flow configuration will be synchronized across the cluster.

NiFi Architecture
=================

![Figure: 1 NiFi architecture diagram, referred from NiFi doc](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*DG-o_x31iquSATABx5eATw.jpeg)

NiFi executes within a JVM on the host operating system. The primary components of NiFi are as follows:

*   **Web Server:** The purpose of the web server is to host NiFi’s HTTP-based command and control API.
*   **Flow Controller:** The flow controller serves as the brain of NiFi. Controls the running of Nifi extensions and schedules allocation of resources for this to happen.
*   **Extensions:** This can be considered as various plugins that allow NiFi to communicate with other systems.
*   **FlowFile Repository:** The FlowFile Repository is where NiFi keeps track of the state of what it knows about a given FlowFile that is presently active in the flow.
*   **Content Repository:** The Content Repository is where the actual content bytes of a given FlowFile live.
*   **Provenance Repository:** The Provenance Repository is where all provenance event data is stored.

NiFi is also able to operate within a cluster. Apache ZooKeeper is responsible for the coordination and fail over. Clustering gives more power in concurrent processing and integration flows.

Unboxing Apache NiFi
====================

When you start NiFi, you finally land on its web interface. The web UI facilitates a platform on which you can create automated dataflows, as well as visualizing, editing, monitoring, and administering those dataflows. Without writing any code NiFi’s user interface allows you to build your pipeline by drag and drop components on the canvas. The below screenshots of NiFi application highlights the different segments of the UI.

![Figure: 2 Apache NiFi web UI](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*eSz1tufrLWPHYwSxGi5qfQ.png)

The **Components Toolbar** runs across the top left portion of your screen. It consists of the components you can drag onto the canvas to build your dataflow.

![Figure: 3 Components Toolbar](https://miro.medium.com/v2/resize:fit:886/format:webp/1*_7HLP1PSAhv1tH8DXswT7A.png)

*   **_Processors_** are the basic blocks for creating a data flow. Every processor has different functionality, which contributes to the creation of output flowfile.
*   **_Input port_** is used to get data from the processor, which is not present in that process group.
*   **_Output Port_** provide a mechanism for transferring data from a Process Group to destinations outside of the Process Group. All Input/Output Ports within a Process Group must have unique name
*   **_Process Group_** can be used to logically group a set of components so that the dataflow is easier to understand and maintain.
*   **_Remote Process Group_** is similar to Process Group the only difference is Remote Process Group references a remote instance of NiFi.
*   **_Funnel_** is a NiFi component that is used to combine the data from several Connections into a single Connection.
*   **_Template_** helps to reuse the data flow in the same or different NiFi instances.
*   **Label** are used to provide documentation to parts of a dataflow.

**Status Bar** placed under the Components Toolbar provides information about the number of threads that are currently active in the flow, the amount of data that currently exists in the flow, how many Remote Process Groups exist on the canvas in each state (Transmitting, Not Transmitting), how many Processors exist on the canvas in each state (Stopped, Running, Invalid, Disabled), how many versioned Process Groups exist on the canvas in each state and the timestamp at which all of this information was last refreshed. Additionally, if the instance of NiFi is clustered, the Status bar shows how many nodes are in the cluster and how many are currently connected (above _figure(2)_ does not show cluster information, since it is not clustered).

On the right side of the canvas is **Search**, and the **Global Menu**. Searching functionality helps to easily find components on the canvas. Components can be searched by name, type, identifier, configuration properties, and their values. Search results can be refined using _Filters_ and _Keywords,_ these features provide an overall good search experience.

![Figure: 4 Global Menu](https://miro.medium.com/v2/resize:fit:434/format:webp/0*MEiXrZS0za0ZPvTP)

The Global Menu contains options that allow you to manipulate existing components on the canvas. _Summary_ helps the user understand how the DataFlow is functioning at a higher level. _Bulletin Board Page_ provides an interface to view and filter Bulletins from all the components [eg: error reported by each component is displayed here].

In addition to the statics provided by each component NiFi will also notify any issues of severity (Debug, Info, Warning, Error) with its messages as Bulletin. Bulletins from all components can also be viewed and filtered in the Bulletin Board Page. Whenever a component reports a Bulletin, a bulletin icon (looks like a sticky note) is displayed on that component. System-level bulletins are displayed on the Status bar near the top of the page.

_Templates_ imported, added or exported can be managed in the Template Management Page. Templates in NiFi are explained briefly in later session of this article.

While monitoring a dataflow, users often need a way to determine what happened to a particular data object (FlowFile). NiFi’s _Data Provenance_ page provides that information, this is possible since NiFi records and indexes data provenance details as objects flow through the system

_Flow Configuration History_ is used to view all the changes that have been made to the dataflow. The history can aid in troubleshooting, such as if a recent change to the dataflow has caused a problem and needs to be fixed.

The _Controller Settings_ page provides the ability to change the name of the NiFi instance, add comments describing the NiFi instance, and set the maximum number of threads that are available to the application. It also provides ability to add and configure Controller Services and Reporting Tasks.

The _Operate Palette_ sits to the left-hand side of the screen. It consists of buttons for managing flowfile, concurrency for processors and other settings.

_Navigate Palette_ gives the option to pan around the canvas, and to zoom in and out. The “_Birds Eye View_” of the dataflow provides a high-level view of the dataflow and allows you to pan across large portions of the dataflow.

_Breadcrumbs_ can be found to the left-bottom of the screen, this gives the option to navigate into and out of Process Groups, the breadcrumbs show the depth in the flow, and each Process Group that you entered to reach this depth. Each of the Process Groups listed in the breadcrumbs is a link that will take you back up to that level in the flow.

Type of Available Processors
============================

NiFi contains different Processors out of the box along with the capability to write custom processors. These Processors which are the building blocks of NiFi, provide the capability to consume data from various sources route, transform, process, split, and aggregate data, and distribute data to almost any system. The below table represents some of the frequently used Processors, categorizing them by their functions.

<b>[other]Figure: 5 Type of Available Processors[/other]</b>

Nifi Templates
==============

NiFi allows us to build very large and complex DataFlows using basic components like Processor, Funnel, Input/Output Port, Process Group, and Remote Process Group. As we know these components can be considered as the basic building blocks for constructing a DataFlow. At times, though, using these small building blocks can become tedious if the same logic needs to be repeated several times.

To address this scenario NiFi offers the concept of Templates. A Template is a way of combining these basic building blocks into larger building blocks. Once a DataFlow has been created, parts of it can be formed into a Template. These templates can then be exported as XML and share with others or can be dragged onto canvas to build complex flows. This property makes it easier to reuse and distribute the NiFi flows.

Creating a Template
-------------------

To create a Template, select the components that are to be a part of the template, and then click the “_Create Template_” button in the Operate Palette (at the left hand side of the NiFi canvas). Clicking this button without selecting anything will create a Template that contains all of the contents of the current Process Group. Each template must have a unique name.

Importing or Uploading a Template
---------------------------------

To use a Template received by exporting from another NiFi, the first step is to import the template into this instance of NiFi. You may import templates into the canvas as a whole dataflow or to any Process Group.

From the Operate Palette, click the “Upload Template” button, this will open a Upload Template dialog. Find and choose the template file to be imported to the instance of NiFi.

Instantiating or Adding a Template
----------------------------------

Once a Template has been created or imported to the NiFi instance, it is ready to be instantiated, or added to the canvas. This is accomplished by dragging the Template icon from the Components Toolbar onto the canvas. Choose the template from the dialog box showing the list of templates present in the current NiFi instance.

Managing Templates
------------------

Ability to export or import dataflow partially or completely is one of the most powerful features of NiFi. You can select Templates from the Global Menu to open a dialog that displays all of the Templates that are currently available, filter the templates to see only those of interest, export, and delete Templates.

**Exporting a Template:** Once a Template has been created, it can be shared with others by downloading the template file from the Template Management page. Click the “Download” button in the Template Management page to download the template as an XML file.

**Removing a Template:** To delete a Template, which are no longer needed, locate it in the table of Template Management page and click the “Delete” button.

Building Apache NiFi data flow
==============================

Starting NiFi
=============

You can launch NiFi via Docker or install it on your local machine.

_Run a NiFi container:_ You can follow the below command to download and run the latest version of NiFi.

```
docker run -d -h nifi -p 8080:8080 — name nifi_latest — memory=4g -v /docker/apache/nifi apache/nifi:latest
```

_Download and run NiFi:_ Download the NiFi installation file from [Nifi official website](https://nifi.apache.org/download.html) .

1.  Choose nifi-x.y.z-bin.zip or nifi-x.y.z-tar.gz for Linux(eg, [nifi-1.12.1-bin.zip](https://www.apache.org/dyn/closer.lua?path=%2Fnifi%2F1.4.0%2Fnifi-1.4.0-bin.zip)).
2.  Extract to a specific folder (eg. c:\Users\username\nifi).
3.  Find and execute _run-nifi.bat_ or _run.sh_ in “your nifi folder\bin\” based on the operating environment.

> We can verify or access the NiFi web UI by accessing [http://localhost:8080/nifi](http://localhost:8080/nifi)

Building Nifi dataflow
----------------------

We will try to build a real word like scenario to get the notion of NiFi. You can find the template file and other required files to run this example in the [github](https://github.com/VishnuGurudathan/nifi-examples).

The data flow we are going to build will fetch CSV files from a data source, process it and save it to MySQL and pass data to Kafka based on some condition. Consider we want to listen to some data source where some _data logger_s will send data as CSV files. NiFi will listen to the data source, fetch the files, parse and load the data to the database. Since we are considering files which contain some sensor reading we will route those data to Apache Kafka based on condition. Those data can then be used by other system or NiFi itself for other activities like alarm processing.

The data source we are considering is a directory location in the local system, however this can be an FTP server, HDFS or an AWS S3, even the data source can be from all of them.

To start with we will add a process group to the canvas. After dragging the process group icon to the canvas NiFi will prompt for a process group name (in this example ‘Logger data parsing’ is the process group name.) We will group all the processes under this process group that we just created.

![Figure: 6 Add Processor](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*nDp-3fWCKzBxKy1N)

To fetch files from the directory we will need to add _GetFile_ processor. Drag the processor icon near the NiFi logo in Components Toolbar. Search in Filter, choose GetFile to add to NiFi canvas.

You can configure any processor by right clicking on it. For the GetFile processor we need to configure the _Input Directory_ location. Configure other settings according to the behavior you expect. You can schedule the processor to work as a cron job or time driven. Here we will choosing the time driven approach.

![Figure: 7 Configure GetFile Processor](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*d_IB395YXH0g5Yvo)

After configuring GetFile to read the CSV we now need to add _SplitRecord_ processor to the canvas for splitting individual lines. You can add SplitRecord to the canvas in the same way we did for GetFile. After that we need to establish a connection between the two by dragging from processor GetFile to SplitRecord processor as shown in the _figure(8)_. The NiFi will provide a simple queue between the two processors with some default threshold.

![Figure: 8 Connecting Processors](https://miro.medium.com/v2/resize:fit:1228/format:webp/0*bEK4GCRCTg6dPId4)

The _figure(9)_ shows the property configuration for SplitRecord. We need to configure _Record Reader_ and _Record Writer_ to read and write records after splitting. To configure Record Reader and Record Writer we have to add them as service in NiFi’s _Controller Services_.

![Figure: 9 Configure SplitRecordProcessor](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*UEWHqFRvalvCVEY9)

Since our input format is of CSV we will add _CSVReader_ as Record Reader and use _JsonRecordSetWriter_ as Record Writer to write records in the JSON format.

![Figure: 10 Adding Controller Service](https://miro.medium.com/v2/format:webp/0*mSZKu2R8YlPa_j7g)

**Adding Controller Service**

We can add a controller service by clicking on the configuration icon at _Operate Palette._ This will open up the process group configuration screen _(in our case Logger data parsing Configuration), ‘Add Controller service’_ box will open after clicking on the **+** sign on the top right corner, similar to what we did for adding processors. We can filter and add the service as shown in the _figure(10)._ Since we are in _Controller Service_ to add Record Reader and Record Writer we will also add _DBCPConnectionPool_(which is required for upcoming processors).

After adding ‘_CSVReader_’, ‘_JsonRecordSetWriter_’ and ‘_DBCPConnectionPool_’ we need to configure them individually before enabling them.

![Figure: 11 Process group configuration screen](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*C1rhzBankkCIeCMs)

At the right end we can see the Configure, Enable and Delete symbol for each service. We can configure each service by clicking the Configure symbol.

_Configure Record Writer:_ We are good to go with the default properties of _JsonRecordSetWriter_ for this example. However explore the configuration to get some understanding and you can also change the default name or properties for your customization.

_Configure Record Reader:_ Choose the **Schema Access Strategy** to ‘_Use String Field From Header_’ for _CSVReader_ in its property. For this example we are extracting the schema form the CSV header.

_Configure DBCPConnectionPool:_ Configure _Database Connection URL, Driver Class Name, Database Driver Location,_ and _Database username_ and _password_ in the properties of DBCPConnectionPool as shown in the _figure(12)_.

![Figure: 12 DBCPConnectionPool Configuration](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*JoanwpPQitqyCew3)

After configuring the services enable them with _Service Only_ scope. In the SplitRecord properties add **‘CSVReader’** and **‘JsonRecordSetWriter’** for Record Reader and Record Writer respectively. Also in the properties of SplitRecord for this example we will configure **Records Per Split** as ‘1’ since we only need one row in each flow file.

Configure and connect processors ConvertJsonToSQL and PutSQL, in the order as shown in the _figure(14)_ to convert JSON to SQL and update on database. Add the already created service DBCPConnectionPool as the JDBC Connection Pool property for both processors. Also configure _Statement type_ as **INSERT** and provide _Table name_ and _Catalog name_; in our case **logger_data** and **logger_data_db** respectively. The _figure(13)_ shows the configuration used for ConvertJsonToSQL processor.

![Figure: 13 Configure ConvertJsonToSQL Processor](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*k1YPQvZ4fWr01z50)

By this we completed our flow to split CSV files and save data in the database. Since we want to experience how we can route a flow file based on some condition, we will use _ExtractJsonPath_ processor to extract some content from the file on which we want to apply the condition. As we know the output of the SplitRecod are flow files with a single line from our initial CSV file in JSON format, we will direct the flow file to ExtractJsonPath from SplitRecord**.**

The _type_ and _value_ field in the input file will be extracted from the JSON using ExtractJsonPath processor. These extracted fields will be added as attributes of the flow file. FlowFiles routed to success relationship from ExtractJsonPath are then routed to _RouteOnAttribute_ processor. In the RouteOnAttribute processor add a new custom property ‘Alarm Trigger Level’ with value _‘${type:equals(‘Temperature’):and(${value:ge(70)})}’_, where the value is a NiFi Expression Language(EL). EL statement is used to check if the type is equal to ‘Temperature’ and its value is greater than 70.

If the condition on attribute value is satisfied at RouteOnAttribute then the flow files will be directed to the Alarm Trigger Level route which is then connected to the Kafka Producer (_PublishKafka_2_6_ NiFi processor).

For Demo we simply use LogMessage and LogAttribute processors to log failure, unmatched and success flows of EvaluateJsonPath, RouteOnAttribute and PublishKafka_2_6 processors respectively. The LogMessage and LogAttribute processors will simply log to NiFi’s log(nifi-app.log) based on the configured log level.

> The complete NiFi flow is shown in the below figure(14)_._

![Figure: 14 Logger data parsing NiFi setup](https://miro.medium.com/v2/resize:fit:2000/format:webp/0*UdSlVwbfUXqeQSUm)

_We can run the application by running the processor group from the Operate Palette or run individual processors by right clicking on them._

> You can find the template and other resource in the [GitHub repository](https://github.com/VishnuGurudathan/nifi-examples) below.

[VishnuGurudathan/nifi-examples
------------------------------

### This repository will contain nifi example templates with required files(if any) for running them. Follow the link to…

github.com](https://github.com/VishnuGurudathan/nifi-examples?source=post_page-----ab63b2451891--------------------------------)

**Common use cases or applications**
====================================

NiFi empowers you to quickly start moving data from multiple different types of source systems to various types of target systems including HDFS, Databases, Streams, etc. This is particularly important in Big Data where the aim is to ingest from a variety of data sources like ERP, CRM, Files, HTTP Links, IoT data, etc. To ingest data from various sources into the Bigdata platform for further analysis needs a well-rounded, scalable, fault-tolerant solution to handle the entire “data flow” logistics of an enterprise. Enterprises are also looking for tools and technologies through which rapid development can be done, supporting ease of use for the developers, reliability in data delivery, scalability to handle large data sets, and lineage tracking.

**Here are some of the reasons for using Apache Nifi:**

*   Allows you to do data ingestion to pull data into NiFi, from numerous data sources and create flow files
*   It offers real-time control which helps you to manage the movement of data between any source & destination.
*   Event though NiFi is not limited to an ETL tool, it can be a managed ETL service

In an IoT environment data is the fuel. The data from numerous sources need to be processed to derive meaningful information. An increase in the number of IoT and wearable devices has resulted in a large volume of data. These big data need to be injected into different tools for processing and extracting information. For example, these data need to be fed to data warehouses like Redshift for large scale data storage and analysis or to a more complex data lake.

The raw data from different sources can be injected into NiFi by leveraging the variety of Data Ingestion processors. These data from different sources can be routed to different built-in or custom processors in NiFi for data transformation, cleansing, extraction, etc. The processed data can then be stored or fed to many systems like databases, cloud solutions, streaming engines like Kafka, Amazon Kinesis, etc, data warehouses like Redshift, or to any other streaming and processing engines like Spark, Fink, Beam, etc. The Data Egress or Sending Data Processors of NiFi can even send data to multiple sources to form a data lake.

![Figure: 15 High-level system design of data collection and integration](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*4abbnbwnrLh3Dabegmam0g.png)

_Figure(15)_ shows an high-level system design to collect and process data from different source to data lake. Apart form NiFi the design also relay on [MiNiFi](https://nifi.apache.org/minifi/index.html) — a subproject of Apache NiFi focusing on the collection of data at the source of its creation.

**Alternatives to Apache NiFi**
===============================

Following are some of the alternative for NiFi in opensource and cloud solution.

[**Streamsets**](https://streamsets.com/) is an opensource solution similar to NiFi

**Cloud Solutions:**
--------------------

*   Amazon offers [**Data Pipeline**](https://docs.aws.amazon.com/en_us/datapipeline/latest/DeveloperGuide/what-is-datapipeline.html)
*   Google offers its [**Dataflow**](https://cloud.google.com/dataflow/)
*   IBM has its [**InfoSphere DataStage**](https://www.ibm.com/us-en/marketplace/datastage)
*   Microsoft has [**Azure Data Factory**](https://azure.microsoft.com/en-us/services/data-factory/)

What’s Next?
============

If you’ve made it until here, you obtained an over all idea of what is NiFi and how to build a working platform to leverage your application. This article scratches only the tip of the iceberg; there are a lot to cover like data provenance, logging, variables and parameters, labels, versioning, creating custom processors and controllers, NiFi registry, etc. The supporting tools for extensive automation capabilities which is also a huge area to cover.

I hope this article will enhance your school of thought on data integration, processing, and distribution.

References:
===========

*   [Nifi documentation](https://nifi.apache.org/docs/nifi-docs/html/user-guide.html)
*   [Nifi Registry documentation](https://nifi.apache.org/docs/nifi-registry-docs/index.html)
