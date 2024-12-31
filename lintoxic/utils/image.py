import pytesseract
import cv2
from PIL import Image

def preprocess(image_path: str):
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding (better for images with varying light conditions)
    adaptive_thresh_img = cv2.adaptiveThreshold(
        gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Apply GaussianBlur to reduce noise (optional, but can help)
    blurred_img = cv2.GaussianBlur(thresh_img, (5, 5), 0)
    
    return blurred_img

def extract_text(image_path: str):
    # Preprocess the image
    processed_image = preprocess_image(image_path)
    
    # Use pytesseract to extract text from the preprocessed image
    text = pytesseract.image_to_string(processed_image)

    return text