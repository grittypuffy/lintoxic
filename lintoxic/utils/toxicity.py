from transformers import AutoModelForSequenceClassification, AutoTokenizer

class TamilToxicityModel:
    _instance = None

    @staticmethod
    def get_instance(model_name="Hate-speech-CNERG/deoffxlmr-mono-tamil"):
        if ModelSingleton._instance is None:
            ModelSingleton._instance = ModelSingleton(model_name)
        return ModelSingleton._instance

    def __init__(self, model_name):
        if ModelSingleton._instance is not None:
            raise Exception("This is a singleton class, use the get_instance() method.")
        
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = self.model(**inputs)
        logits = outputs.logits
        return logits
