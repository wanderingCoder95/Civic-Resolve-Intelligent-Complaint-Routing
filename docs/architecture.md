# Project Architecture

Civic Resolve is an intelligent maintenance complaint management system featuring automated routing and role-based tracking.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Database**: MySQL (for live ticket persistence and user authentication)
- **Machine Learning**: Scikit-learn (**Multinomial Naive Bayes**) for complaint categorization
- **Styling**: Premium Modern CSS with glassmorphism and micro-animations

## Project Structure

```text
project/
├── app.py                  # Main application & ML inference logic
├── auth.py                 # MySQL-backed authentication & RBAC
├── model.ipynb             # Model training & data analysis
├── model.pkl               # Serialized Multinomial Naive Bayes model
├── vectorizer.pkl          # TF-IDF vectorizer (1-2 ngrams)
├── data/
│   ├── complaints.csv      # Historical training dataset
│   ├── users.csv           # Seed data for users
│   └── sql/                # SQL initialization scripts
├── static/
│   └── assets/             # CSS themes, animations, and icons
└── templates/
    ├── home/               # Landing & role selection
    ├── login/              # Multi-role login portals
    ├── dashboard/          # Student & Staff operations
    └── invalid-login/      # Error & triage feedback
```

## Intelligent Data Flow

1. **Complaint Submission**: Users submit text-based complaints through the dashboard.
2. **Predictive Triage**: 
   - Descriptions are processed through the **Multinomial Naive Bayes** model.
   - If confidence is high (>50%), the ticket is routed to a specific wing (e.g., Electrical).
   - If confidence is low or input is junk, the ticket is flagged as **Spam** or **Uncertain** and routed to **General**.
3. **Database Persistence**: Tickets are saved to MySQL with dual labels: `wing` (display label) and `true_wing` (routing key).
4. **Staff Filtering**: Staff dashboards fetch tickets where `true_wing` matches their assigned wing **OR** is set to `General`. This ensures that ambiguous issues are triaged by the entire team.

## Role-Based Access Control (RBAC)

- **Users (Student/Faculty)**: Can file complaints and track the model-predicted category and status.
- **Maintenance Staff**: Access wing-specific tickets and universal triage (General) tickets. Can update priority and status.
- **Superadmin**: Full system control and cross-wing oversight.

Authentication is managed via MySQL-backed sessions, ensuring strict isolation between user types.
