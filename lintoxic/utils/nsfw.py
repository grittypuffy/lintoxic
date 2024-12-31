import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor

class NSFWImageClassificationModel:
    _instance = None

    @staticmethod
    def get_instance(model_name="Falconsai/nsfw_image_detection"):
        if ImageClassificationModel._instance is None:
            ImageClassificationModel._instance = ImageClassificationModel(model_name)
        return ImageClassificationModel._instance

    def __init__(self, model_name):
        if ImageClassificationModel._instance is not None:
            raise Exception("This is a singleton class, use the get_instance() method.")

        # Load model and processor
        self.model = AutoModelForImageClassification.from_pretrained(model_name)
        self.processor = ViTImageProcessor.from_pretrained(model_name)

    def predict(self, image_path):
        # Open the image
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
