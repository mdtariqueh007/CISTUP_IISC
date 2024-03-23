import React, { useState } from 'react';
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [vehicleCount, setVehicleCount] = useState(0);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
  };

  const handleImageUpload = () => {
    if (!image) {
      console.error('No image selected');
      return;
    }

    const formData = new FormData();
    formData.append('image', image);

    fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        const processedImageData = data.processedImage;
        const count = data.vehicleCount;
        setVehicleCount(count);
        if (processedImageData) {
          setProcessedImage(`data:image/jpeg;base64,${processedImageData}`);
        } else {
          console.error('No processed image data returned from the server');
        }
      })
      .catch(error => console.error('Error uploading image:', error));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Transportation Image Object Detection</h1>
      </header>
      <div className="upload-form">
        <input type="file" accept="image/*" onChange={handleImageChange} />
        <button onClick={handleImageUpload}>Upload</button>
      </div>
      <div className="image-display">
        <h2>Original Image</h2>
        {image && (
          <img src={URL.createObjectURL(image)} alt="Original" />
        )}
        <h2>Processed Image</h2>
        {processedImage && (
          <img src={processedImage} alt="Processed" />
        )}
        <h2>Vehicle Count</h2>
        {vehicleCount && (
          <h3>{vehicleCount}</h3>
        )}
      </div>
    </div>
  );
}

export default App;
