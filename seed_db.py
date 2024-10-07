from app import app
from models import db, Column

with app.app_context():
    # Clear existing data (optional)
    db.session.query(Column).delete()

    # Add initial columns
    columns = ['To Do', 'In Progress', 'Done']
    for column_name in columns:
        column = Column(name=column_name)
        db.session.add(column)

    db.session.commit()
    print("Database seeded with initial columns.")
