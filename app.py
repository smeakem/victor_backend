import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('user')


@app.route('/users', methods=['POST'])
def add_user():
    try:
        username = request.json['username']
        user_ref.document(username).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False}), 404


@app.route('/users', methods=['GET'])
def get_users():
    try:
        user_id = request.args.get('id')
        if user_id:
            user = user_ref.document(user_id).get()
            return jsonify(user.to_dict()), 200
        else:
            all_users = [doc.to_dict() for doc in user_ref.stream()]
            return jsonify(all_users), 200
    except Exception as e:
        return jsonify({"success": False}), 404


@app.route('/users', methods=['POST', 'PUT'])
def update_user():
    try:
        id = request.json['id']
        user_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False}), 404


@app.route('/delete', methods=['GET', 'DELETE'])
def delete_user():
    try:
        user_id = request.args.get('id')
        user_ref.document(user_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
