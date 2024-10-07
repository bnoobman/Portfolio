from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Task, Column, Board

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
@app.route('/board/<int:board_id>')
def kanban_board(board_id=None):
    # Fetch all boards to display in the sidebar
    boards = Board.query.all()

    # If no board is selected, default to the first board
    if not board_id and boards:
        board_id = boards[0].id

    # Fetch the columns and tasks for the selected board
    columns = Column.query.filter_by(board_id=board_id).all()

    return render_template('kanban.html', boards=boards, columns=columns, selected_board_id=board_id)


@app.route('/create_board', methods=['POST'])
def create_board():
    board_name = request.form['board_name']
    new_board = Board(name=board_name)
    db.session.add(new_board)
    db.session.commit()

    return redirect(url_for('kanban_board'))


@app.route('/add_column/<int:board_id>', methods=['POST'])
def add_column(board_id):
    column_name = request.form['name']

    # Check if the board exists
    board = Board.query.get(board_id)
    if not board:
        return redirect(url_for('kanban_board'))

    # Create a new column for the specified board
    new_column = Column(name=column_name, board_id=board_id)
    db.session.add(new_column)
    db.session.commit()

    # Redirect back to the same board view
    return redirect(url_for('kanban_board', board_id=board_id))


@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    column_id = request.form['column_id']

    # Create the new task in the specified column
    new_task = Task(title=title, column_id=column_id)
    db.session.add(new_task)
    db.session.commit()

    # Get the board id based on the column
    column = Column.query.get(column_id)
    return redirect(url_for('kanban_board', board_id=column.board_id))


@app.route('/move_task/<int:task_id>/<int:column_id>', methods=['POST'])
def move_task(task_id, column_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return {'error': 'Task not found'}, 404

        column = Column.query.get(column_id)
        if not column:
            return {'error': 'Column not found'}, 404

        # Update task's column and save
        task.column_id = column_id
        db.session.commit()

        return {'success': 'Task moved successfully'}, 200

    except Exception as e:
        print(f"Error moving task: {e}")
        return {'error': 'An error occurred while moving the task'}, 500


@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)

        db.session.commit()

        return jsonify({'success': 'Task updated successfully'}), 200

    except Exception as e:
        print(f"Error editing task: {e}")
        return jsonify({'error': 'An error occurred while updating the task'}), 500


if __name__ == '__main__':
    app.run(debug=True)
