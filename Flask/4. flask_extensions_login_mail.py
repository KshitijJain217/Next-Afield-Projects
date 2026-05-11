# ============================================================
# Flask Extensions - Learning File
# Topic: Flask-Login & Flask-Mail
# ============================================================

# Flask is small by design. For big features like authentication or sending emails,
# we use "extensions".
# To run this, you need: pip install Flask-Login Flask-Mail Flask-SQLAlchemy

import os
from flask import Flask, render_template_string, request, redirect, url_for, flash
# SQLAlchemy for our database (Users need to be saved somewhere!)
from flask_sqlalchemy import SQLAlchemy
# Flask-Login imports
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# Flask-Mail imports
from flask_mail import Mail, Message

app = Flask(__name__)

# ============================================================
# PART 1 - CONFIGURATION
# ============================================================

# Secret key is REQUIRED for Flask-Login (it uses sessions securely)
app.config['SECRET_KEY'] = 'super-secret-key-for-learning'

# Database config (using SQLite again)
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Mail config
# For learning, we will just use a dummy configuration.
# In a real app, you would put your Gmail/SMTP server details here.
# By setting MAIL_SUPPRESS_SEND = True, Flask-Mail pretends to send it
# but doesn't actually try to connect to a real server (great for testing!)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
app.config['MAIL_SUPPRESS_SEND'] = True # <--- Crucial for testing without real credentials!


# ============================================================
# PART 2 - INITIALIZING EXTENSIONS
# ============================================================

# 1. Initialize Database
db = SQLAlchemy(app)

# 2. Initialize Flask-Mail
mail = Mail(app)

# 3. Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Tell Flask-Login which route to redirect to if a non-logged-in user
# tries to visit a protected page.
login_manager.login_view = 'login' 
login_manager.login_message = "Please log in to access this page."


# ============================================================
# PART 3 - USER MODEL & LOGIN MANAGER SETUP
# ============================================================

# UserMixin gives our class default implementations for Flask-Login methods
# like is_authenticated, is_active, is_anonymous, and get_id().
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # In a real app, NEVER store plain text passwords! Always hash them.
    # We use plain text here ONLY for beginner learning purposes.
    password = db.Column(db.String(50), nullable=False)

# The user_loader callback tells Flask-Login how to load a user from the database
# based on the user ID stored in the session cookie.
@login_manager.user_loader
def load_user(user_id):
    # This runs behind the scenes on every request if a user is logged in
    return User.query.get(int(user_id))


# Create the database and a dummy user for us to test with
with app.app_context():
    db.create_all()
    # Check if we already created our test user
    if not User.query.filter_by(username='admin').first():
        test_user = User(username='admin', password='password123')
        db.session.add(test_user)
        db.session.commit()


# ============================================================
# PART 4 - HTML TEMPLATE
# ============================================================

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Extensions</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        .container { background: white; padding: 20px; border-radius: 8px; max-width: 500px; margin: auto; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .alert { background: #fff3cd; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ffeeba; color: #856404; }
        .success { background: #d4edda; border-color: #c3e6cb; color: #155724; }
        input { width: 90%; padding: 8px; margin-bottom: 10px; }
        button { background: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
        .logout-btn { background: #dc3545; }
        .mail-btn { background: #28a745; margin-top: 15px;}
        nav { margin-bottom: 20px; }
        nav a { margin-right: 15px; color: #007bff; text-decoration: none; }
    </style>
</head>
<body>

<div class="container">
    <nav>
        <a href="/">🏠 Home</a>
        <a href="/dashboard">🔒 Dashboard (Protected)</a>
        
        <!-- current_user is provided by Flask-Login in templates automatically! -->
        {% if current_user.is_authenticated %}
            <a href="/logout" style="color: red;">Log Out</a>
        {% else %}
            <a href="/login">Log In</a>
        {% endif %}
    </nav>

    <!-- Displaying Flash messages (like errors or success alerts) -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert {% if category == 'success' %}success{% endif %}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
</div>

</body>
</html>
"""

# Small helper to format templates inside the file
def render_page(content_html):
    final_html = TEMPLATE.replace('{% block content %}{% endblock %}', content_html)
    return render_template_string(final_html)


# ============================================================
# PART 5 - ROUTES
# ============================================================

@app.route('/')
def home():
    if current_user.is_authenticated:
        content = f"<h2>Welcome back, {current_user.username}!</h2><p>You are logged in.</p>"
    else:
        content = "<h2>Welcome Guest!</h2><p>You are NOT logged in. Try visiting the Dashboard.</p>"
    
    return render_page(content)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, no need to show login page
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 1. Look up user by username
        user = User.query.filter_by(username=username).first()

        # 2. Check if user exists and password matches (Remember: never do plain text checks in production)
        if user and user.password == password:
            # 3. MAGIC HAPPENS HERE: login_user() logs them in and creates the session!
            login_user(user)
            flash('Logged in successfully.', 'success')
            
            # If they tried to visit a protected page before logging in, Flask-Login saved that URL.
            # We can redirect them back to it!
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    # HTML for the login form
    form_html = """
        <h2>Login</h2>
        <p><em>Hint: Use <b>admin</b> / <b>password123</b></em></p>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    """
    return render_page(form_html)


@app.route('/logout')
@login_required # Cannot log out if not logged in!
def logout():
    # MAGIC HAPPENS HERE: Clears the session cookie
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


# The @login_required decorator is awesome. 
# If a non-logged-in user tries to visit /dashboard, 
# it intercepts them and sends them to the login page automatically!
@app.route('/dashboard')
@login_required
def dashboard():
    content = f"""
        <h2>🔒 Secret Dashboard</h2>
        <p>Hello <b>{current_user.username}</b>!</p>
        <p>Only logged-in users can see this page.</p>
        
        <hr>
        <h3>Flask-Mail Demo</h3>
        <p>Clicking this button will simulate sending an email.</p>
        <form action="/send-email" method="POST">
            <button type="submit" class="mail-btn">✉️ Send Welcome Email</button>
        </form>
    """
    return render_page(content)


@app.route('/send-email', methods=['POST'])
@login_required
def send_email():
    # 1. Create a Message object
    # sender comes from MAIL_DEFAULT_SENDER config
    msg = Message(
        subject="Welcome to Flask Extensions!",
        recipients=["test-user@example.com"], # Who receives it
        body=f"Hello {current_user.username},\n\nThis is a test email sent using Flask-Mail!"
    )
    
    # 2. Send the message
    # Because MAIL_SUPPRESS_SEND=True, it won't actually send over the internet,
    # but the code executes as if it did.
    mail.send(msg)
    
    flash('Email was "sent" successfully! (Check console for dummy output if configured)', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)

# ============================================================
# QUICK RECAP - What I learned in this file:
# ============================================================
#
# FLASK-LOGIN:
# 1. `LoginManager(app)` sets it up.
# 2. `UserMixin` gives your Database Model the required methods.
# 3. `@login_manager.user_loader` tells Flask-Login how to find a user by ID.
# 4. `login_user(user)` logs them in.
# 5. `logout_user()` logs them out.
# 6. `@login_required` protects routes (redirects to login if not logged in).
# 7. `current_user` is a magic variable available in routes AND templates!
#
# FLASK-MAIL:
# 1. `Mail(app)` sets it up.
# 2. Needs configuration (SERVER, PORT, USERNAME, PASSWORD).
# 3. `MAIL_SUPPRESS_SEND = True` is great for testing without real credentials.
# 4. Create a `Message(subject, recipients, body)`.
# 5. Call `mail.send(msg)`.
# ============================================================
