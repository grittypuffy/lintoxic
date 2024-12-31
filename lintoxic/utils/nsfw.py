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

        # Load model and processor
        self.model = AutoModelForImageClassification.from_pretrained(model_name)
        self.processor = ViTImageProcessor.from_pretrained(model_name)

    def predict(self, image_path: str):
        img = Image.open(image_path)
        
        # Prepare the image input
        inputs = self.processor(images=img, return_tensors="pt")
        
        # Forward pass through the model
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
        
        # Get the predicted label
        predicted_label = logits.argmax(-1).item()
        return predicted_label, self.model.config.id2label[predicted_label]
