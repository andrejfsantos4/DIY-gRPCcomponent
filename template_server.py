# NOTE: Throughout the file the places where you need to make changes are labeled with a TODO.

# Mandatory imports
from concurrent import futures
import grpc
import grpc_reflection.v1alpha.reflection as grpc_reflection
# TODO: change the files names (make sure to change these names in the entire file, not just in these two lines)
import your_service_name_pb2
import your_service_name_pb2_grpc

# Optional but useful imports
import parsing  # For parsing protobuf messages to and from Python data structures
import logging  # For printing information about execution (warnings, errors, etc). See
                # https://docs.python.org/3/howto/logging.html for more info on this


  # TODO: Choose a name for your server class and replace "YourServerClassName". Also replace "YourServicer" with the correct class name
class YourServerClassName(your_service_name_pb2_grpc.YourServicer):
    """Provides methods that implement functionality of your server."""

    # TODO: Replace "YourMethodName" with the method name you defined in your proto
    def YourMethodName(self, request, context):
        """
        Implement your component funcionality here.
        :param request: the input message that your server just received.
        :param context: you can ignore this TODO: check this
        """
        # You can perform some verifications:
        # logging.info("Executing YourMethodName...")
        # if not request or request.some_number == 0:
        #     logging.error("Received empty request.")
        #     return your_service_name_pb2.OutputMessage()  # Simply returns an empty message

        # Your code here
        # ...
        # return your_service_name_pb2.OutputMessage(what_is_true=True)


# The following code is required. Most likely you'll only need to change the service name to match your service name
def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    # TODO: Change "YourServicer" in the method name to the correct name. Also change "YourServerClassName" to the class name you choose earlier
    your_service_name_pb2_grpc.add_YourServicer_to_server(
        YourServerClassName(), server)

    # Add reflection. Is required so that the pipeline orchestrator knows what method to invoke
    service_names = (
        your_service_name_pb2.DESCRIPTOR.services_by_name['YourServiceName'].full_name,  # TODO: change "YourServiceName"
        grpc_reflection.SERVICE_NAME
    )
    grpc_reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port('[::]:8061')  # Port 8061 is used to match AI4Europe specs and ensure compatibility
    server.start()
    logging.info("Successfully started and waiting for connections..")
    server.wait_for_termination()


if __name__ == '__main__':
    # Configure the following line according to the level of messages you want displayed on the terminal
    # This displays all messages
    logging.basicConfig(format='Server %(levelname)s: %(message)s', level=logging.INFO)
    # This displays only warnings or higher
    # logging.basicConfig(format='Server %(levelname)s: %(message)s', level=logging.WARNING)
    serve()
