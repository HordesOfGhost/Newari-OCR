from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
from utils.models import *
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Open the image file
        image = Image.open(io.BytesIO(file.read()))
        # Perform OCR on the image
        text = pytesseract.image_to_string(image)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
