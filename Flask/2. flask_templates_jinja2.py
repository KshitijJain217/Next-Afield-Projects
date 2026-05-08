# ============================================================
# Flask Templates & Jinja2 - Learning File
# Topic: Jinja2 Syntax, Template Inheritance, Passing Data
# ============================================================

# Jinja2 is the templating engine Flask uses by default
# It lets us mix Python-like logic inside HTML
# render_template_string() = render HTML written as a Python string
# render_template() = render HTML from a separate .html file (we'll use strings here)

from flask import Flask, render_template_string, request

app = Flask(__name__)


# ============================================================
# JINJA2 SYNTAX CHEATSHEET (as comments, refer anytime!)
# ============================================================
#
# {{ variable }}         -> Output a variable value
# {% if condition %}     -> Start an if block
# {% for item in list %} -> Loop through a list
# {# This is a comment #} -> Jinja2 comment (not shown in HTML)
# {{ variable | filter }} -> Apply a filter to a variable
#
# Common filters:
# {{ name | upper }}     -> UPPERCASE
# {{ name | lower }}     -> lowercase
# {{ name | title }}     -> Title Case
# {{ name | length }}    -> count characters
# {{ list | join(", ") }} -> join list items
# {{ price | round(2) }} -> round a number
# ============================================================


# ============================================================
# PART 1 - BASE TEMPLATE (simulating template inheritance)
# ============================================================

# In real Flask projects, we'd have a base.html file
# All other pages "extend" it so we don't repeat navbar/footer HTML
# Here we define it as a Python string to keep everything in one file

