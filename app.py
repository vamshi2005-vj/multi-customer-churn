from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_mail import Mail, Message
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import os

app = Flask(__name__)
app.secret_key = 'vamshi'

# Flask-Mail config (use your real credentials here)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vamshijakkali609@gmail.com'       # your email
app.config['MAIL_PASSWORD'] = 'ctjx entx tomr mnfo'          # your app password (not your normal email password)
mail = Mail(app)

DATABASE = 'churn_app.db'

# Load model & scaler
model = joblib.load('churn_predict_model.pkl')
data = pd.read_csv('Churn_Modelling.csv')
data = data.drop(['RowNumber', 'Surname', 'CustomerId'], axis=1)
data = pd.get_dummies(data, drop_first=True)
X = data.drop('Exited', axis=1)
scaler = StandardScaler()
scaler.fit(X)

# Globals
predictions_df = pd.DataFrame()
otp_store = {}  # Store OTP temporarily {user_id: otp}

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def send_otp_email(to_email, otp):
    msg = Message(subject="Your OTP Code",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.body = f"Your OTP for password reset is: {otp}"
    mail.send(msg)

@app.route('/')
def home():
    return redirect(url_for('login_choice'))

@app.route('/login_choice')
def login_choice():
    # Clear OTP session data if any
    session.pop('otp_user_id', None)
    session.pop('otp_verified', None)
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_type = request.form.get('user_type')
    user_id = request.form.get('user_id')
    password = request.form.get('password')
    entered_otp = request.form.get('otp')

    if not user_type or not user_id:
        return render_template('login.html', error="Please select user type and enter ID.")

    conn = get_db_connection()
    if user_type == 'admin':
        user = conn.execute('SELECT * FROM admins WHERE id = ?', (user_id,)).fetchone()
    else:
        user = conn.execute('SELECT * FROM employees WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if not user:
        return render_template('login.html', error="User not found.")

    # If OTP is being verified:
    if entered_otp:
        if session.get('otp_user_id') == user_id and otp_store.get(user_id) == entered_otp:
            # OTP correct: allow password reset form submission (simplified)
            session['otp_verified'] = True
            flash("OTP verified! Please enter your new password.", "info")
            return render_template('login.html', show_reset=True, user_id=user_id, user_type=user_type)
        else:
            return render_template('login.html', error="Invalid OTP. Please try again.", show_otp=True, user_id=user_id, user_type=user_type)

    # If new password is submitted (after OTP verification)
    new_password = request.form.get('new_password')
    if new_password and session.get('otp_verified') and session.get('otp_user_id') == user_id:
        # Update password in DB
        hashed_pw = generate_password_hash(new_password)
        conn = get_db_connection()
        table = 'admins' if user_type == 'admin' else 'employees'
        conn.execute(f'UPDATE {table} SET password = ? WHERE id = ?', (hashed_pw, user_id))
        conn.commit()
        conn.close()
        # Clear OTP session info
        session.pop('otp_verified', None)
        session.pop('otp_user_id', None)
        otp_store.pop(user_id, None)
        flash("Password updated successfully! Please login.", "success")
        return redirect(url_for('login_choice'))

    # Normal login password check
    if check_password_hash(user['password'], password):
        session['user_id'] = user_id
        session['user_type'] = user_type
        session['user_name'] = user['name']
        return redirect(url_for('index'))
    else:
        # Password incorrect -> send OTP to registered email automatically
        # Store OTP and user_id in session for verification
        otp = ''.join(random.choices(string.digits, k=6))
        otp_store[user_id] = otp
        session['otp_user_id'] = user_id
        try:
            send_otp_email(user['email'], otp)
        except Exception as e:
            return render_template('login.html', error=f"Error sending OTP email: {str(e)}")
        return render_template('login.html', error="Wrong password. Enter OTP sent to your registered email.", show_otp=True, user_id=user_id, user_type=user_type)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_choice'))

@app.route('/predict', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login_choice'))

    global predictions_df
    error = None
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.csv'):
            error = "Please upload a valid CSV file (.csv only)."
            return render_template('index.html', predictions=None, error=error, user_name=session['user_name'])

        try:
            df = pd.read_csv(file)
            original_df = df.copy()

            required_features = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure',
                                 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
            missing = [col for col in required_features if col not in df.columns]
            if missing:
                error = f"Missing required columns: {', '.join(missing)}"
                return render_template('index.html', predictions=None, error=error, user_name=session['user_name'])

            df = pd.get_dummies(df, drop_first=True)

            for col in (set(X.columns) - set(df.columns)):
                df[col] = 0
            df = df[X.columns]

            df_scaled = scaler.transform(df)
            predictions = model.predict(df_scaled)

            original_df['Exited'] = predictions
            predictions_df = original_df[original_df['Exited'] == 1]

            # Save churn results (Exited) to DB
            conn = get_db_connection()
            for idx, row in original_df.iterrows():
                conn.execute('''INSERT OR REPLACE INTO customers (CustomerId, CreditScore, Geography, Gender, Age,
                                Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (int(row.get('CustomerId', idx)), row['CreditScore'], row['Geography'], row['Gender'],
                              row['Age'], row['Tenure'], row['Balance'], row['NumOfProducts'], row['HasCrCard'],
                              row['IsActiveMember'], row['EstimatedSalary'], int(row['Exited'])))
            conn.commit()
            conn.close()

            total = len(original_df)
            at_risk = sum(predictions)
            safe = total - at_risk

            return render_template('index.html', predictions=predictions_df,
                                   total=total, at_risk=at_risk, safe=safe, user_name=session['user_name'])

        except Exception as e:
            error = f"Error during file processing: {str(e)}"
            return render_template('index.html', predictions=None, error=error, user_name=session['user_name'])

    return render_template('index.html', predictions=None, error=error, user_name=session['user_name'])

@app.route('/download')
def download():
    global predictions_df
    file_path = 'at_risk_customers.xlsx'
    predictions_df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
