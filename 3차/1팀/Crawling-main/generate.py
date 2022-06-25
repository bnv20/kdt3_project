from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch


class Generate:
    def __init__(self, model_url):
        self.model = torch.load(model_url+'/model.pt')
        self.tokenizer = T5Tokenizer.from_pretrained(model_url)
        self.device = device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(device)

    def generate_text(self, text):
        with torch.no_grad():
            text = 'summarize :'+text
            ids = self.tokenizer.encode(text, return_tensors='pt').to(self.device,dtype=torch.long)
            
            generate = self.model.generate(
                    input_ids = ids,
                    max_length=150, 
                    num_beams=2,
                    repetition_penalty=2.5, 
                    length_penalty=1.0, 
                    early_stopping=True)
            gen = self.tokenizer.decode(generate[0],skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return gen 

    def input_generate(self, df, column):
        dataframe = df.copy()
        dataframe['generate_text'] = dataframe['document'].apply(lambda x: self.generate_text(x))
        return dataframe