# Think of this as the "master layout" for the whole website
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Flask Site{% endblock %}</title>
    <style>
        /* Simple styling so it looks decent */
        body { font-family: Arial, sans-serif; margin: 0; background: #f4f4f4; }
        nav { background: #333; padding: 10px 20px; }
        nav a { color: white; margin-right: 15px; text-decoration: none; }
        nav a:hover { text-decoration: underline; }
        .container { padding: 20px 40px; }
        .card { background: white; padding: 20px; margin: 10px 0;
                border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        footer { background: #333; color: white; text-align: center;
                 padding: 10px; margin-top: 30px; }
        h1 { color: #333; }
        .badge { background: #007bff; color: white; padding: 2px 8px;
                 border-radius: 10px; font-size: 12px; }
        .alert { background: #fff3cd; border: 1px solid #ffc107;
                 padding: 10px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>

    <!-- This navbar appears on EVERY page that uses this base template -->
    <nav>
        <a href="/">Home</a>
        <a href="/students">Students List</a>
        <a href="/profile/Alice">Profile Example</a>
        <a href="/filters-demo">Filters Demo</a>
        <a href="/form-demo">Form Demo</a>
    </nav>

    <div class="container">
        <!-- {% block content %} is a placeholder -->
        <!-- Child templates fill this block with their own content -->
        {% block content %}
        <!-- Default content if child doesn't override this block -->
        <p>No content provided.</p>
        {% endblock %}
    </div>

    <footer>
        <!-- {% block footer %} lets child templates change the footer too -->
        {% block footer %}
        <p>Made while learning Flask 🚀 | Jinja2 Templates</p>
        {% endblock %}
    </footer>

</body>
</html>
"""

# ============================================================
# HOW INHERITANCE WORKS (concept explanation):
# ============================================================
# BASE_TEMPLATE has "blocks" like {% block content %}{% endblock %}
# A child template does {% extends "base.html" %} then fills those blocks
# We simulate this below using Jinja2's environment directly
# ============================================================


# ============================================================
# PART 2 - Passing Simple Variables to Templates
# ============================================================

# Child template that "fills" the blocks from BASE_TEMPLATE
HOME_PAGE = BASE_TEMPLATE.replace(
    "{% block title %}My Flask Site{% endblock %}",
    "{% block title %}Home - Flask Learning{% endblock %}"
).replace(
    "{% block content %}\n        <!-- Default content if child doesn't override this block -->\n        <p>No content provided.</p>\n        {% endblock %}",
    """{% block content %}
        <div class="card">
            <h1>Welcome, {{ username }}! 👋</h1>

            {# This is a Jinja2 comment - it won't appear in browser source #}

            <!-- Jinja2 if/else - checks if user is logged in -->
            {% if is_logged_in %}
                <p class="badge">✅ Logged In</p>
                <p>Great to see you, <strong>{{ username }}</strong>!</p>
            {% else %}
                <p class="alert">You are not logged in. Please sign in.</p>
            {% endif %}

            <p>You have <strong>{{ message_count }}</strong> new messages.</p>
        </div>
        {% endblock %}"""
)


@app.route("/")
def home():
    # Passing data as keyword arguments to the template
    # Each variable name here maps to {{ variable }} in the HTML
    return render_template_string(
        HOME_PAGE,
        username="Kshitij",       # passed as {{ username }}
        is_logged_in=True,         # passed as {{ is_logged_in }}
        message_count=5            # passed as {{ message_count }}
    )


# ============================================================
# PART 3 - Passing Lists and Looping with {% for %}
# ============================================================

STUDENTS_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Students List</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th { background: #333; color: white; padding: 10px; }
        td { padding: 10px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f0f0f0; }
        h1 { color: #333; }
        nav a { margin-right: 15px; color: #007bff; }
    </style>
</head>
<body>
    <nav><a href="/">← Back to Home</a></nav>
    <h1>Students List</h1>

    <!-- Showing total count using Jinja2 length filter -->
    <p>Total students: <strong>{{ students | length }}</strong></p>

    <!-- {% for %} loop goes through each item in the list -->
    <table>
        <tr>
            <th>#</th>
            <th>Name</th>
            <th>Age</th>
            <th>Grade</th>
            <th>Status</th>
        </tr>

        <!-- loop.index gives us the current loop number (starts at 1) -->
        <!-- loop.first and loop.last are also useful -->
        {% for student in students %}
        <tr>
            <td>{{ loop.index }}</td>

            <!-- | title filter makes first letter of each word uppercase -->
            <td>{{ student.name | title }}</td>
            <td>{{ student.age }}</td>
            <td>{{ student.grade }}</td>

            <!-- Inline if/else using Jinja2 ternary style -->
            <td>{{ "✅ Pass" if student.grade >= "C" else "❌ Fail" }}</td>
        </tr>
        {% else %}
            <!-- {% else %} on for loop runs if list is empty -->
            <tr><td colspan="5">No students found!</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""


@app.route("/students")
def students():
    # Passing a list of dictionaries to the template
    # Each dict is one student's data
    student_list = [
        {"name": "alice johnson",  "age": 20, "grade": "A"},
        {"name": "bob smith",      "age": 22, "grade": "B"},
        {"name": "charlie brown",  "age": 19, "grade": "C"},
        {"name": "diana prince",   "age": 21, "grade": "A"},
        {"name": "edward norton",  "age": 23, "grade": "D"},  # will show Fail
    ]

    # 'students' in render_template_string maps to {{ students }} in HTML
    return render_template_string(STUDENTS_PAGE, students=student_list)


# ============================================================
# PART 4 - Passing Dictionaries (Accessing with dot notation)
# ============================================================

PROFILE_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ user.name }}'s Profile</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 30px; background: #f4f4f4; }
        .card { background: white; padding: 25px; border-radius: 8px;
                max-width: 400px; box-shadow: 0 3px 8px rgba(0,0,0,0.1); }
        .tag { background: #e0e0e0; padding: 3px 10px; border-radius: 12px;
               margin: 3px; display: inline-block; font-size: 13px; }
        nav a { color: #007bff; }
    </style>
</head>
<body>
    <nav><a href="/">← Home</a></nav>
    <br>
    <div class="card">
        <h2>👤 {{ user.name | upper }}</h2>  {# name in ALL CAPS using filter #}

        <!-- Accessing dictionary values with dot notation in Jinja2 -->
        <p><b>Email:</b> {{ user.email }}</p>
        <p><b>Age:</b> {{ user.age }}</p>
        <p><b>City:</b> {{ user.city }}</p>
        <p><b>Member since:</b> {{ user.joined }}</p>

        <!-- Checking if a key exists in the dict -->
        {% if user.bio %}
            <p><b>Bio:</b> {{ user.bio }}</p>
        {% else %}
            <p><em>No bio added yet.</em></p>
        {% endif %}

        <p><b>Skills:</b><br>
        <!-- Looping through a list inside a dictionary -->
        {% for skill in user.skills %}
            <span class="tag">{{ skill }}</span>
        {% endfor %}
        </p>
    </div>
</body>
</html>
"""


# URL takes a name so we can show different profiles
@app.route("/profile/<name>")
def profile(name):
    # Simulating fetching user data based on name
    # In real apps, this would come from a database
    user_data = {
        "name": name,
        "email": f"{name.lower()}@example.com",
        "age": 21,
        "city": "Mumbai",
        "joined": "January 2024",
        "bio": f"Hi! I'm {name} and I'm learning Flask.",
        "skills": ["Python", "Flask", "HTML", "Jinja2"]
    }

    # Passing the whole dictionary as one variable
    return render_template_string(PROFILE_PAGE, user=user_data)


# ============================================================
# PART 5 - Jinja2 Filters Demo
# ============================================================

FILTERS_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Jinja2 Filters</title>
    <style>
        body { font-family: monospace; padding: 20px; background: #1e1e1e; color: #d4d4d4; }
        .row { margin: 8px 0; }
        .label { color: #9cdcfe; display: inline-block; width: 220px; }
        .value { color: #ce9178; }
        h1 { color: #569cd6; }
        nav a { color: #4fc1ff; }
    </style>
</head>
<body>
    <nav><a href="/">← Home</a></nav>
    <h1>🔧 Jinja2 Filters Playground</h1>

    <div class="row"><span class="label">Original text:</span>
        <span class="value">{{ text }}</span></div>

    <div class="row"><span class="label">| upper :</span>
        <span class="value">{{ text | upper }}</span></div>

    <div class="row"><span class="label">| lower :</span>
        <span class="value">{{ text | lower }}</span></div>

    <div class="row"><span class="label">| title :</span>
        <span class="value">{{ text | title }}</span></div>

    <div class="row"><span class="label">| length :</span>
        <span class="value">{{ text | length }} characters</span></div>

    <div class="row"><span class="label">| reverse :</span>
        <span class="value">{{ text | reverse }}</span></div>

    <div class="row"><span class="label">| truncate(15) :</span>
        <span class="value">{{ text | truncate(15) }}</span></div>

    <hr style="border-color: #555">
    <h2 style="color: #569cd6">Number Filters</h2>

    <div class="row"><span class="label">Original price:</span>
        <span class="value">{{ price }}</span></div>

    <div class="row"><span class="label">| round(2) :</span>
        <span class="value">{{ price | round(2) }}</span></div>

    <div class="row"><span class="label">| int :</span>
        <span class="value">{{ price | int }}</span></div>

    <hr style="border-color: #555">
    <h2 style="color: #569cd6">List Filters</h2>

    <div class="row"><span class="label">Original list:</span>
        <span class="value">{{ fruits }}</span></div>

    <div class="row"><span class="label">| join(", ") :</span>
        <span class="value">{{ fruits | join(", ") }}</span></div>

    <div class="row"><span class="label">| sort :</span>
        <span class="value">{{ fruits | sort }}</span></div>

    <div class="row"><span class="label">| first :</span>
        <span class="value">{{ fruits | first }}</span></div>

    <div class="row"><span class="label">| last :</span>
        <span class="value">{{ fruits | last }}</span></div>

    <div class="row"><span class="label">| length :</span>
        <span class="value">{{ fruits | length }} items</span></div>

    <div class="row"><span class="label">| reverse :</span>
        <span class="value">{{ fruits | list | reverse | list }}</span></div>

</body>
</html>
"""


@app.route("/filters-demo")
def filters_demo():
    return render_template_string(
        FILTERS_PAGE,
        text="hello flask world",
        price=199.9567,
        fruits=["Mango", "Apple", "Banana", "Cherry", "Grapes"]
    )


# ============================================================
# PART 6 - Passing Form Data Back to Template
# ============================================================

FORM_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Form with Jinja2</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 30px; background: #f4f4f4; }
        form { background: white; padding: 20px; border-radius: 8px;
               max-width: 400px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        input, select { width: 100%; padding: 8px; margin: 8px 0 15px;
                         box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #333; color: white; padding: 10px 20px;
                 border: none; border-radius: 4px; cursor: pointer; }
        .result { background: white; padding: 20px; border-radius: 8px;
                  margin-top: 20px; max-width: 400px;
                  box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        nav a { color: #007bff; }
    </style>
</head>
<body>
    <nav><a href="/">← Home</a></nav>
    <h2>📋 Student Registration Form</h2>

    <form method="POST">
        <label>Name:</label>
        <!-- value="{{ form_data.name or '' }}" keeps the value after form submit -->
        <input type="text" name="name" value="{{ form_data.name or '' }}" placeholder="Enter name">

        <label>Age:</label>
        <input type="number" name="age" value="{{ form_data.age or '' }}" placeholder="Enter age">

        <label>Course:</label>
        <select name="course">
            <!-- Jinja2 sets the selected option based on what was submitted -->
            {% for c in courses %}
                <option value="{{ c }}"
                    {% if form_data.course == c %}selected{% endif %}>
                    {{ c }}
                </option>
            {% endfor %}
        </select>

        <button type="submit">Submit</button>
    </form>

    <!-- Only show result block if form was submitted (POST) -->
    {% if submitted %}
    <div class="result">
        <h3>✅ Registered Successfully!</h3>
        <p><b>Name:</b> {{ form_data.name | title }}</p>
        <p><b>Age:</b> {{ form_data.age }}</p>
        <p><b>Course:</b> {{ form_data.course }}</p>
        <p><b>Category:</b>
            <!-- Inline conditional using 'if' expression -->
            {{ "🧒 Junior (under 20)" if form_data.age | int < 20 else "🧑 Senior (20+)" }}
        </p>
    </div>
    {% endif %}

</body>
</html>
"""


@app.route("/form-demo", methods=["GET", "POST"])
def form_demo():
    # List of courses to show in dropdown - passed to template
    courses = ["Python Basics", "Flask Development", "Data Science", "Web Design"]

    # form_data will store whatever was submitted (or empty dict for fresh page)
    form_data = {}
    submitted = False

    if request.method == "POST":
        # Collect all form fields into a dictionary
        form_data = {
            "name": request.form.get("name", ""),
            "age": request.form.get("age", ""),
            "course": request.form.get("course", "")
        }
        submitted = True  # flag to tell template to show result block

    return render_template_string(
        FORM_PAGE,
        courses=courses,
        form_data=form_data,     # pass dict to template
        submitted=submitted       # pass boolean flag
    )


# ============================================================
# Running the App
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)


# ============================================================
# QUICK RECAP - What I learned in this file:
# ============================================================
#
# JINJA2 SYNTAX:
# {{ var }}              -> display a variable
# {% if %}{% endif %}    -> conditional block
# {% for x in list %}{% endfor %} -> loop
# {# comment #}          -> template comment (hidden from browser)
#
# PASSING DATA:
# render_template_string(HTML, var1=value1, var2=value2)
# - strings, integers, booleans, lists, dicts all work
# - access dict keys with dot: {{ user.name }}
# - access list index: {{ items[0] }}
#
# USEFUL FILTERS:
# | upper | lower | title | length | reverse
# | round(n) | int | truncate(n) | join(", ")
# | sort | first | last
#
# TEMPLATE INHERITANCE CONCEPT:
# - Base template has {% block name %}{% endblock %} placeholders
# - Child templates use {% extends "base.html" %} and fill blocks
# - Avoids repeating navbar/footer HTML on every page
# - In real Flask: use render_template() + separate .html files
# - Here: we simulate it by composing Python strings (same idea!)
#
# ROUTES IN THIS FILE:
# GET      /                -> home with variables
# GET      /students        -> list loop demo
# GET/POST /profile/<name>  -> dict access demo
# GET      /filters-demo    -> all filters playground
# GET/POST /form-demo       -> form + Jinja2 conditionals
# ============================================================
