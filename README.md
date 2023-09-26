# TCC_AI_FIWARE

AI component to FIWARE environment

## Requirements

To execute this project you need to have a fiware cluster with Orion Context Broker and the STH Comet component

## Running on docker-compose


```
    docker-compose up

```



## Project Architecture

![project architecture](./docs/architecture.png)


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
