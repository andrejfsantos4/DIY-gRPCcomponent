# This Dockerfile template most likely contains everything you'll need. The changes you need to make (mostly adjusting
# file names) are labelled with a TODO.

# Define work directory folder inside the docker container for all stages
# Must be renewed in the beggining of each stage
ARG WORKSPACE=/workspace

# --------------------------------------
# Builder stage to generate .proto files
# This prevents having to install protobuf and gRPC on the final docker image
# Only one change is necessary here
# --------------------------------------

FROM python:3.8.7-slim-buster as builder
# Renew build args
ARG WORKSPACE

# Path for the protos folder to copy
ARG PROTOS_FOLDER_DIR=protos

RUN pip install --upgrade pip && \
    pip install grpcio==1.35.0 grpcio-tools==1.35.0 protobuf==3.14.0

COPY ${PROTOS_FOLDER_DIR} ${WORKSPACE}/
WORKDIR ${WORKSPACE}

# Compile proto file and remove it since it will no longer be necessary TODO: adjust the filename
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. your_proto.proto


# -----------------------------
# Stage to generate final image. This will generate your final docker image
# -----------------------------

# TODO: You may need to change the starting Docker image to fit your needs (eg, if you need PyTorch, then you should start
# from an image that already has it)
FROM python:3.8.7-slim-buster
# Renew build args
ARG WORKSPACE

ARG USER=runner
ARG GROUP=runner-group

# Create non-privileged user and workspace
RUN addgroup --system ${GROUP} && \
    adduser --system --no-create-home --ingroup ${GROUP} ${USER} && \
    mkdir ${WORKSPACE} && \
    chown -R ${USER}:${GROUP} ${WORKSPACE}

# Install requirements
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

# COPY .proto file to root to meet ai4eu specifications TODO: adjust the filename
COPY --from=builder --chown=${USER}:${GROUP} ${WORKSPACE}/your_proto.proto /

# Copy generated .py files to workspace
COPY --from=builder --chown=${USER}:${GROUP} ${WORKSPACE}/*.py ${WORKSPACE}/

# Copy necessary files to workspace TODO: adjust the filenames
COPY --chown=${USER}:${GROUP} you_server.py ${WORKSPACE}/your_server.py
# TODO: Add copies of this line for each file you need.
# The syntax is COPY --chown=${USER}:${GROUP} file_name_in_your_machine.py ${WORKSPACE}/file_name_in_docker.py
# For instance, if you use parsing.py:
COPY --chown=${USER}:${GROUP} parsing.py ${WORKSPACE}/parsing.py

# Change to non-privileged user
USER ${USER}

# Expose port 8061 according to ai4eu specifications
EXPOSE 8061

WORKDIR ${WORKSPACE}

# This command will be executed when launching your Docker container TODO: adjust the filename
CMD ["python", "your_server.py"]
