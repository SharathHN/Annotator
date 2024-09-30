from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient('mongodb+srv://sharathhnvasistha:hALV5zOvrdZJIdAd@dataannotations.ogik7.mongodb.net/?retryWrites=true&w=majority&appName=DataAnnotations')  # Adjust the connection string if using MongoDB Atlas
db = client.HumbleBragging
texts_collection = db.DataAnnotations
annotations_collection = db.annotations

# List of predefined users
users = ["User1", "User2", "User3"]

@app.route('/users', methods=['GET'])
def get_users():
    # Return the list of users
    return jsonify({'users': users})

@app.route('/texts/<username>', methods=['GET'])
def get_texts_for_user(username):
    # Fetch texts that have NOT been annotated by the specified user
    annotated_texts = texts_collection.find({username:""})
    annotated_text_ids = [{'text': annot['text'], '_id': str(annot['_id'])} for annot in annotated_texts]


    return jsonify({'texts': annotated_text_ids})

@app.route('/annotate', methods=['POST'])
def annotate_text():
    data = request.json
    print(data)
    username = data.get('user')
    text_id = data.get('text_id')
    response = data.get('response')

    # Save the annotation to MongoDB
    texts_collection.update_one(
    {'_id': ObjectId(text_id)},  # Find the document with the given _id
    {'$set': {username: response}},  # Set the field named after the username to the response
    upsert=True  # If the document does not exist, create a new one
)

    return jsonify({'message': 'Annotation saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)
