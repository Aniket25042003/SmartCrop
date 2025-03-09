import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

def generate_feature_importance_plot(model, feature_names):
    # Get feature importances from the trained model
    importances = model.feature_importances_

    # Create a bar plot for feature importances
    plt.figure(figsize=(10, 6))
    plt.barh(feature_names, importances)
    plt.xlabel('Feature Importance')
    plt.ylabel('Features')
    plt.title('Feature Importance for Crop Prediction')

    # Save the plot as an image
    feature_importance_plot_filename = "static/feature_importance_plot.png"
    plt.savefig(feature_importance_plot_filename)
    plt.close()  # Close the plot to free up memory

    print(f"Feature importance plot saved to: {feature_importance_plot_filename}")
    return feature_importance_plot_filename
