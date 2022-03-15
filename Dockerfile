# Define workdir folder for all stages
# Must be renewed in the beggining of each stage
ARG WORKSPACE=/workspace

# --------------------------------------
# Builder stage to generate .proto files.
# This prevents having to install protobuf and gRPC on the final docker image
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

# Compile proto file and remove it since it will no longer be necessary
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. traffic_routing.proto


# -----------------------------
# Stage to generate final image
# -----------------------------

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
    # Install headless version of opencv-python for server usage
    # Does not install graphical modules
    # See https://github.com/opencv/opencv-python#installation-and-usage
    pip install -r requirements.txt && \
    rm requirements.txt

# COPY .proto file to root to meet ai4eu specifications
COPY --from=builder --chown=${USER}:${GROUP} ${WORKSPACE}/traffic_routing.proto /

# Copy generated .py files to workspace
COPY --from=builder --chown=${USER}:${GROUP} ${WORKSPACE}/*.py ${WORKSPACE}/

# Copy files to workspace
COPY --chown=${USER}:${GROUP} parsing.py ${WORKSPACE}/parsing.py
COPY --chown=${USER}:${GROUP} traffic_routing_server.py ${WORKSPACE}/traffic_routing_server.py

# Change to non-privileged user
USER ${USER}

# Expose port 8061 according to ai4eu specifications
EXPOSE 8061

WORKDIR ${WORKSPACE}

CMD ["python", "traffic_routing_server.py"]
