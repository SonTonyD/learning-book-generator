from pymongo import MongoClient

# Paramètres de connexion
uri = "mongodb+srv://dinhsontony:tony1234@cluster0.sv7rj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Modifiez selon votre configuration
db_name = "lbg"
collection_name = "livre"

# Connexion à la base MongoDB
client = MongoClient(uri)
db = client[db_name]
collection = db[collection_name]

print(f"Connecté à la base {db_name}, collection {collection_name}")

# Fonction pour insérer un document
def insert_document(document):
    """
    Insère un document dans la collection.

    :param document: Dictionnaire représentant le document à insérer
    """
    result = collection.insert_one(document)
    print(f"Document inséré avec l'ID : {result.inserted_id}")

# Fonction pour rechercher tous les documents
def find_all_documents():
    """
    Récupère tous les documents de la collection.

    :return: Liste de tous les documents
    """
    documents = list(collection.find())
    print(f"{len(documents)} documents trouvés.")
    return documents

