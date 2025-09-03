from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
# microsoft/phi-2
# mistralai/Mistral-7B-Instruct-v0.2
model_name = "tiiuae/falcon-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map ="auto", offload_folder = "offload", torch_dtype = torch.float16)

llm = pipeline("text-generation", model = model, tokenizer = tokenizer)

def generate_answer(query, context_chunks):
    prompt = f"""
  you are a helpful assistant. Use the provided context to answer the question. If answer is not in the context, say "I don't know".
  Context:{context_chunks[0]}
  Question:{query}
  Answer:
  """

    #using opensource LLM from hugging face

    response = llm(prompt,max_new_tokens = 200, temperature = 0.7, do_sample = True)
    answer = response[0]["generated_text"]
    return answer

