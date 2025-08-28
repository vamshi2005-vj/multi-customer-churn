![Python](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)
# Multi-Customer Churn Prediction Web App

A **Flask web application** for predicting customer churn. Supports both **single-customer** and **multi-customer (CSV)** predictions. Includes user authentication, OTP-based password reset via email, and database storage of predictions. At-risk customers can be downloaded as an Excel file.

---

## Features

- **User Authentication**
  - Admin and employee login
  - Password hashing for security
  - OTP-based password reset sent via email

- **Customer Churn Prediction**
  - Single-customer prediction via web form
  - Bulk predictions via CSV upload
  - Preprocessing and scaling using trained model features

- **Data Storage & Export**
  - SQLite database (`churn_app.db`) stores customer data and predictions
  - Export at-risk customers to Excel (`at_risk_customers.xlsx`)

- **Email Notifications**
  - OTP automatically sent to user email for password resets

---

## Project Structure
Multi-Churn/
    app.py                     # Main Flask application
    churn_predict_model.pkl     # Pre-trained churn prediction model
    Churn_Modelling.csv         # Sample dataset for preprocessing
    churn_app.db                # SQLite database
    requirements.txt            # Python dependencies
    at_risk_customers.xlsx      # Excel file for at-risk customers
    uploads/                    # Uploaded CSV files (bulk predictions)
    templates/                  # HTML templates
        login.html              # Login & OTP template
        index.html              # Prediction form template
    static/                     # Static files (CSS/JS/images)
        css/
        js/
        images/
    logs/                       # Optional logs folder
        app.log
    README.md                   # Project documentation



---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/vamshi2005-vj/multi-customer-churn.git
cd multi-customer-churn


Create and activate a virtual environment (recommended)

python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

**Install dependencies**
pip install -r requirements.txt

Configure Flask-Mail
Edit app.py to set your email credentials:

app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

Use an App Password for Gmail, not your normal password.

**Usage**
Run the Flask app
python app.py


Open in browser

http://127.0.0.1:5000/


**Login**
Use Admin or Employee credentials
If password is incorrect, an OTP is sent to the registered email

**Predictions**
Single-customer predictions via form
Multi-customer predictions by uploading a CSV file
Download at-risk customers as at_risk_customers.xlsx
CSV File Format for Bulk Upload
The CSV must contain the following columns:
CustomerId, CreditScore, Geography, Gender, Age, Tenure,
Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary
Geography: 1 = Germany, 2 = Spain, 3 = France
Gender: 0 = Female, 1 = Male

**Dependencies**
Python 3.10+
Flask
Flask-Mail
pandas
scikit-learn
joblib
openpyxl
werkzeug
sqlite3 (built-in)

**Install all via:**
pip install -r requirements.txt

License

MIT License

Author

Vamshi Zero
