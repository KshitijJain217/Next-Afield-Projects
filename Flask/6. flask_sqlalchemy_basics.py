# ============================================================
# Flask with SQLAlchemy - Learning File
# Topic: Database Integration, Sessions, CRUD Queries
# ============================================================

# SQLAlchemy is an ORM (Object-Relational Mapper).
# It lets us write Python code to interact with databases instead of writing raw SQL queries.
# To run this, you need: pip install Flask-SQLAlchemy

import os
from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ============================================================
# PART 1 - DATABASE CONFIGURATION
# ============================================================

# We will use SQLite because it's built into Python and saves data to a local file.
# No need to install a separate database server (like MySQL or Postgres) for learning!

# Tell Flask where the database file will be saved.
# 'sqlite:///...' means look in the current folder for 'my_database.db'
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'my_database.db')

# Disable a feature we don't need to save memory (it tracks modifications)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension with our app
db = SQLAlchemy(app)


# ============================================================
# PART 2 - DEFINING THE MODEL (A Table in the DB)
# ============================================================

# A "Model" is a Python class that represents a Table in the database.
# Each attribute in the class is a Column in the table.

class Task(db.Model):
    # __tablename__ is optional, but good practice to name your table explicitly
    __tablename__ = 'tasks'

    # 1. Primary Key: A unique ID for every task
    id = db.Column(db.Integer, primary_key=True)
    
    # 2. String Column: The actual task text (max 100 chars), cannot be empty (nullable=False)
    title = db.Column(db.String(100), nullable=False)
    
    # 3. Boolean Column: Is the task done? Defaults to False.
    is_done = db.Column(db.Boolean, default=False)

    # An optional method to make printing objects look nice while debugging
    def __repr__(self):
        return f"<Task {self.id}: {self.title} (Done: {self.is_done})>"


# ============================================================
# PART 3 - INITIALIZING THE DATABASE
# ============================================================

# We need to tell SQLAlchemy to actually create the 'my_database.db' file
# and the 'tasks' table inside it before the app starts.
# We must do this inside an "app context".
with app.app_context():
    # This reads our Models and creates the tables if they don't exist yet.
    db.create_all()


