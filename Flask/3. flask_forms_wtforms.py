# ============================================================
# Flask Forms & Validation - Learning File
# Topic: WTForms, CSRF Protection, Form Validation
# ============================================================

# To run this, you need to install Flask-WTF and an email validator:
# pip install Flask-WTF email-validator

from flask import Flask, render_template_string, request, redirect, url_for
# Import FlaskForm as the base class for our forms
from flask_wtf import FlaskForm
# Import the specific fields we need for our form
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField
# Import validators to check if the user input is correct
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo

app = Flask(__name__)

# ============================================================
# PART 1 - SECRET KEY & CSRF PROTECTION
# ============================================================
# CSRF (Cross-Site Request Forgery) is a common security attack.
# Flask-WTF automatically protects us against it, BUT it needs a secret key.
# This key is used to generate secure tokens for our forms.
# NEVER share this key in a real project!
app.config['SECRET_KEY'] = 'my_super_secret_beginner_key_123'


# ============================================================
# PART 2 - DEFINING THE FORM CLASS
# ============================================================
# Instead of writing raw HTML forms, we define our form as a Python class.
# This makes validation and rendering much easier.

class RegistrationForm(FlaskForm):
    # Each attribute is a field in the form.
    # The first argument is the label (what the user sees).
    # 'validators' is a list of rules the input must pass.
    
    # DataRequired() means this field cannot be empty.
    # Length(min, max) enforces the character count.
    username = StringField('Username', validators=[
        DataRequired(message="Please enter a username."),
        Length(min=4, max=20, message="Username must be between 4 and 20 characters.")
    ])
    
    # Email() checks if it looks like a valid email address.
    email = StringField('Email Address', validators=[
        DataRequired(),
        Email(message="Invalid email format.")
    ])
    
    # NumberRange() ensures the number falls within specific bounds.
    age = IntegerField('Age', validators=[
        DataRequired(message="Age is required."),
        NumberRange(min=18, max=120, message="You must be at least 18 years old.")
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    
    # EqualTo() checks if this field matches another field (like password confirmation).
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    
    # A simple checkbox
    accept_terms = BooleanField('I accept the Terms and Conditions', validators=[
        DataRequired(message="You must accept the terms to register.")
    ])
    
    submit = SubmitField('Sign Up')


# ============================================================
# PART 3 - THE HTML TEMPLATE
# ============================================================
# We use Jinja2 to render the form fields defined in our Python class.
# We also use it to display any validation errors if the user messed up.

FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>WTForms Registration</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        .form-container { background: white; padding: 30px; border-radius: 8px; max-width: 500px; margin: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        label { font-weight: bold; display: block; margin-bottom: 5px; }
        input[type="text"], input[type="password"], input[type="number"] { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        .error { color: red; font-size: 0.85em; margin-top: 5px; display: block; }
        .btn { background: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 16px; width: 100%; }
        .btn:hover { background: #218838; }
        .success-box { background: #d4edda; color: #155724; padding: 15px; border-radius: 4px; border: 1px solid #c3e6cb; margin-bottom: 20px; }
    </style>
</head>
<body>

<div class="form-container">
    <h2>Create an Account</h2>
    
    <!-- We can pass a success message to the template -->
    {% if success_message %}
        <div class="success-box">
            {{ success_message }}
        </div>
    {% endif %}

    <!-- IMPORTANT: method="POST" and action="" (submits to the same route) -->
    <!-- novalidate disables the browser's default HTML5 validation, so we can see our Flask validation in action -->
    <form method="POST" action="" novalidate>
        
        <!-- THIS IS CRITICAL FOR CSRF PROTECTION -->
        <!-- Flask-WTF creates a hidden input field with a secure token -->
        {{ form.hidden_tag() }}
        
        <!-- Username Field -->
        <div class="form-group">
            {{ form.username.label }}
            <!-- Rendering the input field itself -->
            {{ form.username() }}
            <!-- Checking for errors -->
            {% if form.username.errors %}
                {% for error in form.username.errors %}
                    <span class="error">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </div>
        
        <!-- Email Field -->
        <div class="form-group">
            {{ form.email.label }}
            {{ form.email() }}
            {% if form.email.errors %}
                {% for error in form.email.errors %}
                    <span class="error">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </div>
        
        <!-- Age Field -->
        <div class="form-group">
            {{ form.age.label }}
            {{ form.age() }}
            {% if form.age.errors %}
                {% for error in form.age.errors %}
                    <span class="error">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </div>
        
        <!-- Password Field -->
        <div class="form-group">
            {{ form.password.label }}
            {{ form.password() }}
            {% if form.password.errors %}
                {% for error in form.password.errors %}
                    <span class="error">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </div>
        
        <!-- Confirm Password Field -->
        <div class="form-group">
            {{ form.confirm_password.label }}
            {{ form.confirm_password() }}
            {% if form.confirm_password.errors %}
                {% for error in form.confirm_password.errors %}
                    <span class="error">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </div>
        
        <!-- Accept Terms Checkbox -->
        <div class="form-group">
            {{ form.accept_terms() }} {{ form.accept_terms.label }}
            {% if form.accept_terms.errors %}
                {% for error in form.accept_terms.errors %}
                    <span class="error">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </div>

        <!-- Submit Button -->
        {{ form.submit(class="btn") }}
        
    </form>
</div>

</body>
</html>
"""

# ============================================================
# PART 4 - HANDLING THE ROUTE
# ============================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 1. Create an instance of our form class
    form = RegistrationForm()
    success_message = None

    # 2. validate_on_submit() is the magic method!
    # It checks two things:
    #   a) Is it a POST request? (Did they click submit?)
    #   b) Is all the data valid according to the rules we defined in our class?
    if form.validate_on_submit():
        # If we get here, the form was submitted AND passed all checks!
        
        # We can access the cleaned, valid data like this:
        username = form.username.data
        email = form.email.data
        
        # In a real app, we would save this to a database here.
        # For now, we'll just show a success message.
        success_message = f"Registration successful for {username} ({email})!"
        
        # Optional: We could clear the form after success by creating a fresh one
        # form = RegistrationForm(formdata=None)

    # 3. Render the template.
    # If it's a GET request, it shows an empty form.
    # If it's a POST request that FAILED validation, it shows the form WITH error messages.
    return render_template_string(FORM_TEMPLATE, form=form, success_message=success_message)


# Adding a simple home route to point to the registration page
@app.route('/')
def home():
    return '<a href="/register">Go to Registration Page</a>'


if __name__ == '__main__':
    app.run(debug=True)

# ============================================================
# QUICK RECAP - What I learned in this file:
# ============================================================
#
# 1. SECRET_KEY:
#    Flask needs `app.config['SECRET_KEY']` to enable CSRF protection.
#
# 2. FLASK-WTF (WTForms):
#    Instead of writing raw HTML <input> tags, we create a Python class
#    that inherits from `FlaskForm`.
#
# 3. FIELDS & VALIDATORS:
#    - Fields like `StringField`, `PasswordField` define the input type.
#    - `validators=[...]` is a list of rules (e.g., `DataRequired()`, `Length()`).
#    - If rules are broken, WTForms automatically generates error messages.
#
# 4. CSRF TOKEN IN HTML:
#    We MUST include `{{ form.hidden_tag() }}` inside our HTML `<form>`
#    to render the hidden security token.
#
# 5. RENDERING FIELDS & ERRORS:
#    - `{{ form.field_name.label }}` -> Renders the `<label>`
#    - `{{ form.field_name() }}` -> Renders the `<input>`
#    - `form.field_name.errors` -> A list of error messages to loop through.
#
# 6. HANDLING SUBMISSION:
#    `if form.validate_on_submit():` does all the heavy lifting.
#    It checks if it's a POST request AND if the data passed validation.
#
# ROUTES IN THIS FILE:
# GET       /           -> Link to register
# GET/POST  /register   -> The WTForms registration form
# ============================================================
