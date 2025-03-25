import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data and model
df = pd.read_csv('./engineered_wine_data.csv')
model = joblib.load('./random_forest_model.joblib')  # Adjust the filename if needed

st.title('Wine Quality Prediction Dashboard')

# Sidebar for navigation
page = st.sidebar.selectbox('Choose a page', ['Data Exploration', 'Make Prediction'])

if page == 'Data Exploration':
    st.header('Data Exploration')
    
    # Display basic statistics
    st.subheader('Basic Statistics')
    st.write(df.describe())
    
    # Correlation heatmap
    st.subheader('Correlation Heatmap')
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
    
    # Feature importance
    st.subheader('Feature Importance')
    feature_importance = pd.DataFrame({'feature': df.columns[:-1], 'importance': model.feature_importances_})
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance, ax=ax)
    st.pyplot(fig)

elif page == 'Make Prediction':
    st.header('Make a Prediction')
    
    # Create input fields for each feature
    input_data = {}
    for feature in df.columns[:-1]:
        input_data[feature] = st.slider(f'Select {feature}', float(df[feature].min()), float(df[feature].max()), float(df[feature].mean()))
    
    # Make prediction
    if st.button('Predict'):
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]
        st.success(f'The predicted wine quality is: {prediction:.2f}')

# Run the app: streamlit run app.py