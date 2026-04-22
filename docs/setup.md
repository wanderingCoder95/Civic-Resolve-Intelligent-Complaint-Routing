# Setup Guide

This guide will walk you through setting up the Civic Resolve platform on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/wanderingCoder95/Case-Study-Mini-Project.git
   cd Case-Study-Mini-Project
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   The project requires Flask and other data science libraries.
   ```bash
   pip install flask pandas scikit-learn
   ```

4. **Initialize the Database**
   Ensure the `data/` directory contains `users.csv` and `complaints.csv`. These serve as the primary data stores for the application.

## Running the Application

1. **Start the Flask Server**
   ```bash
   cd project
   python app.py
   ```

2. **Access the Web Interface**
   Open your browser and navigate to `http://localhost:5000`.

## Troubleshooting

- **Port already in use**: If port 5000 is occupied, you can change the port in `project/app.py` or run `flask run --port <your_port>`.
- **Missing Data Files**: If the application fails to start due to missing CSV files, verify they are present in the `project/data/` directory.
