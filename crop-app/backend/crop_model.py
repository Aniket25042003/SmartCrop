#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


# In[2]:


df = pd.read_csv('Crop_recommendation.csv')


# In[3]:


df.head()


# In[4]:


df = df.dropna()


# In[5]:


print(df.shape)
print(f'Total number of rows is:{df.shape[0]} and total number of columns is: {df.shape[1]}')


# In[6]:


df.info()


# In[7]:


print(df.columns)


# In[8]:


df.describe()


# In[9]:


df.duplicated().sum()


# In[10]:


df['label'].value_counts().reset_index()


# In[12]:


X = df.drop(columns=['label'])
y = df['label']


# In[13]:


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# In[14]:


X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# In[15]:


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


# In[16]:


accuracy = model.score(X_test, y_test)
print(f'Model Accuracy: {accuracy:.4f}')


# In[17]:


sample_data = pd.DataFrame({
    'N': [90],
    'P': [42],
    'K': [43],
    'temperature': [20.87974371],
    'humidity': [82.00274423],
    'ph': [6.502985292000001],
    'rainfall': [202.9355362]
})


# In[18]:


sample_data_scaled = scaler.transform(sample_data)


# In[19]:


probabilities = model.predict_proba(sample_data_scaled)


# In[20]:


top_3_indices = probabilities.argsort()[0][-3:][::-1]
top_3_crops = model.classes_[top_3_indices]


# In[21]:


print("Top 3 crop recommendations:", top_3_crops)


# In[23]:


get_ipython().system('pip install shap')


# In[38]:


import shap

# SHAP explainer for tree-based models (Random Forest)
explainer = shap.TreeExplainer(model)

# Get the SHAP values for each class (multi-class classification)
shap_values = explainer.shap_values(X_train)

# Print the shape of shap_values to debug
print(f"Type of shap_values: {type(shap_values)}")
print(f"Shape of shap_values: {shap_values.shape}")

# Choose the SHAP values for the first class (or any other class you prefer)
shap_values_class_0 = shap_values[:, :, 0]  # For the first class (index 0)

# Visualize SHAP summary plot for the first class
for i in range(shap_values.shape[2]):  # Loop through all classes
    shap_values_class_i = shap_values[:, :, i]  # SHAP values for the i-th class
    print(f"Plotting for class {i}")
    shap.summary_plot(shap_values_class_i, X_train)


# In[31]:


print(type(model))


# In[32]:


# Check the shape of shap_values and X_train
print(f"Shape of shap_values[0]: {shap_values[0].shape}")
print(f"Shape of X_train: {X_train.shape}")


# In[47]:


import shap
import numpy as np

# Step 1: Get SHAP values for the input sample
explainer = shap.TreeExplainer(model)  # Using TreeExplainer for RandomForest
shap_values = explainer.shap_values(sample_data_scaled)

# Inspect the shape (for debugging)
print("Shape of shap_values[0]:", shap_values[0].shape)  # Expected: (7, 22)
print("Shape of sample_data_scaled:", sample_data_scaled.shape)  # Expected: (1, 7)

# Step 2: Remove the extra columns (assumed to be constant offsets) to match the 7 features.
# Here, we slice the second dimension to keep only the first 7 columns.
shap_values_clean = shap_values[0][:, :7]  # Now shap_values_clean has shape (7, 7)

# Step 3: Visualize SHAP values for the first class.
shap.initjs()  # Initialize JS for visualizations (if using Jupyter)

# IMPORTANT: Instead of extracting a row as a 1D vector, extract it as a 2D matrix:
top_class_shap_values = shap_values_clean[0:1, :]  # Now shape is (1, 7)

# Visualize the SHAP values for the first class (top predicted class)
shap.summary_plot(top_class_shap_values, sample_data_scaled, feature_names=sample_data.columns)

# (Optional) Step 4: Visualize SHAP values for the top 3 recommended crops if needed.

# Check the indices for the top 3 recommended crops
print("Top 3 Indices:", top_3_indices)  # Debugging line
valid_top_3_indices = [idx for idx in top_3_indices if idx < len(top_3_crops)]

# Now, loop over the valid indices only
for idx in valid_top_3_indices:
    print(f"Explaining the recommendation for: {top_3_crops[idx]}")
    
    # Extract the SHAP values for the specific class as a 2D matrix.
    class_shap_values = np.atleast_2d(shap_values_clean[idx])
    print("Shape of class_shap_values:", class_shap_values.shape)  # Debugging line
    
    shap.summary_plot(class_shap_values, sample_data_scaled, feature_names=sample_data.columns)


# In[42]:


import shap
import numpy as np

# Step 1: Get SHAP values for the input sample
explainer = shap.TreeExplainer(model)  # Using TreeExplainer for RandomForest
shap_values = explainer.shap_values(sample_data_scaled)

# Inspect the shape of shap_values and the input data
print(f"Type of shap_values: {type(shap_values)}")
print(f"Shape of shap_values: {len(shap_values)} classes")
for i, class_shap_values in enumerate(shap_values):
    print(f"Shape of shap_values for class {i}: {class_shap_values.shape}")

# Inspect the shape of sample_data_scaled to compare
print(f"Shape of sample_data_scaled: {sample_data_scaled.shape}")


# In[48]:


import joblib

# Save the trained model
joblib.dump(model, 'crop_recommendation_model.pkl')


# In[ ]:




