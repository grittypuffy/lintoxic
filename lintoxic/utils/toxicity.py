import torch
from detoxify import Detoxify
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class ToxicContentClassifier:
    _instance = None

    @staticmethod
    def get_instance():
        if ToxicContentClassifier._instance is None:
            ToxicContentClassifier._instance = ToxicContentClassifier()
        return ToxicContentClassifier._instance

    def __init__(self):
        if ToxicContentClassifier._instance is not None:
            raise Exception("This is a singleton class, use the get_instance() method.")
        
        self.model = Detoxify("multilingual")

    @torch.no_grad()
    def predict(self, text: str):
        prediction = self.model.predict(text)
        offensive_entries = {key: value for key, value in prediction.items() if value > 0.8}
        return offensive_entries if offensive_entries else prediction


class TamilToxicContentClassifier:
    _instance = None

    @staticmethod
    def get_instance(model_name="Hate-speech-CNERG/deoffxlmr-mono-tamil"):
        if TamilToxicContentClassifier._instance is None:
            TamilToxicContentClassifier._instance = TamilToxicContentClassifier(model_name)
        return TamilToxicContentClassifier._instance

    def __init__(self, model_name):
        if TamilToxicContentClassifier._instance is not None:
            raise Exception("This is a singleton class, use the get_instance() method.")
        
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = self.model(**inputs)
        logits = outputs.logits
        return logits
