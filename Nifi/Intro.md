An Overview of Apache NiFi
==========================

The capabilities of Apache NiFi for managing data flows are examined, providing an in-depth exploration of its essential concepts, features, services, and user interface.

![Image Generated by DALL-E 3 Inspired by The Logo of Apache NiFi.](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*IB0je0Fk3Tia_i7DJTJBSA.jpeg)

I. INTRODUCTION
===============

In recent years, the data processing tasks within various organizations have become increasingly complex , necessitating the use of advanced data flow tools. Consequently, this article aims to provide a comprehensive overview of Apache NiFi inculding its definition, performance expectations, characteristics, and features. Additionally, the core concepts of Apache NiFi are explained in detail, with a significant emphasis on its User Interface (UI). This ensures that all important information about Apache NiFi is thoroughly covered. By using Apache NiFi, several advantages can be obtained, such as reducing system failures, processing data simultaneously, eliminating data processing boundaries, enhancing data management, and increasing security **[1]**.

> _Please refer to the “_[Installation of Apache NiFi](https://medium.com/@alkhanafseh/installation-of-apache-nifi-2856fca5bbdc)_” article_ **_[2]_** _for a complete installation guide of latest version of Apache NiFi “1.25.0”._
> 
> _Please refer to the “_[Executing Python Scripts and SQL Quries In Apache NiFi](https://medium.com/@alkhanafseh/executing-python-scripts-and-sql-quries-in-apache-nifi-4eb49945846f)_” article_ **_[3]_** _for a detailed guide on how to run Python scripts and SQL queries within Apache NiFi._

II. UNDERSTANDING APACHE NIFI: DEFINITION, PERFORMANCE EXPECTATIONS, CHARACTERISTICS, AND FEATURES.
===================================================================================================

Apache NiFi is a highly valuable data flow system designed to automate and schedule various data operations across different processes **[1]**. It is capable of handling both simple and complex systems effectively. The performance of Apache NiFi, in terms of IO, CPU, and RAM utilization, is spectacular as well. Apache NiFi has numerous characteristics and features **[1]**, which can be highlighted in the following points:

*   Flow management
*   Ease of use
*   Security
*   Extensible architecture
*   and flexible scaling model

III. THE CORE CONCEPTS OF APACHE NIFI
=====================================

The most important concepts realted to Apache NiFi are DataFlow Manager (DFM), FlowFile, Bulletin, Processor, Connection, Controller Service, Flow Controller, and Process Group. The significance of each concept is as follows **[4]**:

*   **DFM**

In simple words, a DFM is the user who has different permissions and complete management of Apache NiFi.

*   **FlowFile**

The FlowFile concept refers to each object moving through the system. It has two main parts: attributes and content. The first one stores metadata about the FlowFile, such as its filename, size, etc. The standard attributes that each FlowFile contains are _Universally Unique Identifier (UUID)_, used to distinguish the FlowFile; _filename_, used to represent the name of the output of the data when it is written to some path; and _path_, used to define the path of the filename. On the other hand, the content part is responsible for storing the actual data of the FlowFile.

*   **Bulletin**

It can be considered a service reporter tool that is available for each service. It provides critical information such as rolling statistics, current status, and severity levels such as Debug, Info, Warning, and Error, giving insights into the current situation of the component.

*   **Processor**

A Processor, as the name suggests, is responsible for performing the actual work, such as data routing and transformation, as it has direct access to the attributes and the content of the given FlowFile. For example, processor has the ability to read data files, execute different software languages such as Python scripts, and executing different SQL quries. An example of Apache NiFi processor is shown in Figure 1.

*   **Connection**

A Connection can be regarded as the link between different processors, see Figure 1. It manages the interaction between the processors by establishing queues. A queue in Apache NiFi refers to a buffer that has the ability to store FlowFiles. Therefore, the output of one processor, the FlowFile, is stored in a queue until the other processor is ready to process it.

![Figure 1. Detailed View of a Processor and Connection in Apache NiFi.](https://miro.medium.com/v2/resize:fit:1186/format:webp/1*hEoe0hYoPe-PGAl_Pjbo2g.png)

*   **Controller Service**

When a Controller Service is created, it will automatically start up every time Apache NiFi is initiated. Several essential services can be specified in the Controller Service section. For instance, DBCPConnectionPool and CSVRecordSetWriter are utilized to establish connections between various database systems and Apache NiFi, and to enable writing CSV files to the local system, respectively. Once defined, these services can be utilized by any processors.

*   **Flow Controller**

The Flow Controller, in short, manages the threads used by different processes. As a result, it can dynamically adjust the number of threads used for each flow, increasing or decreasing as necessary.

*   **Process Group**

Grouping a set of processors and their connections is called a Process Group. The input and output data of this Process Group can be managed by Input Ports and Output Ports, respectively. An example of a Porcess Group is obviously shown in Figure 2.

![Figure 2. Detailed View of a Process Group in Apache NiFi.](https://miro.medium.com/v2/resize:fit:776/format:webp/1*fhS7mYdkjHFi-PcrITAFYQ.png)

IV. APACHE NIFI USER INTERFACE
==============================

Specifically, Apache NiFi UI comprises six main elements: the components toolbar, status bar, navigation palette, operation palette, global menu, and canvas **[6]**. The example of the Apache NiFi interface is clearly illustrated in Figure 3 below.

![Figure 3. Apache NiFi Main Page.](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*GAhZRq7zui6xb5Jqnc7xVg.png)

Components Toolbar
------------------

The components toolbar, as shown in Figure 4, comprises seven main elements: Processor, Input & Output ports, Process Group, Remote Process Group, Funnel, Template, and Label. The first three components have been discussed in the preceding section.

![Figure 4. Components Toolbar in Apache NiFi.](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0SP58bwydDgK16jK-FYYbA.png)

*   **Funnel**

Generally, Funnel is utilized when data from several Connections need to be merged into a single Connection. When placed on the canvas, it appears as the symbol shown in Figure 5.

![Figure 5. Funnel Symbol in Apache NiFi UI.](https://miro.medium.com/v2/resize:fit:604/format:webp/1*kXxzGGC2vSe1sQw2wUQaZQ.png)

*   **Remote Process Group**

A Remote Process Group in NiFi is used to facilitate the transfer of data between different NiFi systems.

*   **Template**

Apache NiFi enables DFMs to create templates with unique names for their dataflows. These templates can be found inside the Template icon in the Components Toolbar. This feature allows them to easily reuse specific parts of the flow by simply selecting the corresponding template they have created.

*   **Label**

In summary, Apache NiFi offers the capability to add extra labels to the canvas, enabling users to incorporate additional information, comments, or advices. This can be achieved by dragging the label icon onto the canvas. Once positioned on the canvas, it will resemble the shape displayed in Figure 6.

![Figure 6. Label in Apache NiFi](https://miro.medium.com/v2/resize:fit:680/format:webp/1*8aSFicIgsIven7caJvlpPQ.png)

Status Bar
----------

As depicted in Figure 7, the Status Bar plays a crucial role in displaying vital information about the currently running dataflow. It consists of 15 different components. The first one is _active threads_, which is the number of total threads being used by the current dataflow. The second one is _total queued data_, which represents the amount of data waiting to be processed by other processors. The third and fourth components are _transmitting and not transmitting remote process groups_, which show the count of the currently running groups for each state, respectively. The next four components are related to the status of components, indicating if they are _running_, _stopped_, _invalid_, or _disabled_, respectively. On the other hand, the subsequent five components are responsible for version states. The _Up to date versioned process group_ shows the latest flow version. Moreover, the _Locally modified versioned process group_ indicates the number of local changes that have been made. The _Stale versioned process group_ component informs if there is a new available version of the flow. The _Locally modified and Stale versioned process group_ occurs when the combination of the previous two components occurs simultaneously. The _Sync failure versioned process group_ indicates if there is a conflict in synchronizing the flow with the registry [5]. Additionally, the _Last refresh time_ component displays the last refresh time of the current dataflow. Finally, the _search bar_ is used to make general searches in Apache NiFi.

![Figure 7. Detailed View of Status Bar in Apache NiFi.](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_vCTx7iJ0v6zTCDqJVOz0Q.png)

Navigate palette, Bird’s eye view, Breadcrumbs, and Canvas
----------------------------------------------------------

The Navigate Palette enables DFMs to navigate around the canvas and to zoom in and out. The Bird’s Eye View is a part of the Navigate Palette that allows the required components to be displayed on the canvas within one frame. The Breadcrumbs section shows the depth of the current dataflow and process groups, which can be used to navigate around them. Eventually, Canvas is the home screen of Apache NiFi which is supposed to carry different services or porcessors.

Operate Palette
---------------

The Operate Palette is home to the main buttons of the flow, see Figure 8, providing DFMs flexibility to execute different actions. These include configuring system settings, such as modifying general flow information or adding new Controller Services. Additionally, the Operate Palette allows for a range of operations on the current flow, like enabling, disabling, running, stopping, copying, pasting, grouping, changing colors, and deleting components. It also features two buttons dedicated to creating a template for the current flow or uploading a previously saved template.

![Figure 8. Detailed View of Operate Palette in Apache NiFi.](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*YlWaKPcSPMlld_fCzeSlaw.png)

Global Menu
-----------

Specifically, the Global Menu is employed to make modifications to the existing components in the dataflow. It also facilitates access to the flow configuration history, node status history, controller settings, bulletin board, and available templates. Additionally, the “Help” section within the Global Menu provides further information about the components. Details regarding the current version of Apache NiFi can be found in the “About” section as well. The Global Menu of Apache NiFi is shown in Figure 9, below.

![Figure 9. Global Menu in Apache NiFi .](https://miro.medium.com/v2/resize:fit:426/format:webp/1*DfwyGZBnzOcIHXV_2punOA.png)

V. CONCLUSION
=============

In conclusion, the data flow management capabilities of Apache NiFi are explained through a comprehensive understanding of its essential definitions, concepts, features, services, and UI, all of which are presented with clear explanations and illustrative examples. Each component of the UI is thoroughly explained in detail. Consequently, this article can be regarded as the first step for learning Apache NiFi.

![captionless image](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_Y-W6EVF2acXimZUzq1QCA.gif)

VI. REFERENCES
==============

**[1]** Apache NiFi Team (n.d). Apache NiFi Overview. Accessed on [15.03.2024]. Retrieved from: [https://nifi.apache.org/docs/nifi-docs/html/overview.html](https://nifi.apache.org/docs/nifi-docs/html/overview.html)

**[2]** Alkhanafseh, Y. (2024). Installation of Apache NiFi. Accessed on [29.03.2024]. Retrieved from: [https://medium.com/@alkhanafseh/installation-of-apache-nifi-2856fca5bbdc](https://medium.com/@alkhanafseh/installation-of-apache-nifi-2856fca5bbdc)

**[3]** Alkhanafseh, Y. (2024). Executing Python Scripts and SQL Quries In Apache NiFi. Accessed on [29.03.2024]. Retrieved from: [https://medium.com/@alkhanafseh/executing-python-scripts-and-sql-quries-in-apache-nifi-4eb49945846f](https://medium.com/@alkhanafseh/executing-python-scripts-and-sql-quries-in-apache-nifi-4eb49945846f)

**[4]** Apache NiFi Team (n.d). Apache NiFi User Guide. Accessed on [13.03.2024]. Retrieved from: [https://nifi.apache.org/docs/nifi-docs/html/user-guide.html](https://nifi.apache.org/docs/nifi-docs/html/user-guide.html)

**[5]** Trainingcred (n.d). Apache Nifi UI Components. Accessed on [14.03.2024]. Retrieved from: [https://trainingcred.com/apache-nifi-ui-components](https://trainingcred.com/apache-nifi-ui-components)

**[6]** Cloudera (n.d). USING APACHE NIFI. Accessed on [15.03.2024]. Retrieved from: [https://docs.cloudera.com/cfm/2.0.4/nifi-user-guide/topics/nifi-managing_local_changes.html](https://docs.cloudera.com/cfm/2.0.4/nifi-user-guide/topics/nifi-managing_local_changes.html)?