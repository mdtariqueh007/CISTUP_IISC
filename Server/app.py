from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'})

    if file:
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Example processing
        _, encoded_img = cv2.imencode('.jpg', processed_img)
        processed_img_base64 = base64.b64encode(encoded_img).decode('utf-8')
        return jsonify({'processedImage': processed_img_base64})

if __name__ == '__main__':
    app.run(debug=True)
