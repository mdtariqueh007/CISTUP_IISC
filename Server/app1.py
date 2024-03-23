from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import math
import numpy as np

app = Flask(__name__)
CORS(app)

model = YOLO("yolo-Weights/yolov8n.pt")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'})

    # Perform object detection
    img = cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_COLOR)
    results = model(img)

    # Convert class index to class name
    classNames = model.names

    # Prepare detected objects
    objects_detected = [{'class': classNames[int(box.cls[0])],
                         'confidence': math.ceil((box.conf[0] * 100)) / 100}
                        for r in results for box in r.boxes]

    # Count vehicles
    vehicle_count = sum(1 for obj in objects_detected if obj['class'] == 'car' or obj['class'] == 'truck')

    return jsonify({'objectsDetected': objects_detected, 'vehicleCount': vehicle_count})

if __name__ == '__main__':
    app.run(debug=True)