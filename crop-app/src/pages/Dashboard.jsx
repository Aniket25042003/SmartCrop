import { useState } from "react";
import { Link } from "react-router-dom"; // Import Link for navigation
import { getCropRecommendations } from "../api/api"; 
import "../App.css"; // Correctly import the CSS file without assigning it to a variable

export default function Dashboard() {
  const [n, setN] = useState(""); // Nitrogen (N)
  const [p, setP] = useState(""); // Phosphorus (P)
  const [k, setK] = useState(""); // Potassium (K)
  const [temperature, setTemperature] = useState(""); // Temperature
  const [humidity, setHumidity] = useState(""); // Humidity
  const [ph, setPh] = useState(""); // pH
  const [rainfall, setRainfall] = useState(""); // Rainfall

  // New state variables for weights
  const [weightN, setWeightN] = useState(1); // Weight for Nitrogen
  const [weightP, setWeightP] = useState(1); // Weight for Phosphorus
  const [weightK, setWeightK] = useState(1); // Weight for Potassium
  const [weightTemperature, setWeightTemperature] = useState(1); // Weight for Temperature
  const [weightHumidity, setWeightHumidity] = useState(1); // Weight for Humidity
  const [weightPh, setWeightPh] = useState(1); // Weight for pH
  const [weightRainfall, setWeightRainfall] = useState(1); // Weight for Rainfall

  const [isLoading, setIsLoading] = useState(false); // For loading state
  const [recommendedCrops, setRecommendedCrops] = useState([]); // For storing crop recommendations
  const [errorMessage, setErrorMessage] = useState(""); // For error messages

  // Define thresholds
  const thresholds = {
    features: {
      N: { min: 0, max: 200 }, // Example thresholds for Nitrogen
      P: { min: 0, max: 200 }, // Example thresholds for Phosphorus
      K: { min: 0, max: 200 }, // Example thresholds for Potassium
      temperature: { min: 0, max: 50 }, // Example thresholds for Temperature
      humidity: { min: 0, max: 100 }, // Example thresholds for Humidity
      ph: { min: 0, max: 14 }, // Example thresholds for pH
      rainfall: { min: 0, max: 500 }, // Example thresholds for Rainfall
    },
    weights: {
      N: { min: 0, max: 10 }, // Example thresholds for Weight of Nitrogen
      P: { min: 0, max: 10 }, // Example thresholds for Weight of Phosphorus
      K: { min: 0, max: 10 }, // Example thresholds for Weight of Potassium
      temperature: { min: 0, max: 10 }, // Example thresholds for Weight of Temperature
      humidity: { min: 0, max: 10 }, // Example thresholds for Weight of Humidity
      ph: { min: 0, max: 10 }, // Example thresholds for Weight of pH
      rainfall: { min: 0, max: 10 }, // Example thresholds for Weight of Rainfall
    }
  };

  const fetchRecommendations = async () => {
    // Validate inputs against thresholds
    if (
      !validateInputs() ||
      !validateWeights()
    ) {
      return; // Stop execution if validation fails
    }

    // Prepare the user input data
    const data = {
      N: parseFloat(n),
      P: parseFloat(p),
      K: parseFloat(k),
      temperature: parseFloat(temperature),
      humidity: parseFloat(humidity),
      ph: parseFloat(ph),
      rainfall: parseFloat(rainfall),
      weights: { // Include weights in the data structure
        N: parseFloat(weightN),
        P: parseFloat(weightP),
        K: parseFloat(weightK),
        temperature: parseFloat(weightTemperature),
        humidity: parseFloat(weightHumidity),
        ph: parseFloat(weightPh),
        rainfall: parseFloat(weightRainfall),
      }
    };
  
    setIsLoading(true);
  
    try {
      const result = await getCropRecommendations(data); // API call
      console.log("API Response: ", result);
    
      if (result && result.top_3_crops) {
        setRecommendedCrops(result.top_3_crops); // Store the recommended crops
      } else {
        console.error("No crops data in the API response.");
      }
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  
    setIsLoading(false);
  };

  const validateInputs = () => {
    const inputs = { N: n, P: p, K: k, temperature, humidity, ph, rainfall };
    for (const key in inputs) {
      const value = parseFloat(inputs[key]);
      if (value < thresholds.features[key].min || value > thresholds.features[key].max) {
        setErrorMessage(`Invalid value for ${key}: must be between ${thresholds.features[key].min} and ${thresholds.features[key].max}.`);
        return false;
      }
    }
    setErrorMessage(""); // Clear error message if all inputs are valid
    return true;
  };

  const validateWeights = () => {
    const weights = { N: weightN, P: weightP, K: weightK, temperature: weightTemperature, humidity: weightHumidity, ph: weightPh, rainfall: weightRainfall };
    for (const key in weights) {
      const value = parseFloat(weights[key]);
      if (value < thresholds.weights[key].min || value > thresholds.weights[key].max) {
        setErrorMessage(`Invalid weight for ${key}: must be between ${thresholds.weights[key].min} and ${thresholds.weights[key].max}.`);
        return false;
      }
    }
    setErrorMessage(""); // Clear error message if all weights are valid
    return true;
  };

  // Check if all inputs are filled
  const allInputsFilled = n && p && k && temperature && humidity && ph && rainfall;

  return (
    <div className="container">
      <h1>Crop Recommendations</h1>
      
      {/* Input fields for user data */}
      <div className="inputContainer">
      <input
        className="inputSquare"
        type="number"
        placeholder="Nitrogen (N)"
        value={n}
        onChange={(e) => setN(e.target.value)}
      />
      <input
        className="weightSquare"
        type="number"
        placeholder="Weight for Nitrogen"
        value={weightN}
        onChange={(e) => setWeightN(e.target.value)}
      />
      </div>
      <div className="inputContainer">
      <input
        className="inputSquare"
        type="number"
        placeholder="Phosphorus (P)"
        value={p}
        onChange={(e) => setP(e.target.value)}
      />
      <input
        className="weightSquare"
        type="number"
        placeholder="Weight for Phosphorus"
        value={weightP}
        onChange={(e) => setWeightP(e.target.value)}
      />
      </div>
      <div className="inputContainer">
      <input
        className="inputSquare"
        type="number"
        placeholder="Potassium (K)"
        value={k}
        onChange={(e) => setK(e.target.value)}
      />
      <input
        className="weightSquare"
        type="number"
        placeholder="Weight for Potassium"
        value={weightK}
        onChange={(e) => setWeightK(e.target.value)}
      />
      </div>
      <div className="inputContainer">
      <input
        className="inputSquare"
        type="number"
        placeholder="Temperature (°C)"
        value={temperature}
        onChange={(e) => setTemperature(e.target.value)}
      />
      <input
        className="weightSquare"
        type="number"
        placeholder="Weight for Temperature"
        value={weightTemperature}
        onChange={(e) => setWeightTemperature(e.target.value)}
      />
      </div>
      <div className="inputContainer">
      <input
        className="inputSquare"
        type="number"
        placeholder="Humidity (%)"
        value={humidity}
        onChange={(e) => setHumidity(e.target.value)}
      />
      <input
        className="weightSquare"
        type="number"
        placeholder="Weight for Humidity"
        value={weightHumidity}
        onChange={(e) => setWeightHumidity(e.target.value)}
      />
      </div>
      <div className="inputContainer">
      <input
        className="inputSquare"
        type="number"
        placeholder="pH"
        value={ph}
        onChange={(e) => setPh(e.target.value)}
      />
      <input
        className="weightSquare"
        type="number"
        placeholder="Weight for pH"
        value={weightPh}
        onChange={(e) => setWeightPh(e.target.value)}
      />
      </div>
      <div className="inputContainer">
      <input
        className="inputSquare"
        type="number"
        placeholder="Rainfall (mm)"
        value={rainfall}
        onChange={(e) => setRainfall(e.target.value)}
      />
      <input
        className="weightSquare"
        type="number"
        placeholder="Weight for Rainfall"
        value={weightRainfall}
        onChange={(e) => setWeightRainfall(e.target.value)}
      />
      </div>
      
      {/* Button to fetch recommendations */}
      <button className="button" onClick={fetchRecommendations} disabled={isLoading}>
        {isLoading ? "Loading..." : "Get Recommendations"}
      </button>

      {/* Display error message if any */}
      {errorMessage && <p className="error">{errorMessage}</p>}

      {/* Display recommended crops */}
      <div className="cropList">
        {recommendedCrops.length > 0 ? (
          recommendedCrops.map((crop, index) => (
            <div key={index} className="cropCard">
              <img
                className="cropImage"
                src={`/images/${crop.name.toLowerCase()}.jpg`} 
                alt={crop.name}
                onError={(e) => (e.target.style.display = "none")} // Hide if image is missing
              />
              <h3 className="cropName">{crop.name}</h3>
              <p className="description">{crop.description || "No description available."}</p>
            </div>
          ))
        ) : (
          <p>No recommendations available.</p>
        )}
      </div>

      {/* Conditionally render the Model Explanation Button */}
      {allInputsFilled && recommendedCrops.length > 0 && (
        <div className="modelExplanationButton">
          <Link to="/explanation" state={{ crops: recommendedCrops }}>
            <button className="button">Model Explanation</button>
          </Link>
        </div>
      )}
    </div>
  );
}
