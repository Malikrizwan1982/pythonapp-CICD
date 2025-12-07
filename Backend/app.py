from flask import Flask, jsonify
from pymongo import MongoClient
import os
from flask_cors import CORS # Needed for cross-origin requests from the Frontend

app = Flask(__name__)
# Enable CORS for the frontend to communicate with the backend
CORS(app) 

# --- Database Connection ---
# The hostname 'mongodb' is used because it's the service name in docker-compose.yml
# The port is the default MongoDB port, 27017
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(MONGO_URI)
db = client.simple_db
counter_collection = db.counter_data

@app.route('/')
def hello_world():
    return 'Backend is running!'

@app.route('/api/counter', methods=['GET'])
def get_counter():
    """Retrieves the current counter value."""
    # Find the single document storing the counter (or create if it doesn't exist)
    data = counter_collection.find_one({'_id': 'app_counter'})
    
    if data:
        current_value = data.get('value', 0)
    else:
        # Initialize if not found
        current_value = 0
        counter_collection.insert_one({'_id': 'app_counter', 'value': current_value})

    return jsonify({'value': current_value})

@app.route('/api/increment', methods=['POST'])
def increment_counter():
    """Increments the counter value by 1."""
    # Atomically increment the counter and return the new value
    result = counter_collection.find_one_and_update(
        {'_id': 'app_counter'},
        {'$inc': {'value': 1}},
        upsert=True,
        return_document=True # Return the updated document
    )
    
    new_value = result['value']
    return jsonify({'value': new_value})

if __name__ == '__main__':
    # Use 0.0.0.0 to make the service externally accessible within the Docker network
    app.run(host='0.0.0.0', port=5000)