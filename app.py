from flask import Flask, request, render_template, send_from_directory
import cv2
import os
import shutil
import atexit

from utils.models import *
from utils.preprocess import *
from utils.dict import *
from utils.load_model import *
from utils.inference import *
from utils.translate import *

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    model = request.form.get('model')
    checkpoint = request.form.get('checkpoint')
    color_channel = request.form.get('color_channel')
    model_dir = f"models/{model}/{color_channel}"

    num_of_characters, char_dict = get_dict(model_dir)
    ocr_model = load_model_weights(model_dir, checkpoint, color_channel, num_of_characters)

    if file.filename == '':
        return 'No selected file', 400

    if not model or not color_channel:
        return 'Model or processing type not selected', 400

    if file:
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Read the image file into a numpy array
        image = cv2.imread(file_path)
        
        # Perform processing based on selected color channel type
        if color_channel == 'gray':
            image_arr = preprocess_for_gray_channel(image)
        else:
            image_arr = preprocess_for_rgb_channel(image)
        
        # perform prediction
        ocr_output = predict(ocr_model, image_arr, char_dict)

        # if ranana then further translate to english and nepali
        if model == 'ranjana':
            nepali_output = get_translation(ocr_output, source_lang='new', target_lang='ne')
            english_output = get_translation(ocr_output, source_lang='new', target_lang='en')
            return render_template('ocr_and_translate.html', filename=file.filename, ocr_output=ocr_output, nepali_output=nepali_output, english_output=english_output, model_name = model)
        else:
            return render_template('ocr.html', filename=file.filename, ocr_output=ocr_output, model_name = model)
        
    return 'File upload failed', 500

def cleanup_upload_folder():
    """Remove the uploads directory and its contents."""
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
        print(f"Removed the directory: {UPLOAD_FOLDER}")

atexit.register(cleanup_upload_folder)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
