from app import app
from models import db

with app.app_context():
    db.create_all()  # This creates the tables for the models
    print("Database tables created.")
