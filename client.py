import grpc
import ai_pb2
import ai_pb2_grpc

def run():
    # Utwórz kanał do połączenia z serwerem gRPC
    channel = grpc.insecure_channel('localhost:50051')
    
    # Utwórz klienta AI
    stub = ai_pb2_grpc.AIServiceStub(channel)
    
    # Wprowadź dane do przetworzenia przez model
    user_input = input("Wprowadź dane: ")
    
    # Wysłanie zapytania do serwera i odbiór odpowiedzi
    response = stub.GetOutput(ai_pb2.Input(text=user_input))
    
    # Wyświetlenie odpowiedzi od modelu
    print("Odpowiedź od modelu:", response.text)

if __name__ == '__main__':
    run()