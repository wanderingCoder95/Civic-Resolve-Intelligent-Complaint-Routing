from flask import Flask, render_template, redirect, url_for, session, request, make_response
from auth import auth_bp

app = Flask(__name__)
app.secret_key = "your-secret-key" # Session Keys are to be randomly generated later

app.register_blueprint(auth_bp)



@app.after_request
def add_no_cache_headers(response):
    # Prevent browser/proxy caching so back button cannot show stale protected pages.
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Load model
# model = pickle.load(open("model.pkl", "rb"))
# vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


# ===== DASHBOARD ROUTES =====
@app.route('/users/dashboard')
def users_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.home'))
    return render_template('dashboard/users/index.html')

@app.route('/staff/dashboard')
def staff_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.home'))
    return render_template('dashboard/staff/index.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.home'))
    return render_template('dashboard/admin/index.html')



# ===== OLD ML CODE (COMMENTED OUT) =====
# #karthik try using this while building the frontend
# 
# # Prediction function
# def predict_issue(text):
#     vec = vectorizer.transform([text])
#     return model.predict(vec)[0]
# 
# # Test route
# @app.route('/')
# def home():
#     return "Server running"
# 
# # Main route (frontend will use this)
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     text = data['description']
#     
#     result = predict_issue(text)
#     
#     return jsonify({
#         "department": result,
#         "status": "Pending"
#     })
# 
# #use the model.pkl to load the model and vectorizer.pkl to use the vectorizer

if __name__ == "__main__":
    app.run(debug=True)