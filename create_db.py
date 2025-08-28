from app import db, app

# Use the app context to allow SQLAlchemy to interact with Flask's app
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
