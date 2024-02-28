import grpc
import example_pb2
import example_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = example_pb2_grpc.ExampleServiceStub(channel)
    response = stub.SayHello(example_pb2.HelloRequest(name="World"))
    print("Client received: " + response.message)

if __name__ == '__main__':
    run()
