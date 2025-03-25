import streamlit as st
import requests
import base64

API_URL = "http://localhost:8000"

st.title("AI Virtual Assistant for Data Analysis & Prediction")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    response = requests.post(f"{API_URL}/upload-file/", files=files)
    
    if response.status_code == 200:
        st.success("File uploaded successfully!")
        file_info = response.json()
        st.write(f"**Filename:** {file_info['filename']}")
        st.write(f"**Rows:** {file_info['num_rows']} | **Columns:** {file_info['num_columns']}")
        st.write(f"**Columns:** {', '.join(file_info['columns'])}")
    else:
        st.error(response.json()["detail"])

    if st.button("Perform EDA"):
        eda_response = requests.get(f"{API_URL}/eda/")
        if eda_response.status_code == 200:
            eda_html = eda_response.json()["eda_report"]
            st.components.v1.html(eda_html, height=800, scrolling=True)
        else:
            st.error("Failed to generate EDA report.")

    if st.button("Run Prediction Model"):
        target_column = st.text_input("Enter target column for prediction:")
        if target_column:
            prediction_response = requests.post(f"{API_URL}/predict/", json={"target_column": target_column})
            if prediction_response.status_code == 200:
                predictions = prediction_response.json()["predictions"]
                st.write("**Sample Predictions:**", predictions)
            else:
                st.error("Failed to generate predictions. Ensure the target column exists in the dataset.")

    if st.button("Generate AI Insights"):
        insights_response = requests.get(f"{API_URL}/ai-insights/")
        if insights_response.status_code == 200:
            insights = insights_response.json()["ai_insights"]
            st.write("**AI-Generated Insights:**")
            st.write(insights)
        else:
            st.error("Failed to generate AI insights.")
