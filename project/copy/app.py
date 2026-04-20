#karthik try using this while building the frontend
from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


def is_valid(text):
    text = text.strip()
    return len(text) >= 5 and len(text.split()) >= 2

def keyword_rule(text):
    text = text.lower()
    if "water" in text or "leak" in text:
        return "Plumbing"
    if "wifi" in text or "network" in text:
        return "IT"
    return None

def handle_ticket(text):
    if not is_valid(text):
        return "Invalid input"
    
    rule = keyword_rule(text)
    if rule:
        return rule
    
    vec = vectorizer.transform([text])
    probs = model.predict_proba(vec)[0]
    
    if max(probs) < 0.5:
        return "Uncertain"
    
    return model.classes_[probs.argmax()]

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

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['description']   # from frontend
    
    result = handle_ticket(text)         # 👈 YOUR CODE USED HERE
    
    return {"department": result}

if __name__ == "__main__":
    app.run(debug=True)

#use the model.pkl to load the model and vectorizer.pkl to use the vectorizer   