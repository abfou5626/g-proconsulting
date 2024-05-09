import pymongo
import uuid
import pandas as pd 

try:
    # Connexion à MongoDB
    mongodb_url = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(mongodb_url)
    db = client["commandes"]
    collection = db["factures"]
    collection1 =db["facture_brute"]
    collection2=db["facture_prix"]
    print("Connexion à la base de données établie avec succès.")
except pymongo.errors.ConnectionFailure as e:
    print("Erreur de connexion à la base de données MongoDB:", e)
except Exception as e:
    print("Une erreur inattendue s'est produite:", e)

