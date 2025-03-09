// Function to fetch crop recommendations from the backend
export async function getCropRecommendations(data) {
    // Validate data before sending to the backend
    const requiredFields = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"];
    for (let field of requiredFields) {
      if (data[field] === undefined || data[field] === null || isNaN(data[field])) {
        throw new Error(`Missing or invalid data for ${field}`);
      }
    }
  
    try {
      const response = await fetch("http://127.0.0.1:5000/api/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        const errorDetails = await response.text();
        throw new Error(`API Error: ${errorDetails}`);
      }
  
      const result = await response.json();
      return result;
    } catch (error) {
      console.error("Error fetching crop recommendations:", error);
      throw error;
    }
  }    
  
// Function to fetch SHAP explanation from the backend
export async function getShapExplanation() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/shap");
        
        if (!response.ok) {
            throw new Error("Failed to fetch SHAP explanation");
        }

        return await response.json();  // Return JSON response
    } catch (error) {
        console.error("Error fetching SHAP explanation:", error);
        return null;
    }
}

// Function to fetch model explanation from the backend
export async function getModelExplanation() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/model-explanation");
        
        if (!response.ok) {
            throw new Error("Failed to fetch model explanation");
        }

        return await response.json();  // Return JSON response
    } catch (error) {
        console.error("Error fetching model explanation:", error);
        return null;
    }
}

// Function to fetch LLM explanation from the backend
export async function getLlmExplanation(imagePath, recommendedResult) {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/llm-explanation", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ imagePath, recommendedResult })
        });

        if (!response.ok) {
            throw new Error("Failed to fetch LLM explanation");
        }

        return await response.json();  // Return JSON response
    } catch (error) {
        console.error("Error fetching LLM explanation:", error);
        return null;
    }
}