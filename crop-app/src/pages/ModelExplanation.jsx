import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { getLlmExplanation } from "../api/api"; // Import API function
import "../App.css"; // Correctly import the CSS file without assigning it to a variable

export default function ModelExplanation() {
  const location = useLocation();
  const crops = location.state?.crops || []; // Get crops from state

  const [explanation, setExplanation] = useState(""); // Explanation state
  const [isLoading, setIsLoading] = useState(false); // Loading state
  const [error, setError] = useState(""); // Error state

  useEffect(() => {
    if (crops.length > 0) {
      setIsLoading(true);
      async function fetchExplanation() {
        try {
          // Create a string of recommended crops for the explanation
          const recommendedResult = crops.map(crop => `${crop.name}: ${crop.description}`).join("\n");

          // Use a valid image path for the SHAP plot
          const imagePath = "static/feature_importance_plot.png"; // Adjust this path as necessary

          // Call the backend API for LLM explanation
          const explanationData = await getLlmExplanation(imagePath, recommendedResult);
          setExplanation(explanationData.explanation); // Assuming explanation is returned
        } catch (error) {
          console.error("Error fetching explanation:", error);
          setError("Failed to load explanation. Please try again later.");
        }
        setIsLoading(false);
      }

      fetchExplanation();
    }
  }, [crops]);

  // Function to format the explanation text for display
  const formatExplanation = (text) => {
    return text.split('\n').map((line, index) => (
      <p key={index}>{line}</p>
    ));
  };

  return (
    <div className="container">
      <h1>Model Explanation</h1>

      {crops.length > 0 ? (
        <div className="explanationBox">
          {isLoading ? (
            <>Loading Explanation...</>
          ) : error ? (
            <>{error}</>
          ) : explanation ? (
            <p className="explanationText">{explanation}</p>
          ) : (
            <>No explanation available at the moment.</>
          )}
        </div>
      ) : (
        <div className="questionBox">
          <p className="content">
            This page provides an explanation of how our AI model recommends crops based on your input data.
            <br />
            <br />
            To generate a personalized model explanation:
            <ol>
              <li>Visit the Dashboard and enter your details.</li>
              <li>Review your top 3 recommended crops.</li>
              <li>Click on the "Model Explanation" button to understand the reasoning behind the predictions.</li>
            </ol>
          </p>
        </div>
      )}
    </div>
  );
}
