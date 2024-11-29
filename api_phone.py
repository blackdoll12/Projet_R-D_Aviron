from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from pymongo.server_api import ServerApi
# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin

# Configuration Flask et MongoDB
app = Flask(__name__)
uri = "mongodb+srv://chrisfotso:Junior123@clusterbryan.hmoea.mongodb.net/?retryWrites=true&w=majority&appName=ClusterBryan"
 
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
 
# Send a ping to confirm a successful connection
try:
   
    db = client['AvironDB']
    """ client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!") """
   
except Exception as e:
    print(e)

# Route pour ajouter un document
@app.route("/add", methods=["POST"])
def add_document(collection):
    try:
        data = request.json  # Récupérer les données JSON envoyées par l'application iOS
        result = collection.insert_one(data)
        return jsonify({"status": "success", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/addmultiple", methods=["POST"])
def add_document(collection):
    try:
        data = request.json  # Récupérer les données JSON envoyées par l'application iOS
        result = collection.insert_many(list(data))
        return jsonify({"status": "success", "ids": list(map(str, result.inserted_ids))}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
# Route pour lire tous les documents
@app.route("/get", methods=["GET"])
def get_documents(collection):
    try:
        documents = list(collection.find())  # Récupérer tous les documents
        for doc in documents:
            doc["_id"] = str(doc["_id"])  # Convertir l'ObjectId en string
        return jsonify({"status": "success", "documents": documents}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route pour mettre à jour un document
@app.route("/update/<string:id>", methods=["PUT"])
def update_document(id, collection):
    try:
        data = request.json  # Récupérer les nouvelles données à mettre à jour
        result = collection.update_one(
            {"_id": ObjectId(id)},  # Rechercher le document par son ID
            {"$set": data}  # Mettre à jour les champs spécifiés
        )
        if result.modified_count == 0:
            return jsonify({"status": "error", "message": "Document not found or no change made"}), 404
        return jsonify({"status": "success", "modified_count": result.modified_count}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route pour supprimer un document
@app.route("/delete/<string:id>", methods=["DELETE"])
def delete_document(collection,id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})  # Supprimer le document par ID
        if result.deleted_count == 0:
            return jsonify({"status": "error", "message": "Document not found"}), 404
        return jsonify({"status": "success", "deleted_count": result.deleted_count}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
