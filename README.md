# Tutorial on how to create and Dockerize your gRPC service
This repository contains template files and the steps required for creating your gRPC-enabled service and its own Docker 
container, compatible with AI4Europe platform and with 
[this pipeline orchestrator](https://github.com/DuarteMRAlves/Pipeline-Orchestrator). It is meant for a Python service, 
but the steps for a different language should be the same.

## First things first
Although you do not need to be an expert on the tools that are used for pipelines (Docker, protocol buffer, gRPC), it 
will be useful if you know the basics.

The **orchestrator** manages pipelines by launching each component in its own Docker container. Communication between each 
component is only possible because their interface is defined with Protocol Buffer (Protobuf for short), which 
specifies the component's inputs and outputs, as well as the service it provides.

A **Docker container** is basically an easily-deployable virtual machine. It has its own OS, libraries and tools, and is
(mostly) independent of the machine on which it runs.

**Protocol Buffer** is used to define the interface of a service. It is useful because it enables communication between 
services developed in different programming languages. For instance, your service developed in Python could receive 
requests from a Java client and send responses to a C++ visualizer. This is only possible because the messages' types 
are defined in a .proto file, which then generates two auxiliary files with the corresponding message types in the 
desired programming language.

## Before you begin
You'll need to have installed:
* [Docker](https://docs.docker.com/get-docker/)
* [Protobuf](https://github.com/protocolbuffers/protobuf) 
* [gRPC](https://grpc.io/blog/installation/) (for Python just `pip install grpcio`)

## Creating your component
1. Define the interface of your service in a .proto file and compile it
2. Create your service and a test client
3. Create a Docker image (and container) for your service 