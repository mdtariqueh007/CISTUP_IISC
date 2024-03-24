from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import math
import numpy as np
from PIL import Image
import base64

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
    img_arr = np.array(img)
    results = model(img)
    # res_plotted = results[0].plot()

    # cv2.imshow("result",res_plotted)

    # Convert class index to class name
    classNames = model.names

    # Prepare detected objects
    objects_detected = [{'class': classNames[int(box.cls[0])],
                         'confidence': math.ceil((box.conf[0] * 100)) / 100}
                        for r in results for box in r.boxes]
    
    cnt = 0

    for r in results:
        for box in r.boxes:
            if classNames[int(box.cls[0])] in ["car","truck","bus","motorcycle"]:
                cnt += 1
            coor = box.xywh[0]
            # print(coor)
            x = int(coor[0])
            y = int(coor[1])
            w = int(coor[2])
            h = int(coor[3])
            cv2.rectangle(img_arr,(int(x-w/2),int(y+h/2)),(int(x+ w/2),int(y-h/2)),(0,0,255),2)
            cv2.putText(img_arr,str(str(classNames[int(box.cls[0])])+" "+str(math.ceil((box.conf[0] * 100)) / 100)),(int(x-w/2),int(y-h/2)),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,0),2,cv2.LINE_AA)

    # Count vehicles
    # vehicle_count = sum(1 for obj in objects_detected if obj['class'] == 'car' or obj['class'] == 'truck')
    

    processed_img = Image.fromarray(img_arr)
    processed_img = img_arr
    _, encoded_img = cv2.imencode('.jpg', processed_img)
    processed_img_base64 = base64.b64encode(encoded_img).decode('utf-8')
    return jsonify({'objectsDetected': objects_detected, 'vehicleCount': cnt, 'annotatedImage':processed_img_base64})

if __name__ == '__main__':
    app.run(debug=True)