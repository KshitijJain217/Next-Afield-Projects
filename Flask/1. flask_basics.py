# ============================================================
# Flask Basics - Learning File
# Topic: Setup, Routing, Views, Request/Response
# ============================================================

# Flask is a lightweight web framework for Python
# It helps us create web apps and APIs easily
# We install it with: pip install flask

from flask import Flask, request, render_template_string

# Creating the Flask app
# __name__ tells Flask where to look for resources (templates, static files etc.)
app = Flask(__name__)


# ============================================================
# PART 1 - Basic Route (Homepage)
# ============================================================

# A "route" connects a URL to a Python function
# When someone visits "/" (homepage), this function runs
@app.route("/")
def home():
    # This is called a "view function" - it returns what the user sees
    return "Hello! Welcome to my first Flask app 🎉"


# ============================================================
# PART 2 - Multiple Routes (Different Pages)
# ============================================================

# Each URL can have its own route and function
@app.route("/about")
def about():
    # Returning plain text for now, we'll use HTML later
    return "This is the About page. I'm learning Flask!"


@app.route("/contact")
def contact():
    return "Contact me at: learner@example.com"


# ============================================================
# PART 3 - Dynamic Routes (URL with Variables)
# ============================================================

# Sometimes we want the URL itself to carry data
# Like /user/John should greet John
# <name> is a variable part of the URL
@app.route("/user/<name>")
def greet_user(name):
    # Flask passes the URL variable as a function argument
    return f"Hello, {name}! Nice to meet you 👋"


# We can also specify the type of variable
# <int:number> means Flask will only accept a number here
@app.route("/square/<int:number>")
def square(number):
    result = number * number
    return f"The square of {number} is {result}"


# ============================================================
# PART 4 - HTTP Methods (GET and POST)
# ============================================================

# By default, routes only accept GET requests
# GET = fetching/reading data (like visiting a page)
# POST = sending/submitting data (like a form submission)

# We use render_template_string() to write HTML directly in the same file
# (Normally we'd use separate HTML files, but this is easier for learning)

# A simple HTML form - written as a Python string
html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Form</title>
</head>
<body>
    <h2>Simple Flask Form</h2>

    <!-- This form sends data to /greet using POST method -->
    <form method="POST" action="/greet">
        <label>Enter your name:</label>
        <input type="text" name="username" placeholder="Your name here">
        <br><br>
        <input type="submit" value="Say Hello!">
    </form>

    <!-- Show the result message if there is one -->
    {% if message %}
        <h3>{{ message }}</h3>
    {% endif %}
</body>
</html>
"""


# methods=["GET", "POST"] means this route handles both types
@app.route("/greet", methods=["GET", "POST"])
def greet_form():
    message = None  # no message at first

    if request.method == "POST":
        # request.form is a dictionary of all form data sent by the user
        # "username" matches the name="username" in our HTML input
        username = request.form.get("username")

        # .get() is safer than request.form["username"]
        # it won't crash if the field is empty or missing
        if username:
            message = f"Hello, {username}! Flask received your name 🎉"
        else:
            message = "You didn't enter a name!"

    # render_template_string() renders HTML written as a string
    # We pass 'message' so the HTML template can use it
    return render_template_string(html_form, message=message)


# ============================================================
# PART 5 - Understanding Request Object
# ============================================================

# The `request` object has lots of useful info about the incoming request
# Let's make a route that shows some of that info

@app.route("/request-info")
def request_info():
    # request.method = GET, POST, PUT, DELETE etc.
    method = request.method

    # request.args = query parameters from the URL
    # e.g. /request-info?city=Mumbai  -> request.args.get("city") = "Mumbai"
    city = request.args.get("city", "not provided")

    # request.host = the server address (like 127.0.0.1:5000)
    host = request.host

    # request.path = the URL path (like /request-info)
    path = request.path

    # building a simple response string with all this info
    info = f"""
    <h2>Request Info</h2>
    <p><b>Method:</b> {method}</p>
    <p><b>Host:</b> {host}</p>
    <p><b>Path:</b> {path}</p>
    <p><b>City (from URL param):</b> {city}</p>
    <p>Try: <a href="/request-info?city=Mumbai">/request-info?city=Mumbai</a></p>
    """
    return info


# ============================================================
# PART 6 - Returning Different Responses
# ============================================================

# Flask lets us return more than just strings
# We can return HTML, set status codes, add headers etc.

@app.route("/custom-response")
def custom_response():
    # We can return a tuple: (response_body, status_code)
    # 200 = OK (default), 404 = Not Found, 500 = Server Error etc.
    return "This response has a custom status code!", 200


@app.route("/not-found-example")
def not_found():
    # Manually returning a 404 response to show how it works
    return "Oops! This page doesn't really exist (demo)", 404


# ============================================================
# Running the App
# ============================================================

# This block runs only when we execute the file directly
# Not when it's imported somewhere else
if __name__ == "__main__":
    # debug=True means:
    # 1. It auto-reloads when we change the code (very helpful!)
    # 2. It shows detailed error messages in the browser
    # NOTE: Never use debug=True in production!
    app.run(debug=True)


# ============================================================
# QUICK RECAP - What I learned in this file:
# ============================================================
#
# 1. Flask app is created with Flask(__name__)
# 2. @app.route("/path") connects a URL to a Python function
# 3. The function is called a "view function"
# 4. Dynamic routes use <variable> in the URL path
# 5. methods=["GET","POST"] lets a route handle form submissions
# 6. request.form gets data from HTML forms (POST)
# 7. request.args gets data from URL query strings (GET)
# 8. render_template_string() renders HTML written inside Python
# 9. We can return (response, status_code) as a tuple
# 10. debug=True is great for development, bad for production
#
# Routes in this file:
# GET  /                -> home page
# GET  /about           -> about page
# GET  /contact         -> contact page
# GET  /user/<name>     -> greet user by name
# GET  /square/<number> -> calculate square
# GET  /greet           -> show form
# POST /greet           -> handle form submission
# GET  /request-info    -> show request details
# GET  /custom-response -> show custom status code
# GET  /not-found-example -> manual 404 demo
# ============================================================
