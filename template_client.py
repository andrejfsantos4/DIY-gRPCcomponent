"""
You'll only need this client to test your server. Other than that it won't be necessary since in practice your server
will be deployed in a pipeline.
"""

# Required imports
import grpc
import your_service_name_pb2
import your_service_name_pb2_grpc

# Optional but useful imports
import parsing
import logging


# You'll need the following code, just change the service name
if __name__ == '__main__':
    with grpc.insecure_channel('localhost:8061') as channel:
        estimator_stub = your_service_name_pb2_grpc.YourServiceStub(channel)
        try:
            # Send a request to your server and receive the response
            response = estimator_stub.YourMethodName(your_service_name_pb2.InputMessage(some_number=3.14159))
            # Check if the response is what you expected
            print("The server said ", response.what_is_true)
        except grpc.RpcError as rpc_error:  # Print the errors if they occur
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')