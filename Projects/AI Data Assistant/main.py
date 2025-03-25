from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
import torch
import io
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_profiling import ProfileReport
from transformers import pipeline
import torch.nn as nn
import torch.optim as optim

app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available
uploaded_df = None  # Initialize globally

@app.get("/")
def home():
    return {"message": "AI Data Assistant API (GPU-Optimized) is running successfully!"}

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    global uploaded_df

    contents = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents), skiprows=1)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Upload CSV or Excel (.xlsx).")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file is empty!")

    df.columns = df.columns.astype(str).str.strip()
    uploaded_df = df.copy()

    return {
        "filename": file.filename,
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": list(df.columns),
    }

@app.get("/eda/")
def perform_eda():
    global uploaded_df
    if uploaded_df is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a CSV or Excel file first.")

    profile = ProfileReport(uploaded_df, explorative=True)
    report_html = profile.to_html()
    
    return {"eda_report": report_html}

@app.post("/predict/")
def predict(data: dict):
    global uploaded_df
    if uploaded_df is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a dataset first.")

    target_column = data.get("target_column")
    if target_column not in uploaded_df.columns:
        raise HTTPException(status_code=400, detail="Target column not found in dataset.")
    
    feature_cols = [col for col in uploaded_df.columns if col != target_column]
    X = torch.tensor(uploaded_df[feature_cols].fillna(0).values, dtype=torch.float32, device=device)
    y = torch.tensor(uploaded_df[target_column].fillna(0).values, dtype=torch.float32, device=device)
    
    model = nn.Linear(X.shape[1], 1).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    
    for _ in range(500):
        optimizer.zero_grad()
        predictions = model(X).squeeze()
        loss = criterion(predictions, y)
        loss.backward()
        optimizer.step()
    
    predictions = model(X).detach().cpu().numpy().tolist()
    return {"predictions": predictions[:10]}  # Return first 10 predictions

@app.get("/ai-insights/")
def ai_insights():
    global uploaded_df
    if uploaded_df is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a dataset first.")
    
    generator = pipeline("text-generation", model="gpt-4")
    prompt = f"Analyze the following dataset and provide insights: {uploaded_df.head().to_dict()}"
    insights = generator(prompt, max_length=100, num_return_sequences=1)
    
    return {"ai_insights": insights[0]["generated_text"]}

@app.post("/chatbot/")
def chatbot(query: dict):
    user_input = query.get("message")
    if not user_input:
        raise HTTPException(status_code=400, detail="No user message provided.")
    
    generator = pipeline("text-generation", model="gpt-4")
    response = generator(user_input, max_length=100, num_return_sequences=1)
    return {"chatbot_response": response[0]["generated_text"]}
