import tensorflow as tf
import numpy as np
import cv2
import os

# === Load TFLite model ===
interpreter = tf.lite.Interpreter(model_path="/kaggle/input/pneumonic-detection/tflite/default/1/chest_xray_model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Get input shape
input_shape = input_details[0]['shape']
height, width = input_shape[1], input_shape[2]

# === Preprocess function ===
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    img = cv2.resize(img, (width, height))      # Resize to model input size
    img = img / 255.0                           # Normalize to [0, 1]
    img = np.expand_dims(img, axis=0).astype(np.float32)  # Add batch dimension
    return img

# === Predict function ===
def predict(image_path, class_names):
    img = preprocess_image(image_path)
    
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    predicted_class = np.argmax(output_data)
    confidence = np.max(output_data)
    
    print(f"Prediction: {class_names[predicted_class]} (Confidence: {confidence:.2f})")

# === Define class names ===
# Example: If you trained for Normal vs Pneumonia
class_names = ["Normal", "Pneumonia"]

# === Test the model on a sample image ===
image_path = "/kaggle/input/pneumonia-xray-images/train/opacity/person1002_bacteria_2933.jpeg"   # Change this to your test image
predict(image_path, class_names)
