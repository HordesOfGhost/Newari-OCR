from flask import Flask, request, render_template
import cv2
import numpy as np
import os
from utils.models import *
from utils.preprocess import *
from utils.get_dict import *
from utils.load_model import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400

    # Get information from form

    file = request.files['file']
    model = request.form.get('model')
    checkpoint = request.form.get('checkpoint')
    color_channel = request.form.get('color_channel')
    model_dir = f"models/{model}/{color_channel}"

    # Get models and required files
    num_of_characters = get_dict(model_dir)
    ocr_model = load_model_weights(model_dir, checkpoint, color_channel, num_of_characters)

    if file.filename == '':
        return 'No selected file', 400

    if not model or not color_channel:
        return 'Model or processing type not selected', 400

    if file:
        # Read the image file into a numpy array
        file_stream = file.read()
        np_arr = np.frombuffer(file_stream, np.uint8)
        
        # Decode the numpy array to an image
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # Perform processing based on selected color channel type
        if color_channel == 'gray':
            image = preprocess_for_gray_channel(image)
        else:
            image = preprocess_for_rgb_channel(image)
        
        
        # Save the processed image
        output_file_path = f'uploads/{model}_{color_channel}_{file.filename}'
        cv2.imwrite(output_file_path, image)

        return f'File uploaded and processed successfully: {file.filename}'

    return 'File upload failed', 500

if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    app.run(debug=True)
