from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
from pymongo.server_api import ServerApi
from weather import get_weather_data

app = Flask(__name__)

# Connexion à MongoDB
uri = "mongodb+srv://chrisfotso:Junior123@clusterbryan.hmoea.mongodb.net/?retryWrites=true&w=majority&appName=ClusterBryan"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Aviron_db']

# Une route simple pour tester l'API
@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur l'API!"})


@app.route("/upload_sensors_data", methods=["POST"])
def upload_sensor_data():
    try:
        # Récupérer les données JSON envoyées par le capteur
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        weather_data = get_weather_data() 
        
        data['weather'] = weather_data
        
        # Insérer dans la collection MongoDB
        collection = db['Activity']
        result = collection.insert_one(data)
        return jsonify({"message": "Data inserted successfully", "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
