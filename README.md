# Cosmos-Redshift

ML and Data Analytics Generic Enabler for FIWARE

*******
| Table of Contents |
| :--- |
| [Requirements](#requirements) |
| [Running on Docker Compose](#running-on-docker-compose) |
| [API](#api) |
| [Requesting Sync Analysis](#requesting-sync-analysis) |
| [Payload Description](#payload-description) |
| [Requesting Asynchronous Analysis](#requesting-asynchronous-analysis) |
| [Architectures](#architectures) |
| [Component Architecture](#component-architecture) |
| [Connection with FIWARE Project](#connection-with-fiware-project) |
| [Tutorials](#tutorials) |
| [1 - Setting FIWARE Instance to be Attached](#1---setting-fiware-instance-to-be-attached) |
| [2 - Discover Available Entities and its Attributes to Perform Analysis](#2---discover-available-entities-and-its-attributes-to-perform-analysis) |
| [3 - Request a 2D graph - Blocking](#3---request-a-2d-graph---blocking) |
| [4 - Perform a Correlation Analysis - Blocking](#4---perform-a-correlation-analysis---blocking) |
| [5 - Perform a Linear Regression - Blocking](#5---perform-a-linear-regression---blocking) |
| [Environment variables](#environment-variables) |
*******

## Requirements

To execute this project you need to have a FIWARE cluster with Orion Context Broker and the STH Comet component

## Running on Docker Compose

```
    docker-compose up
```

## API

Users can interact with this component through REST API, you can check all the samples shown here by clicking in this [collection]()

### Requesting Sync Analysis

To perform a synchronized analysis, you need to execute a POST request to **/api/sync/requestAnalysis** with a body as the sample below.

![body](./docs/payload.png)

#### Payload description

* **Action:** Action to be executed, accepted values are: (CORRELATION_ANALYSIS, LINEAR_REGRESSION_ANALYSIS, 2D_GRAPHICS);
* **Entity:** Entity ID to perform analysis;
* **Entity Type:** ID to entity type;
* **Fields:** Entity's selected fields to perform analysis **(In LINEAR_REGRESSION_ANALYSIS, the last field will consider as target of prediction)**;
* **Agg_method** Object of aggregation method to query data, if nothing were provided, the default value is LastN=100 **(lastN,dateFrom,dateTo)**;

### Requesting Asynchronous Analysis

To perform this kind of request, you need to execute a POST request to **/api/requestAnalysis** using the same payload as the previous [request](#requesting-sync-analisys)

## Architectures

### Component Architecture

![Project Architecture](./docs/architecture.png)

### Connection With FIWARE Project

![FIWARE Architecture](./docs//fiware-with-component.png)

## Tutorials

### 1 - Setting FIWARE Instance to be Attached

As mentioned in the project description, this is the FIWARE component, therefore, you must configure the FIWARE instance location (STH Comet and Orion Context Broker) the FIWARE service, and the service path.

All of the parameters are available in [Environment Variables](#environment-variables), just set up the [Docker Compose File](./docker-compose.yml). The block below shows an example of how the Docker Compose file should be set, considering that there is a FIWARE instance running on "*172.26.64.1*", having "*smart*" as the service name and "*/*" as the service path.

```
   version: '3'
    services:

    rabbitmq:
        image: "rabbitmq:3-management"
        #hostname: rabbitmq
        ports:
        - "5672:5672"  
        - "15672:15672"
    
    app:
        build:
        context:  
        ports:
        - "5000:5000" 
        depends_on:
        - rabbitmq
        environment:
        - INTERNAL_RABBIT_MQ_HOST=rabbitmq
        - INTERNAL_RABBIT_MQ_PORT=5672
        - STH_COMET_HOST=172.26.64.1
        - STH_COMET_PORT=8666
        - ORION_CONTEXT_BROKER_HOST=172.26.64.1
        - ORION_CONTEXT_BROKER_PORT=1026
        - FIWARE_SERVICE=smart
        - FIWARE_SERVICE_PATH=/
```

With docker-compose.yml set, [Execute Docker Container](#running-on-docker-compose)

### 2 - Discover Available Entities and its Attributes to Perform Analysis

First of all, make sure to set correctly all [Envirorment Variables](#environment-variables).

Before starting to request an advanced analysis, it's recommended the read all entities and attributes available on the attached fiware instance. You can check all entities by a simple GET request to **/api/availableEntities**. The image below demonstrates an example.

![Get Entities](./docs/get-entities.png)

As demonstrated above, the example FIWARE instance has an Entity type called "eggPrediction" with ID "urn:ngsi-ld:entity:986463ec-3f51-11ee-be56-0242ac120002" and attributes: "cracked_eggs", "dateReading" and "humidity".

### 3 - Request a 2D Graph - Blocking

To perform a 2D Graph request, you have to execute a POST request to **/api/sync/requestAnalysis** using the action field as "2D_GRAPHIC" as shown below.

Please, pay attention that we have use **entity** with the same value of **id** got from the [previous sample](#2---discover-available-entities-and-its-attributes-to-perform-analysis) and **entity_type** as the same of collected on [previous sample](#2---discover-available-entities-and-its-attributes-to-perform-analysis)

![Request 2D Graphic](./docs/2d_req_analysis.png)

In this case, you should receive an answer like this

![Response 2D Graphic](./docs/2d_resp_analysis.png)

Attribute **img** is the result of the analysis formatted as a PNG image and encoded by Base64 method. You can use the [Base64 Guru Site](https://base64.guru/converter/decode/image) to convert raw data into images. Using the last example, we got the following image.

### 4 - Perform a Correlation Analysis - Blocking

Continuing with the same FIWARE instance, let's request a correlation analysis with attributes "cracked_eggs" and "temperature". Again, create a POST request, but now change the payload as shown below.

![Request Correlation Payload](./docs/request-correlation.png)

The component should return a message like that.

![Result Correlation Payload](./docs/result-correlation.png)

Attribute **img** is the result of the analysis formatted as a PNG image and encoded by Base64 method. You can use the [Base64 Guru Site](https://base64.guru/converter/decode/image) to convert raw data into images. Keeping the last example, we got the following image.

![Converted Image](./docs/result-correlation-img.png)
### 5 - Perform a Linear Regression - Blocking

Continuing with the same FIWARE instance, let's request a linear analysis with attributes "humidity", "temperature" and "cracked_eggs" as **Target**. Again, create a POST request, but now change the payload as shown below.

![Linear Regression Request](./docs/request-lin-reg.png)

The component should return a message like this.

![Result Linear Regression](./docs/result-lin-reg.png)

In this case, the parameters of linear regression are returned (coefficients and intercept), as well as a graph indicating the model prevision versus the real value measured.

### Environment variables

```
    INTERNAL_RABBIT_MQ_HOST = "localhost"
    INTERNAL_RABBIT_MQ_PORT = 5672


    STH_COMET_HOST = "localhost"
    STH_COMET_PORT = 8666

    ORION_CONTEXT_BROKER_HOST = "localhost"
    ORION_CONTEXT_BROKER_PORT = 1026

    FIWARE_SERVICE=smart
    FIWARE_SERVICE_PATH=/

```
