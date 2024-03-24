import React, { useState } from 'react';
import './App.css';
import logo from "./eye_logo.jpg";

function App() {
  const [image, setImage] = useState(null);
  const [objectsDetected, setObjectsDetected] = useState([]);
  const [vehicleCount, setVehicleCount] = useState(0);
  const [carCount, setCarCount] = useState(0);
  const [busCount, setBusCount] = useState(0);
  const [truckCount, setTruckCount] = useState(0);
  const [motorcycleCount, setMotorCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [processedImage, setProcessedImage] = useState(null);
  const [error, setError] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setProcessedImage(null); // Reset processed image when a new image is selected
  };

  const handleImageUpload = () => {
    if (!image) {
      setError('Please select an image.');
      return;
    }

    setIsLoading(true);
    setError(null); // Reset error message

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
        const car = data.carCount || 0;
        const bus = data.busCount || 0;
        const truck = data.truckCount || 0;
        const motorcycle = data.motorcycleCount || 0;
        setObjectsDetected(detectedObjects);
        setVehicleCount(count);
        setCarCount(car);
        setBusCount(bus);
        setTruckCount(truck);
        setMotorCount(motorcycle);
        const processedImageData = data.annotatedImage;
        if(processedImageData){
          setProcessedImage(`data:image/jpeg;base64,${processedImageData}`);
        }else{
          setProcessedImage(null);
          setError('No processed image data returned from the server.');
        }
      })
      .catch(error => setError('Error uploading image: ' + error.message))
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
          {error && <p className="error-message">{error}</p>}
        </div>
        <div className="image-display">
          <h2>Original Image</h2>
          {image && (
            <img className="image" src={URL.createObjectURL(image)} alt="Original" />
          )}
          <h2>Processed Image</h2>
          {processedImage && (
            <img className="image" src={processedImage} alt="Processed" />
          )}
        </div>
        <h2>Vehicle Count: {vehicleCount}</h2>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <h2 style={{ marginRight: '20px' }}>Car Count: {carCount}</h2>
          <h2 style={{ marginRight: '20px' }}>Bus Count: {busCount}</h2>
          <h2 style={{ marginRight: '20px' }}>Truck Count: {truckCount}</h2>
          <h2>Motorcycle Count: {motorcycleCount}</h2>
        </div>
        <div className="detection-results">
          <h2>Detected Objects</h2>
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
      </div>
      <footer className="footer">
        <p>Md Tarique Hussain @ 2024</p>
      </footer>
    </div>
  );
}

export default App;
