from pymongo import MongoClient # type: ignore

client = MongoClient("mongodb+srv://iaksg:ynot6803@learningbookgenerator.h88j6.mongodb.net/?retryWrites=true&w=majority&appName=LearningBookGenerator")

db = client["lbg"]

# Sélection de la collection
collection_livre = db["livre"]
collection_user = db["user"]

print("Connexion réussie à MongoDB !")


def save_livre(livre):
  result = collection_livre.insert_one(livre)
  print(f"Livre inséré avec l'ID : {result.inserted_id}")
  return result

def save_user(user):
  result = collection_user(user)
  print(f"Utilisateur inséré avec l'ID : {result.inserted_id}")
  return result
