from flask import Flask, render_template, redirect, url_for, session, request, make_response, g
from auth import auth_bp
import mysql.connector
import os
import uuid
from datetime import datetime

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

app.get_db_connection = get_db_connection

app.register_blueprint(auth_bp)



import pickle
import numpy as np

# Load ML Model and Vectorizer for auto-assignment
try:
    with open(os.path.join(os.path.dirname(__file__), "model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(os.path.dirname(__file__), "vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)
except Exception as e:
    print(f"Warning: ML models not loaded. {e}")
    model = None
    vectorizer = None

def predict_wing(description):
    if not model or not vectorizer:
        return "Unassigned"
    try:
        # Preprocess and predict
        vec = vectorizer.transform([description])
        prediction = model.predict(vec)[0]
        return prediction
    except:
        return "Unassigned"


@app.before_request
def enforce_authorization():
    # List of endpoints that DO NOT require login
    public_endpoints = [
        'auth.root', 'auth.home', 'auth.login', 
        'auth.user_login', 'auth.maintenance_login', 
        'auth.invalid_login', 'static'
    ]

    # 1. Allow access to public endpoints
    if request.endpoint in public_endpoints or not request.endpoint:
        return

    # 2. Global Login Check: Require login for all other routes
    if 'user_id' not in session:
        return redirect(url_for('auth.home'))

    # 3. Path & Role-Based Access Control (RBAC) - Strict 1-to-1 Mapping
    role = session.get('role')
    path = request.path

    # Admin routes: Only for superadmin
    if path.startswith('/admin') and role != 'superadmin':
        return redirect(url_for('auth.home'))

    # Staff routes: Only for maintenance staff
    if path.startswith('/staff') and role != 'maintenance':
        return redirect(url_for('auth.home'))
    
    # User routes: For regular users (student/faculty/office staff)
    if path.startswith('/users') and role not in ['student', 'faculty', 'staff']:
        return redirect(url_for('auth.home'))
    
    # API Protection (Strict)
    if path.startswith('/api/assign_ticket') and role != 'superadmin':
        return redirect(url_for('auth.home'))
    
    if path.startswith('/api/update_ticket') and role != 'maintenance':
        return redirect(url_for('auth.home'))


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
    user_id = session.get('user_id')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all tickets filed by this specific user, ordered by status importance
    cursor.execute("""
        SELECT * FROM complaints 
        WHERE user_id = %s 
        ORDER BY FIELD(status, 'Pending', 'In Progress', 'Resolved', 'Referred'), created_at DESC
    """, (user_id,))
    tickets = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard/users/index.html', tickets=tickets)

@app.route('/staff/dashboard')
def staff_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    staff_wing = session.get('wing')
    
    if staff_wing:
        # Aging complaints for the staff's specific wing (simulated as older than 3 days from 2026-04-21)
        cursor.execute("SELECT * FROM complaints WHERE status != 'Resolved' AND true_wing = %s AND created_at <= DATE_SUB('2026-04-21', INTERVAL 3 DAY) ORDER BY created_at ASC LIMIT 10", (staff_wing,))
        aging_tickets = cursor.fetchall()
        
        # All active complaints for the staff's specific wing
        cursor.execute("SELECT * FROM complaints WHERE status != 'Resolved' AND true_wing = %s ORDER BY created_at DESC LIMIT 20", (staff_wing,))
        active_tickets = cursor.fetchall()
    else:
        # Fallback: show all aging complaints
        cursor.execute("SELECT * FROM complaints WHERE status != 'Resolved' AND created_at <= DATE_SUB('2026-04-21', INTERVAL 3 DAY) ORDER BY created_at ASC LIMIT 10")
        aging_tickets = cursor.fetchall()
        
        # Fallback: show all active complaints
        cursor.execute("SELECT * FROM complaints WHERE status != 'Resolved' ORDER BY created_at DESC LIMIT 20")
        active_tickets = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('dashboard/staff/index.html', aging_tickets=aging_tickets, active_tickets=active_tickets)

@app.route('/api/update_ticket', methods=['POST'])
def update_ticket():
    if 'user_id' not in session or session.get('role') not in ['maintenance', 'superadmin']:
        return {"error": "Unauthorized"}, 403
    
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    field = data.get('field')
    value = data.get('value')
    
    if field not in ['priority', 'status']:
        return {"error": "Invalid field"}, 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update ticket
    cursor.execute(f"UPDATE complaints SET {field} = %s WHERE ticket_id = %s", (value, ticket_id))
    
    # Log action
    user_id = session.get('user_id', 'Unknown')
    role = session.get('role', 'User')
    action_msg = f"{role.capitalize()} {user_id} updated {field} of {ticket_id} to {value}"
    cursor.execute("INSERT INTO syslogs (action, performed_by) VALUES (%s, %s)", (action_msg, user_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"success": True}

@app.route('/api/assign_ticket', methods=['POST'])
def assign_ticket():
    if 'user_id' not in session or session.get('role') != 'superadmin':
        return {"error": "Unauthorized"}, 403
    
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    wing = data.get('wing')
    
    if not ticket_id or not wing:
        return {"error": "Missing data"}, 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    # Update ticket to new wing and reset status
    cursor.execute("UPDATE complaints SET status = 'Pending', true_wing = %s, wing = %s WHERE ticket_id = %s", (wing, wing, ticket_id))
    
    # Log the action
    admin_id = session.get('user_id', 'Admin')
    action_msg = f"Admin {admin_id} reassigned ticket {ticket_id} to {wing}"
    cursor.execute("INSERT INTO syslogs (action, performed_by) VALUES (%s, %s)", (action_msg, admin_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"success": True}

@app.route('/api/submit_ticket', methods=['POST'])
def submit_ticket():
    if 'user_id' not in session:
        return {"error": "Unauthorized"}, 401
    
    data = request.get_json()
    description = data.get('description')
    location = data.get('location')
    
    if not description or not location:
        return {"error": "Missing data"}, 400
        
    user_id = session.get('user_id')
    ticket_id = f"TICK_{uuid.uuid4().hex[:6].upper()}"
    
    # ML Prediction for auto-assignment
    predicted_wing = predict_wing(description)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert ticket with predicted wing (filling both wing and true_wing for consistency)
    cursor.execute("""
        INSERT INTO complaints (ticket_id, user_id, description, location, status, priority, wing, true_wing, created_at)
        VALUES (%s, %s, %s, %s, 'Pending', 'None', %s, %s, NOW())
    """, (ticket_id, user_id, description, location, predicted_wing, predicted_wing))
    
    # Log action
    action_msg = f"New Ticket {ticket_id} auto-assigned to {predicted_wing} wing"
    cursor.execute("INSERT INTO syslogs (action, performed_by) VALUES (%s, %s)", (action_msg, user_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"success": True, "ticket_id": ticket_id, "predicted_wing": str(predicted_wing)}

@app.route('/api/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'user_id' not in session:
        return {"error": "Unauthorized"}, 401
    
    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment')
    user_id = session.get('user_id')
    
    # Log the feedback in syslogs for now
    conn = get_db_connection()
    cursor = conn.cursor()
    action_msg = f"User Feedback: Rating={rating}, Comment='{comment}'"
    cursor.execute("INSERT INTO syslogs (action, performed_by) VALUES (%s, %s)", (action_msg, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"success": True}

@app.route('/admin/dashboard')
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # STATS
    cursor.execute("SELECT COUNT(*) AS total_active FROM complaints WHERE status != 'Resolved'")
    total_active = cursor.fetchone()['total_active']

    cursor.execute("SELECT COUNT(*) AS resolved FROM complaints WHERE status = 'Resolved'")
    resolved = cursor.fetchone()['resolved']

    cursor.execute("SELECT COUNT(*) AS total FROM complaints")
    total = cursor.fetchone()['total']

    resolution_rate = int((resolved / total) * 100) if total > 0 else 0

    # ESCALATED
    cursor.execute("""
        SELECT ticket_id, description, true_wing
        FROM complaints
        WHERE status = 'Referred'
        ORDER BY created_at DESC
        LIMIT 5
    """)
    escalated = cursor.fetchall()

    # LOGS
    cursor.execute("""
        SELECT timestamp, action
        FROM syslogs
        ORDER BY timestamp DESC
        LIMIT 6
    """)
    logs = cursor.fetchall()

    # WINGS
    cursor.execute("SELECT DISTINCT wing FROM users WHERE role = 'maintenance' AND wing IS NOT NULL")
    wings = [r['wing'] for r in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render_template(
        'dashboard/admin/index.html',
        total_active=total_active,
        resolution_rate=resolution_rate,
        escalated=escalated,
        logs=logs,
        wings=wings
    )


if __name__ == "__main__":
    import sys
    # Allow port to be passed as an argument, default to 5000
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=True, port=port)