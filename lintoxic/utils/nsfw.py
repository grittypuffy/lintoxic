from typing import Optional
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor

class NSFWImageClassificationModel:
    _instance = None

    @staticmethod
    def get_instance(model_name: str ="Falconsai/nsfw_image_detection"):
        if NSFWImageClassificationModel._instance is None:
            NSFWImageClassificationModel._instance = NSFWImageClassificationModel(model_name)
        return NSFWImageClassificationModel._instance

    def __init__(self, model_name: str):
        if NSFWImageClassificationModel._instance is not None:
            raise Exception("This is a singleton class, use the get_instance() method.")

        self.model = AutoModelForImageClassification.from_pretrained(model_name)
        self.processor = ViTImageProcessor.from_pretrained(model_name)

    def predict(self, *, image_path: Optional[str] = None, image_content: Optional[Image] = None):
        img = Image.open(image_path) if image_path else image_content
        inputs = self.processor(images=img, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
        
        predicted_label = logits.argmax(-1).item()
        return predicted_label, self.model.config.id2label[predicted_label]