# ============================================================
# PART 4 - THE HTML TEMPLATE
# ============================================================

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask SQLAlchemy To-Do</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        .container { background: white; padding: 20px; border-radius: 8px; max-width: 500px; margin: auto; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h2 { color: #333; }
        .task-list { list-style-type: none; padding: 0; }
        .task-item { padding: 10px; border-bottom: 1px solid #ddd; display: flex; justify-content: space-between; align-items: center; }
        .done { text-decoration: line-through; color: #888; }
        input[type="text"] { width: 70%; padding: 8px; }
        button { padding: 8px 15px; background: #28a745; color: white; border: none; cursor: pointer; border-radius: 4px; }
        .btn-delete { background: #dc3545; color: white; text-decoration: none; padding: 5px 10px; border-radius: 3px; font-size: 12px;}
        .btn-toggle { background: #ffc107; color: black; text-decoration: none; padding: 5px 10px; border-radius: 3px; font-size: 12px; margin-right: 5px;}
        .stats { margin-top: 20px; font-size: 0.9em; color: #555; background: #e9ecef; padding: 10px; border-radius: 4px; }
    </style>
</head>
<body>

<div class="container">
    <h2>📝 Task Manager (SQLAlchemy)</h2>
    
    <!-- Form to CREATE a new task -->
    <form method="POST" action="/add">
        <input type="text" name="title" placeholder="What needs to be done?" required>
        <button type="submit">Add Task</button>
    </form>

    <ul class="task-list">
        <!-- Loop through the tasks passed from the route -->
        {% for task in tasks %}
            <li class="task-item">
                <!-- Apply a CSS class if task.is_done is True -->
                <span class="{% if task.is_done %}done{% endif %}">
                    {{ task.id }}. {{ task.title }}
                </span>
                
                <div>
                    <!-- UPDATE route link -->
                    <a href="/toggle/{{ task.id }}" class="btn-toggle">Toggle Status</a>
                    <!-- DELETE route link -->
                    <a href="/delete/{{ task.id }}" class="btn-delete">Delete</a>
                </div>
            </li>
        {% else %}
            <li class="task-item">No tasks yet. Add one above!</li>
        {% endfor %}
    </ul>

    <!-- Displaying some custom query results -->
    <div class="stats">
        <strong>Database Stats:</strong><br>
        Total Tasks: {{ total_count }} <br>
        Pending Tasks: {{ pending_count }} <br>
        Completed Tasks: {{ completed_count }}
    </div>
</div>

</body>
</html>
"""

# ============================================================
# PART 5 - ROUTES & QUERY PATTERNS (CRUD Operations)
# ============================================================

# --- 1. READ (Querying Data) ---
@app.route('/')
def index():
    # QUERY PATTERN 1: Get ALL records
    # SELECT * FROM tasks;
    all_tasks = Task.query.all()
    
    # QUERY PATTERN 2: Count records
    # SELECT count(id) FROM tasks;
    total_count = Task.query.count()
    
    # QUERY PATTERN 3: Filtering (using filter_by for exact matches)
    # SELECT count(id) FROM tasks WHERE is_done = False;
    pending_count = Task.query.filter_by(is_done=False).count()
    completed_count = Task.query.filter_by(is_done=True).count()
    
    # (Advanced Note: `filter()` is used for complex conditions like >, <, etc.
    # e.g., Task.query.filter(Task.id > 5).all() - but we stick to basics here)

    return render_template_string(
        TEMPLATE, 
        tasks=all_tasks, 
        total_count=total_count,
        pending_count=pending_count,
        completed_count=completed_count
    )


# --- 2. CREATE (Adding Data) ---
@app.route('/add', methods=['POST'])
def add_task():
    task_title = request.form.get('title')
    
    if task_title:
        # Step A: Create a new Python object representing our row
        new_task = Task(title=task_title)
        
        # Step B: Add the object to the Database "Session" (staging area)
        db.session.add(new_task)
        
        # Step C: Commit the session to save it to the actual database file
        # If you forget to commit, data will NOT be saved!
        db.session.commit()
        
    return redirect(url_for('index'))


# --- 3. UPDATE (Modifying Data) ---
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    # QUERY PATTERN 4: Fetch a single record by its Primary Key (ID)
    # SELECT * FROM tasks WHERE id = <task_id>;
    # .get_or_404() is amazing: it automatically returns a 404 Error page if the ID doesn't exist!
    task = Task.query.get_or_404(task_id)
    
    # Step A: Change the Python object's attribute
    # Toggle boolean (True becomes False, False becomes True)
    task.is_done = not task.is_done
    
    # Step B: Commit the session. 
    # Notice we don't need db.session.add() for updates! 
    # SQLAlchemy knows this object came from the DB and was modified.
    db.session.commit()
    
    return redirect(url_for('index'))


# --- 4. DELETE (Removing Data) ---
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # Step A: Fetch the record we want to delete
    task = Task.query.get_or_404(task_id)
    
    # Step B: Tell the session to delete it
    db.session.delete(task)
    
    # Step C: Commit the change to the database
    db.session.commit()
    
    return redirect(url_for('index'))


# ============================================================
# Running the App
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)

# ============================================================
# QUICK RECAP - What I learned in this file:
# ============================================================
#
# 1. SETUP:
#    `app.config['SQLALCHEMY_DATABASE_URI']` points to the database file.
#    `db = SQLAlchemy(app)` connects the app and the database.
#
# 2. MODELS:
#    Classes that inherit from `db.Model`.
#    They define tables, and attributes (`db.Column`) define the columns.
#    `db.create_all()` actually builds the tables.
#
# 3. THE DB SESSION (`db.session`):
#    Think of it as a staging area or "shopping cart" for database changes.
#    - `db.session.add(obj)` puts a new row in the cart.
#    - `db.session.delete(obj)` puts a deletion request in the cart.
#    - `db.session.commit()` "checks out" and actually executes the SQL to save changes.
#
# 4. BASIC QUERY PATTERNS (CRUD):
#    - Create: `obj = Model(name='x')` -> `session.add(obj)` -> `commit()`
#    - Read All: `Model.query.all()`
#    - Read One by ID: `Model.query.get_or_404(id)`
#    - Read with Filters: `Model.query.filter_by(column=value).all()`
#    - Update: `obj = query.get(id)` -> `obj.name = 'y'` -> `commit()`
#    - Delete: `obj = query.get(id)` -> `session.delete(obj)` -> `commit()`
# ============================================================
