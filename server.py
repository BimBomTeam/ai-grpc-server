from concurrent import futures
import grpc
import ai_pb2
import ai_pb2_grpc
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class AIServicer(ai_pb2_grpc.AIServiceServicer):
    def __init__(self):
        # Ustawienie domyślnego urządzenia na CUDA
        torch.cuda.set_device(0)
        # Inicjalizacja modelu i tokenizatora
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype=torch.float32, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)

    def GetOutput(self, request, context):
        user_input = request.text
        
        # Tokenizacja tekstu na serwerze
        tokens = self.tokenizer.encode(user_input, return_tensors='pt').squeeze().tolist()
        
        # Przekazanie tokenów do modelu i generacja odpowiedzi
        response = self.generate_response(tokens)
        
        return ai_pb2.Output(text=response)

    def generate_response(self, tokens):
        # Generowanie odpowiedzi na podstawie tokenów
        model_inputs = {"input_ids": torch.tensor([tokens])}
        outputs = self.model.generate(**model_inputs, max_length=200)
        
        # Dekodowanie wygenerowanych odpowiedzi
        text = self.tokenizer.batch_decode(outputs)[0]
        return text

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ai_pb2_grpc.add_AIServiceServicer_to_server(AIServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()