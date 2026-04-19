#karthik try using this while building the frontend
from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Prediction function
def predict_issue(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

# Test route
@app.route('/')
def home():
    return "Server running"

# Main route (frontend will use this)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['description']
    
    result = predict_issue(text)
    
    return jsonify({
        "department": result,
        "status": "Pending"
    })

if __name__ == "__main__":
    app.run(debug=True)

#use the model.pkl to load the model and vectorizer.pkl to use the vectorizer