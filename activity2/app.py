from flask import Flask, jsonify, request, render_template, abort

app = Flask(__name__)

# Sample data
items = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"},
    {"id": 3, "name": "Item 3", "description": "This is item 3"},
]

# Endpoint 1: Welcome message
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

# Endpoint 2: List all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Endpoint 3: Get item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        abort(404, description="Item not found")
    return jsonify(item)

# Endpoint 4: Add a new item (POST request)
@app.route('/items', methods=['POST'])
def add_item():
    if request.is_json:
        # Handle JSON data
        new_item = request.json
        if not new_item or not "name" in new_item or not "description" in new_item:
            abort(400, description="Invalid input")
    else:
        # Handle form data
        name = request.form.get('name')
        description = request.form.get('description')
        if not name or not description:
            abort(400, description="Name and description are required")
        new_item = {
            "name": name,
            "description": description
        }

    # Create new item
    new_item["id"] = len(items) + 1
    items.append(new_item)

    if request.is_json:
        return jsonify(new_item), 201
    else:
        return render_template('items.html', items=items)

# Render HTML page for items
@app.route('/items-page')
def items_page():
    return render_template('items.html', items=items)

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

if __name__ == '__main__':
    app.run(debug=True)