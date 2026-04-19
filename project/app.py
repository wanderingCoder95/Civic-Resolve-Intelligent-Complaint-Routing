from flask import Flask, render_template, redirect, url_for, session, request
import pandas as pd

app = Flask(__name__)
app.secret_key = "your-secret-key" # Session Keys are to be randomly generated later

users_df = pd.read_csv("data/users.csv")

# Load model
# model = pickle.load(open("model.pkl", "rb"))
# vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ===== AUTH ROUTES =====
@app.route('/')
@app.route('/login')
def login():
    return render_template('home/index.html')

@app.route('/invalid-login')
def invalid_login():
    login_type = request.args.get('type', 'user')  # 'user' or 'maintenance'
    if login_type == 'maintenance':
        login_link = url_for('maintenance_login')
    else:
        login_link = url_for('user_login')
    return render_template('invalid-login/index.html', login_link=login_link)

@app.route('/user', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        user_id = request.form.get('username')
        password = request.form.get('password')
        
        # Validate against users.csv - Users (Students, Faculty, Staff)
        user = users_df[(users_df['user_id'] == user_id) & 
                        (users_df['password'] == password) & 
                        (users_df['role'].isin(['student', 'faculty', 'staff']))]
        
        if not user.empty:
            session['user_id'] = user_id
            session['role'] = user.iloc[0]['role']
            session['name'] = user.iloc[0]['name']
            return redirect(url_for('users_dashboard'))
        else:
            return redirect(url_for('invalid_login', type='user'))
    
    # GET: Show user login form
    return render_template('login/users.html')

@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance_login():
    if request.method == 'POST':
        user_id = request.form.get('username')
        password = request.form.get('password')
        
        # Validate against users.csv - Maintenance Staff and Admin
        user = users_df[(users_df['user_id'] == user_id) & 
                        (users_df['password'] == password) & 
                        (users_df['role'].isin(['maintenance', 'superadmin']))]
        
        if not user.empty:
            session['user_id'] = user_id
            session['role'] = user.iloc[0]['role']
            session['name'] = user.iloc[0]['name']
            wing = user.iloc[0]['wing']
            if pd.notna(wing):
                session['wing'] = wing
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('invalid_login', type='maintenance'))
    
    # GET: Show maintenance login form
    return render_template('login/maintenance.html')

# ===== DASHBOARD ROUTES =====
@app.route('/users/dashboard')
def users_dashboard():
    # TODO: Check if user is logged in
    # if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('dashboard/users/index.html')

@app.route('/staff/dashboard')
def staff_dashboard():
    # TODO: Check if user is logged in
    # if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('dashboard/staff/index.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    # TODO: Check if user is logged in
    # if 'user_id' not in session: return redirect(url_for('login'))
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