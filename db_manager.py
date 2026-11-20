# db_manager.py
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import bcrypt

class DBManager:
    def __init__(self):
        """Initialise la configuration depuis config.py"""
        self.config = DB_CONFIG

    def get_connection(self):
        """Établit et retourne une connexion à la base de données."""
        try:
            conn = mysql.connector.connect(**self.config)
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"Erreur de connexion à MySQL : {e}")
            return None

    def execute_query(self, query, params=None):
        """Exécute une requête (INSERT, UPDATE, DELETE) et valide les changements."""
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount  # Retourne le nombre de lignes affectées
            except Error as e:
                print(f"Erreur lors de l'exécution de la requête : {e}")
                return None
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

    def fetch_all(self, query, params=None):
        
        conn = self.get_connection()
        if conn:
            try:
                # dictionary=True permet de récupérer les résultats sous forme de dictionnaire 
                cursor = conn.cursor(dictionary=True) 
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results
            except Error as e:
                print(f"Erreur lors de la récupération des données : {e}")
                return None
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
    def authenticate_user(self, email, password_clair):
        """Vérifie les identifiants avec bcrypt."""
        # 1. On récupère l'utilisateur par son email (y compris son mot de passe haché)
        query = "SELECT id_membre, nom, prenom, role, mot_de_passe FROM Membres WHERE email = %s"
        result = self.fetch_all(query, (email,))
        
        if result and len(result) == 1:
            user = result[0]
            # bcrypt a besoin que le mot de passe stocké soit en format 'bytes'
            stored_hash = user['mot_de_passe'].encode('utf-8') 
            
            # 2. On utilise bcrypt pour vérifier si le mot de passe en clair correspond au hash
            if bcrypt.checkpw(password_clair.encode('utf-8'), stored_hash):
                # Par sécurité, on retire le mot de passe du dictionnaire avant de le renvoyer
                del user['mot_de_passe']
                return user
                
        return None

    def hash_password(self, password_clair):
        """Méthode utilitaire pour hacher un mot de passe (utile pour l'INSERT d'un membre)."""
        salt = bcrypt.gensalt()
        # On retourne une chaîne de caractères (string) pour l'insérer facilement dans MySQL
        return bcrypt.hashpw(password_clair.encode('utf-8'), salt).decode('utf-8')
    def register_user(self, nom, prenom, email, telephone, password_clair):
        """Inscrit un nouvel utilisateur avec un mot de passe haché par bcrypt."""
        # 1. Vérifier si l'email existe déjà
        check_query = "SELECT id_membre FROM Membres WHERE email = %s"
        if self.fetch_all(check_query, (email,)):
            return False, "Cet email est déjà utilisé."

        # 2. Hacher le mot de passe
        hashed_pwd = self.hash_password(password_clair)

        # 3. Insérer le nouvel utilisateur (rôle 'membre' par défaut)
        query = """INSERT INTO Membres (nom, prenom, email, telephone, mot_de_passe, role) 
                   VALUES (%s, %s, %s, %s, %s, 'membre')"""
        params = (nom, prenom, email, telephone, hashed_pwd)
        
        lignes_affectees = self.execute_query(query, params)
        if lignes_affectees:
            return True, "Compte créé avec succès !"
        else:
            return False, "Erreur lors de la création du compte."
    

    def get_all_livres(self):
        """Récupère tous les livres avec le nom de leur auteur via une jointure."""
        query = """
            SELECT l.id_livre, l.titre, l.isbn, l.annee_publication, a.nom, a.prenom 
            FROM Livres l
            LEFT JOIN Auteurs a ON l.id_auteur = a.id_auteur
            ORDER BY l.titre ASC
        """
        return self.fetch_all(query)
    def get_all_auteurs(self):
        """Récupère la liste de tous les auteurs."""
        query = "SELECT id_auteur, nom, prenom FROM Auteurs ORDER BY nom"
        return self.fetch_all(query)

    def ajouter_livre(self, titre, isbn, annee, id_auteur):
        """Insère un nouveau livre dans la base de données."""
        # On vérifie d'abord si l'ISBN existe déjà pour éviter une erreur SQL brutale
        check_query = "SELECT id_livre FROM Livres WHERE isbn = %s"
        if self.fetch_all(check_query, (isbn,)):
            return False, "Un livre avec cet ISBN existe déjà."

        query = "INSERT INTO Livres (titre, isbn, annee_publication, id_auteur) VALUES (%s, %s, %s, %s)"
        lignes = self.execute_query(query, (titre, isbn, annee, id_auteur))
        
        if lignes:
            return True, "Le livre a été ajouté avec succès."
        return False, "Erreur lors de l'ajout du livre."
    def supprimer_livre(self, id_livre):
        """Supprime un livre de la base de données selon son ID."""
        query = "DELETE FROM Livres WHERE id_livre = %s"
        lignes = self.execute_query(query, (id_livre,))
        
        if lignes:
            return True, "Le livre a été supprimé avec succès."
        return False, "Erreur ou livre introuvable lors de la suppression."
    def modifier_livre(self, id_livre, titre, isbn, annee, id_auteur):
        """Met à jour les informations d'un livre existant."""
        # On vérifie si le nouvel ISBN n'est pas déjà pris par un AUTRE livre
        check_query = "SELECT id_livre FROM Livres WHERE isbn = %s AND id_livre != %s"
        if self.fetch_all(check_query, (isbn, id_livre)):
            return False, "Un autre livre utilise déjà cet ISBN."

        query = """UPDATE Livres 
                   SET titre = %s, isbn = %s, annee_publication = %s, id_auteur = %s 
                   WHERE id_livre = %s"""
        
        lignes = self.execute_query(query, (titre, isbn, annee, id_auteur, id_livre))
        
        # execute_query renvoie None s'il y a une erreur. S'il renvoie 0 ou plus, c'est un succès.
        if lignes is not None: 
            return True, "Le livre a été modifié avec succès."
        return False, "Erreur lors de la modification du livre."
    
    def get_all_membres(self):
        """Récupère la liste de tous les membres inscrits."""
        # On ne récupère pas le mot de passe pour des raisons de sécurité
        query = "SELECT id_membre, nom, prenom, email, telephone, role FROM Membres ORDER BY nom ASC"
        return self.fetch_all(query)
    
    def get_emprunts(self, id_membre=None):
        """
        Récupère les emprunts avec les noms des livres et des membres.
        Si id_membre est fourni, filtre uniquement pour ce membre.
        """
        query = """
            SELECT e.id_emprunt, l.titre AS livre, m.nom, m.prenom, 
                   e.date_emprunt, e.date_retour_prevue, e.date_retour_effective 
            FROM Emprunts e
            JOIN Livres l ON e.id_livre = l.id_livre
            JOIN Membres m ON e.id_membre = m.id_membre
        """
        params = None
        
        # Si ce n'est pas un admin, on filtre par l'ID de l'utilisateur connecté
        if id_membre is not None:
            query += " WHERE e.id_membre = %s"
            params = (id_membre,)
            
        query += " ORDER BY e.date_emprunt DESC"
        
        return self.fetch_all(query, params)
    
    def rendre_livre(self, id_emprunt):
        """Met à jour la date de retour effective à aujourd'hui."""
        # On vérifie que la date_retour_effective est NULL pour ne pas écraser un retour déjà validé
        query = "UPDATE Emprunts SET date_retour_effective = CURDATE() WHERE id_emprunt = %s AND date_retour_effective IS NULL"
        lignes = self.execute_query(query, (id_emprunt,))
        
        if lignes and lignes > 0:
            return True, "Le livre a été marqué comme rendu avec succès."
        return False, "Erreur : L'emprunt est introuvable ou le livre a déjà été rendu."
    
    def ajouter_emprunt(self, id_livre, id_membre):
        """Crée un nouvel emprunt avec une date de retour prévue dans 14 jours."""
        # 1. On vérifie si le livre n'est pas DÉJÀ emprunté (et pas encore rendu)
        check_query = "SELECT id_emprunt FROM Emprunts WHERE id_livre = %s AND date_retour_effective IS NULL"
        if self.fetch_all(check_query, (id_livre,)):
            return False, "Ce livre est actuellement indisponible (déjà emprunté)."

        # 2. On insère le nouvel emprunt (CURDATE() = aujourd'hui, DATE_ADD = +14 jours)
        query = """INSERT INTO Emprunts (id_livre, id_membre, date_emprunt, date_retour_prevue) 
                   VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY))"""
        
        lignes = self.execute_query(query, (id_livre, id_membre))
        
        if lignes:
            return True, "L'emprunt a été enregistré avec succès (retour prévu dans 14 jours)."
        return False, "Erreur lors de l'enregistrement de l'emprunt."
    
    def get_statistiques(self):
        """Récupère le nombre total de livres, membres et emprunts en cours."""
        try:
            nb_livres = self.fetch_all("SELECT COUNT(*) as total FROM Livres")[0]['total']
            nb_membres = self.fetch_all("SELECT COUNT(*) as total FROM Membres")[0]['total']
            # On compte uniquement les emprunts qui n'ont pas encore été rendus
            nb_emprunts = self.fetch_all("SELECT COUNT(*) as total FROM Emprunts WHERE date_retour_effective IS NULL")[0]['total']
            return nb_livres, nb_membres, nb_emprunts
        except Exception as e:
            print(f"Erreur lors de la récupération des statistiques : {e}")
            return 0, 0, 0
        
    # ==================== GESTION DES AUTEURS ====================
    def ajouter_auteur(self, nom, prenom):
        """Insère un nouvel auteur dans la base de données."""
        query = "INSERT INTO Auteurs (nom, prenom) VALUES (%s, %s)"
        lignes = self.execute_query(query, (nom, prenom))
        
        if lignes:
            return True, "L'auteur a été ajouté avec succès."
        return False, "Erreur lors de l'ajout de l'auteur."

    def modifier_auteur(self, id_auteur, nom, prenom):
        """Met à jour les informations d'un auteur existant."""
        query = "UPDATE Auteurs SET nom = %s, prenom = %s WHERE id_auteur = %s"
        lignes = self.execute_query(query, (nom, prenom, id_auteur))
        
        if lignes is not None: 
            return True, "L'auteur a été modifié avec succès."
        return False, "Erreur lors de la modification de l'auteur."

    def supprimer_auteur(self, id_auteur):
        """Supprime un auteur (uniquement s'il n'a pas de livres associés)."""
        # 1. Vérification de sécurité : l'auteur a-t-il des livres ?
        check_query = "SELECT id_livre FROM Livres WHERE id_auteur = %s"
        if self.fetch_all(check_query, (id_auteur,)):
            return False, "Impossible de supprimer cet auteur car il possède des livres dans la bibliothèque."

        # 2. Suppression s'il n'y a pas de livres
        query = "DELETE FROM Auteurs WHERE id_auteur = %s"
        lignes = self.execute_query(query, (id_auteur,))
        
        if lignes:
            return True, "L'auteur a été supprimé avec succès."
        return False, "Erreur ou auteur introuvable lors de la suppression."