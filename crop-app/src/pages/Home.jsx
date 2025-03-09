import { useNavigate } from "react-router-dom";
import "../App.css";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <h1 className="title">AI-Powered Crop Recommendation</h1>
      <p className="subtitle">
        Get the best crops based on soil and weather conditions.
      </p>
      <button className="button" onClick={() => navigate("/dashboard")}>
        Get Started
      </button>
    </div>
  );
}
