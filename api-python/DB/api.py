import requests
from bson import ObjectId
from flask import Flask, jsonify, app
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
CORS(app)

try:
    client = pymongo.MongoClient("mongodb+srv://Sara:1234@cluster0.jyqagdy.mongodb.net/", serverSelectionTimeoutMS=5000)
    db = client['basicMongoDb']
    collection = db['Collection1']
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"Error deleting document: {e}")
    db=None
    collection=None


@app.route('/')
def home():
    return "Welcome to the Flask API!"


@app.route('/getPersons', methods=['GET'])
def person():
    documents = collection.find()
    return list(documents)

@app.route('/getPerson/<int:_id>', methods=['GET'])
def get_person(_id):
    try:
        person = collection.find_one({'_id': _id})
        if person:
            return jsonify(person), 200
        else:
            return jsonify({'error': 'Person not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/newPerson', methods=['POST'])
def new_person():
    try:
        data = request.get_json()  # Correctly get JSON data
        result = collection.insert_one(data)
        print(f"Person created successfully with id={result.inserted_id}")
        return jsonify({'message': 'Person created successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        print(f"Error creating person: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/updatePerson/<int:_id>/<string:name>', methods=['PUT'])
def update_person(_id, name):
    try:
        result = collection.update_one(
            {'_id': _id},
            {'$set': {'name': name}}
        )
        if result.modified_count > 0:
            return jsonify({'message': f'Person with _id={_id} updated successfully'}), 200
        else:
            return jsonify({'message': f'Person with _id={_id} not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deletePerson/<int:_id>', methods=['DELETE'])
def delete_person(_id):
    try:
        result = collection.delete_one({'_id': _id})
        if result.deleted_count > 0:
            return jsonify({'message': f'Person with _id={_id} deleted successfully'}), 200
        else:
            return jsonify({'message': f'Person with _id={_id} not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
