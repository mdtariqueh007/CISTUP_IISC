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
    objects_detected = []
    for r in results:
        for box in r.boxes:
            class_index = int(box.cls.item())
            if 0 <= class_index < len(classNames):
                class_name = classNames[class_index]
                confidence = round(float(box.conf.item()), 2)
                bbox = [(int(box.xyxy[0]), int(box.xyxy[1])), (int(box.xyxy[2]), int(box.xyxy[3]))]
                objects_detected.append({'class': class_name, 'confidence': confidence, 'bbox': bbox})

    # Count vehicles
    vehicle_count = sum(1 for obj in objects_detected if obj['class'] in ['car', 'truck'])

    # Annotate the image
    annotated_img = img.copy()
    for obj in objects_detected:
        class_name = obj['class']
        confidence = obj['confidence']
        bbox = obj['bbox']
        cv2.rectangle(annotated_img, bbox[0], bbox[1], (0, 255, 0), 2)
        cv2.putText(annotated_img, f"{class_name} {confidence}", bbox[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Encode the annotated image to JPEG format
    _, img_encoded = cv2.imencode('.jpg', annotated_img)
    img_bytes = img_encoded.tobytes()

    return jsonify({'objectsDetected': objects_detected, 'vehicleCount': vehicle_count, 'annotatedImage': img_bytes})

if __name__ == '__main__':
    app.run(debug=True)
