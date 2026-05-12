# ============================================================
# Flask REST APIs - Learning File
# Topic: RESTful Endpoints, JSON, API Versioning
# ============================================================

# What is a REST API?
# It's a way for two programs to talk to each other over the internet.
# Instead of returning HTML pages for a human to read, an API returns raw data 
# (usually in JSON format) for another program (like a React frontend or a mobile app) to use.

from flask import Flask, jsonify, request, Blueprint

app = Flask(__name__)

# ============================================================
# PART 1 - IN-MEMORY DATABASE (For testing)
# ============================================================
# Instead of setting up SQLAlchemy again, we'll just use a Python list.
# Every time the server restarts, this data resets.

users_db = [
    {"id": 1, "name": "Alice", "role": "admin"},
    {"id": 2, "name": "Bob", "role": "user"},
    {"id": 3, "name": "Charlie", "role": "user"}
]

# Helper function to find the next available ID
def get_next_id():
    if not users_db:
        return 1
    return max(user["id"] for user in users_db) + 1


# ============================================================
# PART 2 - API VERSIONING (Using Blueprints)
# ============================================================

# Why versioning? 
# If people are using your API, and you suddenly change how it works, their apps will break!
# Instead, you create a "v2". Old apps keep using "v1", new apps use "v2".
# Blueprints let us group routes together under a common prefix.

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')


# ============================================================
# PART 3 - DESIGNING RESTful ENDPOINTS (v1)
# ============================================================
# REST uses standard HTTP Methods to define actions:
# GET    = Read/Fetch data
# POST   = Create new data
# PUT    = Update existing data completely
# DELETE = Remove data
#
# Status Codes:
# 200 = OK, 201 = Created, 400 = Bad Request, 404 = Not Found

# --- 1. GET (Read All) ---
@api_v1.route('/users', methods=['GET'])
def get_users():
    # jsonify() converts Python dictionaries/lists into a JSON string response
    return jsonify({
        "status": "success",
        "count": len(users_db),
        "data": users_db
    }), 200 # 200 OK is the default, but it's good practice to be explicit


# --- 2. GET (Read One) ---
@api_v1.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    # Search for the user in our list
    user = next((u for u in users_db if u["id"] == user_id), None)
    
    if user is None:
        # 404 Not Found
        return jsonify({"error": "User not found"}), 404
        
    return jsonify(user), 200


# --- 3. POST (Create) ---
@api_v1.route('/users', methods=['POST'])
def create_user():
    # request.get_json() parses the incoming JSON data sent by the client
    data = request.get_json()
    
    # Validation: Ensure 'name' is provided
    if not data or not 'name' in data:
        # 400 Bad Request
        return jsonify({"error": "Missing 'name' field in JSON body"}), 400
        
    new_user = {
        "id": get_next_id(),
        "name": data['name'],
        "role": data.get('role', 'user') # Default to 'user' if role isn't provided
    }
    
    users_db.append(new_user)
    
    # 201 Created
    return jsonify({
        "message": "User created successfully",
        "user": new_user
    }), 201


# --- 4. PUT (Update) ---
@api_v1.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users_db if u["id"] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    # Update the dictionary
    user['name'] = data.get('name', user['name'])
    user['role'] = data.get('role', user['role'])
    
    return jsonify({
        "message": "User updated successfully",
        "user": user
    }), 200


# --- 5. DELETE (Remove) ---
@api_v1.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users_db
    # Find user first
    user = next((u for u in users_db if u["id"] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
        
    # Filter out the deleted user
    users_db = [u for u in users_db if u["id"] != user_id]
    
    return jsonify({"message": f"User {user_id} deleted successfully"}), 200


# ============================================================
# PART 4 - API VERSION 2 (Demonstrating changes)
# ============================================================

# Let's say in v2, we want the response structure to be different
# Instead of just returning the list, we want nested data.
@api_v2.route('/users', methods=['GET'])
def get_users_v2():
    # Different structure than v1
    formatted_data = []
    for user in users_db:
        formatted_data.append({
            "identifier": user["id"],  # Changed 'id' to 'identifier'
            "full_name": user["name"]  # Changed 'name' to 'full_name'
        })
        
    return jsonify({
        "api_version": "v2.0",
        "results": formatted_data
    }), 200


# ============================================================
# PART 5 - REGISTER BLUEPRINTS
# ============================================================
# We have defined the blueprints, now we attach them to the app.

app.register_blueprint(api_v1)
app.register_blueprint(api_v2)


# Just a simple home route to guide the user
@app.route('/')
def home():
    return """
    <h2>Flask REST API Demo</h2>
    <p>Try visiting these endpoints in your browser or Postman:</p>
    <ul>
        <li><a href="/api/v1/users">GET /api/v1/users</a> (v1 API)</li>
        <li><a href="/api/v1/users/1">GET /api/v1/users/1</a> (Single User)</li>
        <li><a href="/api/v2/users">GET /api/v2/users</a> (v2 API - notice the different format)</li>
    </ul>
    <p><i>Note: POST, PUT, and DELETE requests usually require a tool like Postman, cURL, or a frontend app to test properly.</i></p>
    """


if __name__ == '__main__':
    app.run(debug=True)

# ============================================================
# QUICK RECAP - What I learned in this file:
# ============================================================
#
# 1. WHAT IS REST?
#    Using standard URLs and HTTP Methods (GET, POST, PUT, DELETE) to manage data.
#    It returns raw JSON instead of HTML pages.
#
# 2. JSONIFY:
#    `jsonify(dictionary)` is Flask's built-in tool to turn Python dicts/lists 
#    into properly formatted JSON responses.
#
# 3. HANDLING JSON REQUESTS:
#    When a frontend sends JSON data in a POST/PUT request, you read it using
#    `data = request.get_json()`. It converts the JSON into a Python dictionary.
#
# 4. HTTP STATUS CODES:
#    Return a tuple: `return jsonify(...), 200`
#    - 200 = OK (Success)
#    - 201 = Created (Successful POST)
#    - 400 = Bad Request (Client sent missing/bad data)
#    - 404 = Not Found (ID doesn't exist)
#
# 5. API VERSIONING & BLUEPRINTS:
#    `Blueprint('name', __name__, url_prefix='/api/v1')` groups routes together.
#    This allows you to create a `/v2` later without breaking `/v1` for older clients.
# ============================================================
