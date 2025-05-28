from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
import torch
import io
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from transformers import pipeline
import torch.nn as nn
import torch.optim as optim
from dotenv import load_dotenv
load_dotenv()
import openai
from openai import OpenAI
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
from google import genai
GEMINI_KEY = os.environ.get('GEMINI_KEY')
app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available
uploaded_df = None  # Initialize globally
print(device)
print(uploaded_df)

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
        raise HTTPException(400, "No file uploaded.")

    target_column = data.get("target_column")
    if not target_column or target_column not in uploaded_df.columns:
        raise HTTPException(400, "Target column missing or invalid.")

    df = uploaded_df.dropna(subset=[target_column]).copy()
    feature_cols = [col for col in df.columns if col != target_column]

    # Encode categoricals
    for col in feature_cols:
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))

    X_raw = df[feature_cols].fillna(0)
    y_raw = df[target_column].fillna(0)

    if not pd.api.types.is_numeric_dtype(y_raw):
        raise HTTPException(400, "Target column must be numeric.")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_raw, test_size=0.2, random_state=42)

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32, device=device)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32, device=device)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32, device=device)

    model = nn.Linear(X_train.shape[1], 1).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()

    for _ in range(500):
        model.train()
        optimizer.zero_grad()
        preds = model(X_train_tensor).squeeze()
        loss = criterion(preds, y_train_tensor)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        test_preds = model(X_test_tensor).squeeze().cpu().numpy()

    mse = mean_squared_error(y_test, test_preds)
    r2 = r2_score(y_test, test_preds)

    return {
        "status": "success",
        "model": "LinearRegression (PyTorch)",
        "target_column": target_column,
        "mse": mse,
        "r2_score": r2,
        "predictions": test_preds[:10].tolist()
    }
@app.get("/ai-insights/")
def ai_insights():
    global uploaded_df
    if uploaded_df is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a dataset first.")
    
    prompt = f"You're a data analyst. Give insights about the dataset with columns: {', '.join(uploaded_df.columns[:10])}. Data preview: {uploaded_df.head().to_dict()}"
    try:
        #FIXME: The below code is for the openAI based chat completions
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system"   , "content": "You are an expert data analyst."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.7,
        #     max_tokens=300
        # )
        # # insights = response.choices[0].message["content"]
        # # return {"ai_insights": insights}
        
        client = genai.Client(api_key=GEMINI_KEY)

        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        chat_response = response.text
        return {"ai_insights":chat_response}
    except Exception as e:
        print("❌ OpenAI API error:", e)  # <-- this will show in terminal
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/chatbot/")
# def chatbot(query: dict):
#     user_input = query.get("message")
#     if not user_input:
#         raise HTTPException(status_code=400, detail="No user message provided.")
    
#     generator = pipeline("text-generation", model="gpt-4")
#     response = generator(user_input, max_length=100, num_return_sequences=1)
#     return {"chatbot_response": response[0]["generated_text"]}



@app.post("/query_file")
def query_file(query: dict):
    global uploaded_df
    if uploaded_df is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a dataset first.")

    query_text = query.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="No query provided.")

    try:
        # Perform query on the uploaded file
        prompt = f"""You're a data analyst. Answer the below user query using the given information.
        
        Information: {', '.join(uploaded_df.columns[:10])}. Data preview: {uploaded_df.head().to_dict()}

        User query: {query_text}
        """
        print(prompt)

        client = genai.Client(api_key=GEMINI_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        print(response)
        result = response.text
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

