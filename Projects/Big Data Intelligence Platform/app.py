from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('./random_forest_model.joblib')  # Adjust the filename if needed

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request
    data = request.get_json(force=True)
    
    # Convert data to DataFrame
    df = pd.DataFrame(data, index=[0])
    
    # Make prediction
    prediction = model.predict(df)
    
    # Return the prediction
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    