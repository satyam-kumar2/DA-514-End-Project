import tkinter as tk
from tkinter import filedialog, Label, Button, Frame
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.models import load_model
import tensorflow as tf

# Custom loss function registration
mse_loss = MeanSquaredError()

@tf.keras.utils.register_keras_serializable()
def custom_loss(y_true, y_pred):
    encoded_loss = mse_loss(y_true[0], y_pred[0])
    decoded_loss = mse_loss(y_true[1], y_pred[1])
    return encoded_loss + 10 * decoded_loss

# Load the pre-trained model
model = load_model('model/model.keras', custom_objects={"custom_loss": custom_loss})

# Initialize the GUI application
root = tk.Tk()
root.title("Image encryption")
root.geometry("1200x800")

# Define variables for images
container_img = None
secret_img = None
encoded_img = None
decoded_img = None
image_labels = []

# Function to load an image as either container or secret
def load_image(image_type):
    global container_img, secret_img
    filepath = filedialog.askopenfilename()
    if filepath:
        img = Image.open(filepath).convert("RGB")  # Ensure 3 channels
        img = img.resize((64, 64))  # Resize to match model input size if needed
        if image_type == "container":
            container_img = img
            display_image(img.resize((256,256)), "Container Image", 0, 0)
        elif image_type == "secret":
            secret_img = img
            display_image(img.resize((256,256)), "Secret Image", 0, 1)

# Function to encode the secret image into the container image
def encode_image():
    global container_img, secret_img, encoded_img, decoded_img
    if container_img and secret_img:
        # Convert images to arrays and normalize to [0, 1]
        container_array = np.array(container_img) / 255.0
        secret_array = np.array(secret_img) / 255.0

        # Expand dimensions to match model input shape (1, 64, 64, 3)
        container_array = container_array[np.newaxis, ...]
        secret_array = secret_array[np.newaxis, ...]

        # Perform encoding using the model
        encoded_array, decoded_array = model.predict([container_array, secret_array])
        
        # Remove the batch dimension to match (64, 64, 3)
        encoded_array = np.squeeze(encoded_array, axis=0)
        decoded_array = np.squeeze(decoded_array, axis=0)

        weights = np.array([0.2989, 0.5870, 0.1140])
        grayscale_image = np.dot(decoded_array[...,:3], weights)
        decoded_array = (decoded_array > 0.5).astype(np.float32)  # Convert to binary
        # Convert encoded output back to image
        encoded_img = Image.fromarray((encoded_array * 255).astype(np.uint8)).resize((256,256))
        decoded_img = Image.fromarray((decoded_array * 255).astype(np.uint8)).resize((256,256))
        display_image(encoded_img, "Encoded Image", 1, 0)

# Function to decode the secret image from the encoded image
def decode_image():
    if encoded_img:
        
        display_image(decoded_img, "Decoded Image", 1, 1)

# Function to display an image in the GUI
def display_image(img, title, row, col):
    img = ImageTk.PhotoImage(img)
    img_frame = tk.Frame(image_container, bg="#ecf0f1", bd=2, relief="groove")
    img_frame.grid(row=row, column=col, padx=10, pady=10)  # Use grid layout for 2x2 arrangement
    
    img_label = Label(img_frame, image=img, text=title, compound="top", bg="#ecf0f1")
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.pack()

def clear_images():
    for widget in image_container.winfo_children():
        widget.destroy()
        image_labels = []

image_container = Frame(root, bg="#2c3e50")
image_container.pack(pady=20)

# Buttons to load images and run encode/decode operations
button_frame = Frame(root, bg="#2c3e50")
button_frame.pack(side="bottom", pady=20)
button_style = {"font": ("Arial", 12), "bg": "#2980b9", "fg": "white", "bd": 4, "relief": "raised", "width": 18, "height": 2}

load_container_button = Button(button_frame, text="Load Container Image", command=lambda: load_image("container"), **button_style)
load_container_button.grid(row=0, column=0, padx=10, pady=10)

load_secret_button = Button(button_frame, text="Load Secret Image", command=lambda: load_image("secret"), **button_style)
load_secret_button.grid(row=0, column=1, padx=10, pady=10)

encode_button = Button(button_frame, text="Encode", command=encode_image, **button_style)
encode_button.grid(row=0, column=2, padx=10, pady=10)

decode_button = Button(button_frame, text="Decode", command=decode_image, **button_style)
decode_button.grid(row=0, column=3, padx=10, pady=10)

clear_button = Button(button_frame, text="Clear", command=clear_images, **button_style)
clear_button.grid(row=0, column=4, padx=10, pady=10)

# Start the GUI loop
root.mainloop()
