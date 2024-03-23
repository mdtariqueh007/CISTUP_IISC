import React, { useState } from 'react';
import './App.css';
import logo from "./iisc.png";

function App() {
  const [image, setImage] = useState(null);
  const [objectsDetected, setObjectsDetected] = useState([]);
  const [vehicleCount, setVehicleCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [annotatedImage, setAnnotatedImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
  };

  const handleImageUpload = () => {
    if (!image) {
      console.error('No image selected');
      return;
    }

    setIsLoading(true);

    const formData = new FormData();
    formData.append('image', image);

    fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        const detectedObjects = data.objectsDetected || [];
        const count = data.vehicleCount || 0;
        setObjectsDetected(detectedObjects);
        setVehicleCount(count);
        // Load annotated image if available
        if (data.annotatedImage) {
          setAnnotatedImage(URL.createObjectURL(new Blob([data.annotatedImage], { type: 'image/jpeg' })));
        }
      })
      .catch(error => console.error('Error uploading image:', error))
      .finally(() => setIsLoading(false));
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="logo-container">
          <img src={logo} alt="Logo" className="logo" />
          <h1>Transportation Image Object Detection</h1>
        </div>
        
      </header>
      <div className="content">
        <div className="upload-form">
          <input type="file" accept="image/*" onChange={handleImageChange} />
          <button className="button" onClick={handleImageUpload} disabled={isLoading}>
            {isLoading ? 'Processing...' : 'Upload'}
          </button>
        </div>
        <div className="image-display">
          <h2>Original Image</h2>
          {image && (
            <img className="image" src={URL.createObjectURL(image)} alt="Original" />
          )}
        </div>
        <h2>Vehicle Count: {vehicleCount}</h2>
        <div className="detection-results">
          <h2>YOLO v8 Detected Objects</h2>
          {objectsDetected.length > 0 ? (
            <ul>
            {objectsDetected.map((obj, index) => (
              <div key={index} className="object-card">
                <div className="object-info">
                  <h3>{obj.class}</h3>
                  <p>Confidence: {obj.confidence}</p>
                </div>
              </div>
            ))}
            </ul>
          ) : (
            <p>No objects detected.</p>
          )}
        </div>
        <div className="annotated-image">
          {annotatedImage && (
            <div>
              <h2>Annotated Image</h2>
              <img className="image" src={annotatedImage} alt="Annotated" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
