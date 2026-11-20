# setup_bcrypt.py
from db_manager import DBManager
import bcrypt

def update_passwords_to_bcrypt():
    db = DBManager()
    
    # On génère un nouveau hash bcrypt pour 'password123'
    mot_de_passe_clair = "password123"
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(mot_de_passe_clair.encode('utf-8'), salt).decode('utf-8')
    
    # On met à jour tous les membres dans la base de données
    query = "UPDATE Membres SET mot_de_passe = %s"
    lignes_modifiees = db.execute_query(query, (hashed_pwd,))
    
    if lignes_modifiees is not None:
        print(f"Succès ! {lignes_modifiees} mots de passe ont été mis à jour avec bcrypt.")
    else:
        print("Une erreur est survenue lors de la mise à jour.")

if __name__ == "__main__":
    update_passwords_to_bcrypt()