# Civic Resolve - Documentation

Quick reference for project structure and key features.

## Project Structure

```
project/
├── app.py                          # Main Flask app with auth routes
├── model.ipynb                     # ML model
├── data/
│   ├── complaints.csv              # Complaints dataset
│   ├── users.csv                   # User credentials (login)
│   └── code/                       # Data synthesis notebooks
├── static/
│   └── assets/
│       ├── css/auth-pages.css      # Shared auth styling
│       ├── js/auth-waves.js        # Wave animation
│       └── images/sau-white-logo.png
└── templates/
    ├── auth.py                     # Preview server
    ├── home/
    │   └── index.html              # Role selection page
    ├── login/
    │   ├── users.html              # User login form
    │   └── maintenance.html        # Maintenance login form
    ├── invalid-login/
    │   └── index.html              # Error page
    └── dashboard/
        ├── users/index.html
        ├── staff/index.html
        └── admin/index.html
```

## Authentication

### Pages
- **Home**: `templates/home/index.html` - Role selection page
- **User Login**: `templates/login/users.html` - User credential form (Students, Faculty, Staff)
- **Maintenance Login**: `templates/login/maintenance.html` - Maintenance staff credential form
- **Error**: `templates/invalid-login/index.html` - Invalid login message

### Validation
- Uses `data/users.csv` for authentication
- **User roles** (`/user`): `student`, `faculty`, `staff`
- **Maintenance roles** (`/maintenance`): `maintenance`, `superadmin`
- Role-based access control enforced - users cannot access maintenance portal and vice versa

### Session Storage
On successful login, stores in session:
- `user_id` - User's ID from CSV
- `role` - User's role (student, faculty, staff, maintenance, superadmin)
- `name` - User's full name
- `wing` - Department/wing (for maintenance staff)

## Colors & Styling

- **CSS**: `static/assets/css/auth-pages.css` - Shared styling for all auth pages
- **Animation**: `static/assets/js/auth-waves.js` - Canvas wave background (blue for user, red for error)
- **Logo**: `static/assets/images/sau-white-logo.png`

Colors customizable via CSS variables in auth-pages.css

## Running

### Main Application (Recommended)
```bash
cd project
python app.py
```
Visit `http://localhost:5000/login` to start

### Preview Server (Alternative)
```bash
cd project
python templates/auth.py
```
Visit `http://127.0.0.1:8084` (older preview server)

## Routes

**Auth Flow:**
- `/` or `/login` → `home/index.html` (Role selection)
- `/user` (GET) → `login/users.html` (User login form)
- `/user` (POST) → Validates credentials → Success: `/users/dashboard` | Failure: `/invalid-login?type=user`
- `/maintenance` (GET) → `login/maintenance.html` (Maintenance login form)
- `/maintenance` (POST) → Validates credentials → Success: `/admin/dashboard` | Failure: `/invalid-login?type=maintenance`
- `/invalid-login` → Error page with context-aware "Try Again" link

**Dashboards:**
- `/users/dashboard` → Users dashboard (Students, Faculty, Staff)
- `/staff/dashboard` → Staff dashboard
- `/admin/dashboard` → Admin/Maintenance dashboard

## Test Credentials

From `data/users.csv`:
- **Users**: `STU00001` / `Pass483` (student)
- **Users**: `FAC001` / `User719` (faculty)
- **Maintenance**: `MNT001` / `fixit56`
- **Admin**: `ADMIN001` / `Root@123` (superadmin)

## Data

- `data/users.csv` - User credentials
- `data/complaints.csv` - Complaints data
