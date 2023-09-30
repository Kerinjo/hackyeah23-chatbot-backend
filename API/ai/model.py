import torch
import transformers

from tqdm import tqdm
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("ai-forever/mGPT")
model = GPT2LMHeadModel.from_pretrained("ai-forever/mGPT")
model.eval()
model.cuda()

@torch.no_grad()
def generate_answer(query):
    input_ids = tokenizer.encode(query, return_tensors="pt").to(model.device)
    out = model.generate(
        input_ids,
        min_length=10,
        max_length=100,
        min_new_tokens=10,
        eos_token_id=5,
        pad_token_id=1,
        top_k=50,
        top_p=0.0,
        no_repeat_ngram_size=5
    )
    generated_text = tokenizer.decode(out[0])
    print(generated_text)
    torch.cuda.empty_cache()