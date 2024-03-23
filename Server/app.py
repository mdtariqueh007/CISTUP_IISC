from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
# from vehicle_detector import VehicleDetector
from PIL import Image
import requests

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
        # img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        img = Image.open(file)
        # processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Example processing
        img = img.resize((450,250))
        img_arr = np.array(img)
        grey = cv2.cvtColor(img_arr,cv2.COLOR_BGR2GRAY)
        Image.fromarray(grey)
        blur = cv2.GaussianBlur(grey,(5,5),0)
        Image.fromarray(blur)
        dilated = cv2.dilate(blur,np.ones((3,3)))
        Image.fromarray(dilated)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
        Image.fromarray(closing)
        car_cascade_src = 'C:/Users/mdtar/Downloads/cars.xml'
        car_cascade = cv2.CascadeClassifier(car_cascade_src)
        cars = car_cascade.detectMultiScale(closing, 1.1, 1)
        cnt = 0
        for (x,y,w,h) in cars:
            cv2.rectangle(img_arr,(x,y),(x+w,y+h),(0,0,255),2)
            cnt += 1
        # print(cnt, " cars found")
        processed_img = Image.fromarray(img_arr)
        processed_img = img_arr
        _, encoded_img = cv2.imencode('.jpg', processed_img)
        processed_img_base64 = base64.b64encode(encoded_img).decode('utf-8')
        return jsonify({'processedImage': processed_img_base64, 'vehicleCount':cnt})

if __name__ == '__main__':
    app.run(debug=True)
