from flask import Flask, request, render_template
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import joblib
import numpy as np

# Load GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Load the saved scaler (ensure the scaler.pkl file is in your app directory)
#scaler = joblib.load('scaler.pkl')

# Flask App
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", prediction="", ltc_prediction="")

@app.route("/predict", methods=["POST"])
def predict():
    # Get text from the form (for GPT-2)
    text = request.form.get("text")
    
    # Get DevOps metrics data from the form (e.g., Time to change, Build time, Build status)
    devops_data = request.form.get("devops_data")
    
    # Initialize predictions
    prediction = ""
    ltc_prediction = ""
    
    # Handle GPT-2 text generation
    if text:
        inputs = tokenizer.encode(text, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(inputs, max_length=100)
        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Handle DevOps metrics prediction (simulated prediction for now)
    if devops_data:
        # Convert the devops_data into a list of numbers (parse user input)
        devops_data_list = list(map(float, devops_data.split(',')))
        
        # Scale the data using the previously fitted scaler
        try:
            scaled_data = scaler.transform([devops_data_list])
            ltc_prediction = f"Scaled DevOps Data: {scaled_data[0]}"
        except Exception as e:
            ltc_prediction = f"Error in processing DevOps data: {str(e)}"
    
    return render_template("index.html", prediction=prediction, ltc_prediction=ltc_prediction)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
