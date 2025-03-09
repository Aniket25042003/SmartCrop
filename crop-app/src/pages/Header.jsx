// src/components/Header.jsx
import React from "react";
import { Link } from "react-router-dom";
import "../App.css"; // Ensure this import is correct

const Header = () => {
  return (
    <header className="header">
      <nav className="nav">
        <ul>
          <li>
            <Link to="/">AI Crop Recommendation</Link>
          </li>
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li>
            <Link to="/explanation">Model Explanation</Link>
          </li>
          <li>
            <Link to="/help">Help</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
