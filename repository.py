from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from pymongo import MongoClient
from passlib.context import CryptContext


# Paramètres de connexion
uri = "mongodb+srv://dinhsontony:tony1234@cluster0.sv7rj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Modifiez selon votre configuration
db_name = "lbg"
collection_name = "livre"

# Connexion à la base MongoDB
client = MongoClient(uri)
db = client[db_name]
collection = db[collection_name]
users_collection = db['users']

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def register(username, password): 
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_password})
    return {"message": "User registered successfully"}




SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def login(username, password):
    user = users_collection.find_one({"username": username})
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_jwt_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}