from flask import Flask, render_template, redirect, url_for, session, request, make_response, g
from auth import auth_bp
import mysql.connector
import os

dbconfig = {
    "user": "Placeholder",
    "password": "Placeholder",
    "host": "Placeholder",
    "database": "Placeholder"
}

def get_db_connection():
    return mysql.connector.connect(**dbconfig)

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
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    uid = session.get('user_id')
    cursor.execute('SELECT * FROM complaints WHERE user_id = %s ORDER BY created_at DESC LIMIT 20', (uid,))
    tickets = cursor.fetchall()
    
    if not tickets:
        cursor.execute('SELECT * FROM complaints ORDER BY created_at DESC LIMIT 5')
        tickets = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('dashboard/users/index.html', tickets=tickets)

@app.route('/staff/dashboard')
def staff_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.home'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Aging complaints (simulated as older than 3 days from 2026-04-21)
    # Using MySQL syntax: created_at <= DATE_SUB('2026-04-21', INTERVAL 3 DAY)
    cursor.execute("SELECT * FROM complaints WHERE status != 'Resolved' AND created_at <= DATE_SUB('2026-04-21', INTERVAL 3 DAY) ORDER BY created_at ASC LIMIT 10")
    aging_tickets = cursor.fetchall()
    
    # All active complaints
    cursor.execute("SELECT * FROM complaints WHERE status != 'Resolved' ORDER BY created_at DESC LIMIT 20")
    active_tickets = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('dashboard/staff/index.html', aging_tickets=aging_tickets, active_tickets=active_tickets)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.home'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as total FROM complaints WHERE status != 'Resolved'")
    total_active = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as resolved FROM complaints WHERE status = 'Resolved'")
    resolved_count = cursor.fetchone()['resolved']
    
    cursor.execute("SELECT COUNT(*) as all_tickets FROM complaints")
    all_tickets = cursor.fetchone()['all_tickets']
    
    resolution_rate = round((resolved_count / all_tickets) * 100) if all_tickets > 0 else 0

    cursor.close()
    conn.close()
    return render_template('dashboard/admin/index.html', total_active=total_active, resolution_rate=resolution_rate)



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