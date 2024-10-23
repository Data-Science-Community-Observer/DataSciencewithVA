import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image

# Load the data and model
df = pd.read_csv('engineered_wine_data.csv')
model = joblib.load('random_forest_model.joblib')  # Adjust the filename if needed

# Set page config for a wider layout
st.set_page_config(layout="wide", page_title="Wine Quality Predictor")


# Custom CSS for anime-inspired styling
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(to right, #FF9A8B, #FF6A88, #FF99AC);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #3A1C71, #D76D77, #FFAF7B);
    }
    h1, h2, h3 {
        color: #3A1C71;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #FF6A88;
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title('🍷 Wine Quality Prediction Adventure 🍷')

# Sidebar for navigation
page = st.sidebar.selectbox('Choose your path', ['Data Exploration', 'Predict Wine Quality'])

# Wine quality categories explanation
quality_categories = {
    0: "Undrinkable",
    1: "Poor",
    2: "Mediocre",
    3: "Below Average",
    4: "Average",
    5: "Above Average",
    6: "Good",
    7: "Very Good",
    8: "Excellent",
    9: "Outstanding"
}

if page == 'Data Exploration':
    st.header('🔍 Magical Data Exploration')
    
    # Display basic statistics with a colorful table
    st.subheader('✨ Mystical Wine Statistics')
    stats_df = df.describe().round(2)
    st.dataframe(stats_df.style.background_gradient(cmap='YlOrRd'))
    
    # # Interactive correlation heatmap using plotly
    # st.subheader('🌈 Correlation Wonderland')
    # corr = df.corr()
    # fig = px.imshow(corr, color_continuous_scale='Viridis')
    # fig.update_layout(title='Interactive Correlation Heatmap')
    # st.plotly_chart(fig)
    
    # Feature importance with colorful bar chart
    st.subheader('🏆 Feature Importance Tournament')
    feature_importance = pd.DataFrame({'feature': df.columns[:-1], 'importance': model.feature_importances_})
    feature_importance = feature_importance.sort_values('importance', ascending=False)
    fig = px.bar(feature_importance, x='importance', y='feature', orientation='h',
                 color='importance', color_continuous_scale='Reds')
    fig.update_layout(title='Feature Importance Ranking')
    st.plotly_chart(fig)
    
    # Wine quality distribution
    st.subheader('🍇 Wine Quality Distribution')
    quality_counts = df['quality'].value_counts().sort_index()
    fig = px.bar(x=quality_counts.index, y=quality_counts.values, 
                 labels={'x': 'Quality', 'y': 'Count'},
                 color=quality_counts.index, color_continuous_scale='Viridis')
    fig.update_layout(title='Wine Quality Distribution')
    st.plotly_chart(fig)
    
    # Display quality categories
    st.subheader('🏅 Wine Quality Categories')
    for quality, description in quality_categories.items():
        st.markdown(f"**{quality}**: {description}")

elif page == 'Predict Wine Quality':
    st.header('🔮 Predict Your Wine\'s Magical Quality')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Enter Your Wine\'s Characteristics')
        input_data = {}
        for feature in df.columns[:-1]:
            input_data[feature] = st.slider(f'Select {feature}', 
                                            float(df[feature].min()), 
                                            float(df[feature].max()), 
                                            float(df[feature].mean()))
    
    with col2:
        st.subheader('Your Wine\'s Magical Properties')
        fig = px.line_polar(r=[input_data[feat] for feat in df.columns[:-1]], 
                            theta=df.columns[:-1], line_close=True)
        fig.update_traces(fill='toself')
        st.plotly_chart(fig)
    
    if st.button('🪄 Reveal Wine Quality'):
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]
        quality_category = quality_categories[round(prediction)]
        
        st.success(f'Your wine\'s predicted quality is: {prediction:.2f}')
        st.markdown(f"**Category**: {quality_category}")
        
        # Visual representation of the prediction
        fig = px.bar(x=['Prediction'], y=[prediction], 
                     color=['Prediction'], color_continuous_scale='RdYlGn',
                     range_y=[0, 10])
        fig.update_layout(title='Predicted Wine Quality')
        st.plotly_chart(fig)

# Run the app: streamlit run anime_wine_dashboard.py