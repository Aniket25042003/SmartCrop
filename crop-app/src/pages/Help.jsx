import React from "react";
import "../App.css";

const Help = () => {
  return (
    <div className="container">
      <h1 className="title">Help & Support</h1>

      <div className="questionBox">
        <h2>What is Crop Recommendation?</h2>
        <p>
          Our Crop Recommendation model provides the best crops for your soil based on features like temperature, humidity, and soil type.
        </p>
      </div>

      <div className="questionBox">
        <h2>How accurate is the model?</h2>
        <p>
          The model is trained on diverse datasets, and accuracy depends on your specific data inputs and environment.
        </p>
      </div>

      <div className="questionBox">
        <h2>How does this work?</h2>
        <p>
          To generate a personalized model explanation:
          <ol>
            <li>Visit the Dashboard and enter your details.</li>
            <li>Review your top 3 recommended crops.</li>
            <li>Click on the "Model Explanation" button to understand the reasoning behind the predictions.</li>
          </ol>
        </p>
      </div>

      <div className="questionBox">
        <h2>What is Model Explanation in the Crop Recommendation system?</h2>
        <p>
          Model Explanation provides insights into how our AI model arrives at the crop recommendations, helping you understand which factors influenced the suggestions, such as soil features, climate conditions, and more.
        </p>
      </div>

      <div className="questionBox">
        <h2>How can I get a personalized explanation of the model's recommendations?</h2>
        <p>
          To get a personalized explanation, visit the Model Explanation page after receiving your crop recommendations. You can see the reasoning behind the suggestions, including key data points that contributed to the decision.
        </p>
      </div>

      <div className="faqSection">
        <div className="separator"></div>
      </div>
    </div>
  );
};

export default Help;
