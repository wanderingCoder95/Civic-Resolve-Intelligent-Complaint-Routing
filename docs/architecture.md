# Project Architecture

Civic Resolve is built with a focus on intelligent maintenance complaint routing. This document outlines the technical structure and data flow of the application.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Data Persistence**: CSV files (Pandas for processing)
- **Machine Learning**: Scikit-learn (Naive Bayes) for complaint categorization
- **Styling**: Modern CSS with glassmorphism and wave animations

## Project Structure

```text
project/
├── app.py                  # Main application entry point and routing
├── auth.py                 # Authentication logic and RBAC
├── model.ipynb             # Jupyter notebook for ML model training
├── model.pkl               # Serialized ML model for real-time predictions
├── vectorizer.pkl          # TF-IDF vectorizer for text processing
├── data/
│   ├── complaints.csv      # Main complaints database
│   ├── users.csv           # User credentials and role definitions
│   └── code/               # Data synthesis and utility scripts
├── static/
│   └── assets/
│       ├── css/            # UI styling and theme definitions
│       ├── js/             # Interactive elements and animations
│       └── images/         # Project logos and assets
└── templates/
    ├── home/               # Landing and role selection pages
    ├── login/              # Multi-role login forms
    ├── dashboard/          # User, Staff, and Admin portals
    └── invalid-login/      # Error and feedback pages
```

## Data Flow

1. **Complaint Submission**: Users submit complaints via the dashboard.
2. **Auto-Categorization**: The backend uses the pre-trained `model.pkl` to predict the maintenance wing (e.g., Electrical, Plumbing) based on the complaint description.
3. **Storage**: The complaint, along with its predicted wing and user metadata, is appended to `complaints.csv`.
4. **Staff View**: Maintenance staff log in and see a filtered view of complaints assigned to their specific wing.
5. **Admin Oversight**: Superadmins have a holistic view of all complaints and can manage the system state.

## Security & RBAC

The system implements Role-Based Access Control (RBAC) with the following roles:
- **Student/Faculty/Staff**: Can file complaints and view their own history.
- **Maintenance**: Can view and manage complaints within their assigned wing.
- **Superadmin**: Full system access, including cross-wing visibility.

Session-based authentication ensures that users can only access routes authorized for their specific role.
