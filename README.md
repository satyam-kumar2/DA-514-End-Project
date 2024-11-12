
# Image Steganography with TensorFlow

This project is an Image Steganography application that hides a secret image within a container image using Convolutional Neural Networks (CNNs) built with TensorFlow and Keras. The application encodes the secret image in a way that makes it nearly invisible within the container image, and provides functionality to decode and reveal the secret image.

## Features
- **Container and Secret Image Loading**: Load images for hiding (container) and the image to be hidden (secret).
- **Encoding and Decoding**: Use the trained model to encode and decode images.
- **Graphical User Interface**: Built with Tkinter for an intuitive and easy-to-use interface.
- **Clear Functionality**: Clear loaded images and results to start a new encoding or decoding process.

## Installation

### Prerequisites
Ensure you have Python 3.8+ installed on your system.

### Dependencies
1. Clone this repository and navigate to the project directory.
   ```bash
   git clone https://github.com/satyam-kumar2/DA-514-End-Project.git
   ```

2. Install the required dependencies with:
   ```bash
   pip install -r requirements.txt
   ```

### Additional Notes for Linux Users
If `tkinter` is not pre-installed, you can install it with:
```bash
sudo apt-get install python3-tk
```

## Usage

1. **Run the Application**
   ```bash
   python project.py
   ```

2. **Load Images**
   - **Load Container Image**: Select the base image where the secret will be hidden.
   - **Load Secret Image**: Select the image to hide.

3. **Encode Image**
   - Press **Encode** to hide the secret image within the container. The encoded image will appear in the grid.

4. **Decode Image**
   - Press **Decode** to reveal the secret image from the encoded output.

5. **Clear Images**
   - Press **Clear** to reset the display and load new images.

## File Structure
- `project.py`: Main GUI application code.
- `./model`: Contains the trained `model.keras` file used for encoding and decoding.
- `requirements.txt`: Lists the dependencies for the project.

## Custom Loss Function
This project uses a custom Mean Squared Error (MSE)-based loss function that balances:
- The similarity between the container and encoded image.
- The accuracy of the decoded image.

## Example
Load a container and secret image, click **Encode** to hide the image, and **Decode** to reveal it.

## Acknowledgments
- **TensorFlow** and **Keras** for model building and training.
- **Pillow** for image processing.
- **Tkinter** for creating a simple GUI.
- IMAGE STEGANOGRAPHY USING CNN Shourya Chambial, Dhruv Sood
