from flask import Flask, request, render_template
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Flask App
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", prediction="")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form["text"]
    
    if text.strip():  # Ensure text is not empty or just spaces
        inputs = tokenizer.encode(text, return_tensors="pt")
        
        # Get the input length
        input_length = inputs.shape[1]
        
        # Set max_new_tokens to control how many new tokens to generate
        max_new_tokens = 100  # You can adjust this value
        
        with torch.no_grad():
            outputs = model.generate(inputs, max_new_tokens=max_new_tokens)

        prediction = tokenizer.decode(outputs[0], skip_special_tokens=True)
    else:
        prediction = "Please enter some text to generate a prediction."

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
