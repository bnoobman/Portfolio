from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Board Model: Represents a Kanban Board
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    columns = db.relationship('Column', backref='board', lazy=True)

# Column Model: Represents a Kanban Column
class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)  # Foreign key to Board
    tasks = db.relationship('Task', backref='column', lazy=True)

# Task Model: Represents a Task in a Column
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    column_id = db.Column(db.Integer, db.ForeignKey('column.id'), nullable=False)

