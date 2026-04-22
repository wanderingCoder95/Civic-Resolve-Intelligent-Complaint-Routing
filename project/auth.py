from flask import Blueprint, render_template, redirect, url_for, session, request, make_response, current_app

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def root():
    return redirect(url_for('auth.home'))


@auth_bp.route('/home')
def home():
    if 'user_id' in session:
        session.clear()
    return render_template('login/index.html')


@auth_bp.route('/user', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET' and 'user_id' in session:
        session.clear()

    if request.method == 'POST':
        user_id = request.form.get('username')
        password = request.form.get('password')

        conn = current_app.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT user_id, role, name
            FROM users
            WHERE user_id = %s AND password = %s
        """, (user_id, password))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            session['name'] = user['name']
            return redirect(url_for('users_dashboard'))

        return redirect(url_for('auth.invalid_login', next=url_for('auth.user_login')))

    return render_template('login/users/index.html')


@auth_bp.route('/maintenance', methods=['GET', 'POST'])
def maintenance_login():
    if request.method == 'GET' and 'user_id' in session:
        session.clear()

    if request.method == 'POST':
        user_id = request.form.get('username')
        password = request.form.get('password')

        conn = current_app.get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT user_id, role, name, wing
            FROM users
            WHERE user_id = %s AND password = %s
        """, (user_id, password))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            session['name'] = user['name']
            session['wing'] = user.get('wing')

            if user['role'] == 'superadmin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('staff_dashboard'))

        return redirect(url_for('auth.invalid_login', next=url_for('auth.maintenance_login')))

    return render_template('login/maintenance/index.html')


@auth_bp.route('/invalid-login')
def invalid_login():
    login_link = request.args.get('next', url_for('auth.home'))
    return render_template('invalid-login/index.html', login_link=login_link)


@auth_bp.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect(url_for('auth.home')))
    response.headers["Clear-Site-Data"] = '"cache", "storage"'
    return response