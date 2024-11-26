from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import uuid

import main as main_program

import repository as repo
from passlib.context import CryptContext



# Création de l'application FastAPI
app = FastAPI()

# Modèle pour les sous-parties de chapitre
class SousPartie(BaseModel):
    titre: str
    contenu: str

# Modèle pour les chapitres
class Chapitre(BaseModel):
    titre: str
    sous_parties: List[SousPartie]

# Modèle pour le livre
class Livre(BaseModel):
    id: Optional[str] = None
    titre: str
    chapitres: List[Chapitre]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # URL de votre application Angular
        "http://127.0.0.1:4200",  # Ajoutez aussi cette variante
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP
    allow_headers=["*"],  # Autorise tous les headers
)

# Fonction pour analyser le texte
def analyser_texte(texte: str) -> Livre:
    # Séparer les sections du texte en lignes
    lignes = texte.splitlines()
    
    # Le titre du livre est la première ligne
    titre_livre = lignes[0].replace("Sujet: ", "").strip()
    
    # Variables pour stocker les chapitres et sous-parties
    chapitres = []
    chapitre = None
    sous_partie = None

    # Parcourir les lignes du texte
    for ligne in lignes[1:]:
        ligne = ligne.strip()

        # Si la ligne est un titre de chapitre
        if ligne.startswith("###"):
            # Si un chapitre est déjà en cours, on l'ajoute à la liste
            if chapitre:
                chapitres.append(chapitre)
            
            # Créer un nouveau chapitre
            chapitre_titre = ligne.replace("###", "").strip()
            chapitre = Chapitre(titre=chapitre_titre, sous_parties=[])
        
        # Si la ligne est un titre de sous-partie
        elif ligne.startswith("#"):
            if chapitre:
                if sous_partie:  # Si une sous-partie est en cours, on l'ajoute
                    chapitre.sous_parties.append(sous_partie)
                
                sous_partie_titre = ligne.replace("#", "").strip()
                sous_partie = SousPartie(titre=sous_partie_titre, contenu="")
        
        # Si la ligne n'est ni un titre de chapitre, ni un titre de sous-partie
        elif ligne:
            if sous_partie:
                # Ajouter le contenu à la sous-partie en cours
                sous_partie.contenu += ligne + "\n"
    
    # Ajouter la dernière sous-partie et chapitre en cours
    if sous_partie:
        chapitre.sous_parties.append(sous_partie)
    if chapitre:
        chapitres.append(chapitre)
    
    # Créer et retourner l'objet Livre
    livre = Livre(titre=titre_livre, chapitres=chapitres)
    return livre

def lire_fichier(fichier_path):
    try:
        with open(fichier_path, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
        return contenu
    except FileNotFoundError:
        print(f"Le fichier {fichier_path} n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"Une erreur est survenue lors de la lecture du fichier : {e}")
        return None

@app.get("/generateBook", response_model=Livre)
async def generate_book(sujet: str):
    main_program.generate_livre(sujet)
    livre = analyser_texte(lire_fichier("output.txt"))
    livre = livre.model_copy(update={"id": str(uuid.uuid4())})
    repo.insert_document(livre.model_dump())
    return livre

@app.get("/getAllBooks", response_model=List[Livre])
async def get_all_books():
    livres = repo.find_all_documents()
    return livres

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/register")
async def register_user(username: str, password: str):
    repo.register(username, password)

@app.post("/login")
async def login_user(username: str, password: str):
    return repo.login(username, password)
