# Tutorial on how to create and Dockerize your gRPC service
This repository contains template files and the steps required for creating your gRPC-enabled service and its own Docker 
container, compatible with AI4Europe platform and with 
[this pipeline orchestrator](https://github.com/DuarteMRAlves/Pipeline-Orchestrator). It is meant for a Python service, 
but the steps for a different language should be similar.

## First things first
Although you do not need to be an expert on the tools that are used for pipelines (Docker, protocol buffer, gRPC), it 
will be useful if you know the basics.

The **orchestrator** manages pipelines by connecting each component in its own Docker container. Communication between each 
component is only possible because their interface is defined with Protocol Buffer (Protobuf for short), which 
specifies the component's inputs and outputs, as well as the service it provides.

A **Docker container** is basically an easily-deployable virtual machine. It has its own OS, libraries and tools, and is
(mostly) independent of the machine on which it runs.

**Docker-compose** is a helper utility for docker that launches multiple Docker containers. This tool starts the containers with the components for the pipeline and also the orchestrator, that then connects the components and executes the pipeline.

**Protocol Buffer** is used to define the interface of a service. It is useful because it enables communication between 
services developed in different programming languages. For instance, your service developed in Python could receive 
requests from a Java client and send responses to a C++ visualizer. This is only possible because the messages' types 
are defined in a .proto file, which then generates two auxiliary files with the corresponding message types in the 
desired programming language.

## Before you begin
You'll need to have installed:
* [Docker](https://docs.docker.com/get-docker/)
* [Protobuf](https://github.com/protocolbuffers/protobuf) (for Python just `pip install protobuf`)
* [gRPC](https://grpc.io/blog/installation/) (for Python just `pip install grpcio`)
* [gRPC Reflection](https://grpc.io/blog/installation/) (this usually does not come with the grpc instalation, but for Python just `pip install grpcio-reflection`)

## Creating your component
1. [Define the interface of your service in a .proto file and compile it](#defining-the-service-interface)
2. [Create your service and a test client](#creating-your-service-and-client)
3. [Create a Docker image (and container) for your service](#creating-your-docker-image) 

### Defining the service interface
The first task is to think of what your service needs to receive as input and what it produces as output. You'll then 
need to define these inputs and outputs in a .proto file. See the file [template.proto](template.proto) for a simple example of what your .proto will look like, and [common_msgs.proto](Useful%20Things/common_msgs.proto) for some examples of messages for common data structures such as arrays. When defining this interface it is very important to also consider what the other users of your service will need from it. You should try to have generic and simple interfaces that other users can incorporate in their components. The other users should receive the information in a usual format that does not require much logic to parse.

Note that you can also define multiple services with just one proto file. To achieve this you'd need to define one 
service with multiple methods. Later you can specify which method to execute in the definition of the pipeline.

For instance, if you have an approach to detect the pose of a hand from an image, then you can define several methods around this. First you could have a generic method that just outputs the hand pose. However, for visualization purposes, you could have a second method that outputs the original image with the pose overlayed. With this approach, you have a generic inteface in the form of the first method, that can be incorporated into any pipeline, and you have an interface focused on simplicity in the form of the second method, for users that only want to visualize the hand pose.

Once you have defined your interface with a proto file, you have to compile it. In the directory of your proto file, 
open a terminal and execute

`python -m grpc_tools.protoc --proto_path=./path_to_proto_files --python_out=. --grpc_python_out=. name_of_proto.proto`

This should generate two files, `your_service_pb2.py` and `your_service_pb2_grpc.py`, which you'll use in your service.

### Creating your service and client

Although not necessary, Protobuf has a great tutorial on how to do this. Alternatively, you can simply copy 
`template_server.py`, adjust the names of the files to match your service and add its functionalities. Repeat the same 
process for `template_client.py` where you'll send a request to your service to verify that if functions as expected.

### Creating your Docker image

We're almost done! Now you just need to create your Docker image that will be used to launch the Docker container 
running your service. Copy the provided Dockerfile and open it. It has comments specifying what you need to change and 
briefly explaining how it works. Once you're finished editing it, open a terminal in its directory and execute

`docker build -t image_name .`

It should compile without errors (let us know in this repository's issues otherwise). You can know deploy your Docker
container with your service running inside with

`docker run -p 8061:8061 -it --rm image_name`

The flags `-it` and `--rm` indicate that the container should have an interactive terminal and should remove the Docker container from 
your machine once it terminates.

## Building full pipelines
Are you interested in building entire pipelines? Head over to 
[this repository](https://github.com/DuarteMRAlves/Pipeline-Orchestrator), and in particular, 
[this pipeline example](https://github.com/DuarteMRAlves/Pipeline-Orchestrator/blob/main/examples/ENSEMBLE.md).
