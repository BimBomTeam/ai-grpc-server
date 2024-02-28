import grpc
import example_pb2
import example_pb2_grpc
from concurrent import futures

class ExampleServicer(example_pb2_grpc.ExampleServiceServicer):
    def SayHello(self, request, context):
        return example_pb2.HelloResponse(message=f"Hello, {request.name}!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleServicer(), server)
    server.add_insecure_port('localhost:50051')  # Change IP address to localhost
    server.start()
    print("Server started, listening on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
