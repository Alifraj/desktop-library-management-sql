# main.py
from db_manager import DBManager
from ui.login_window import LoginWindow
from ui.main_window import MainWindow 

def lancer_application_principale(user_info):
    
    print(f"Ouverture de la session pour : {user_info['prenom']} ({user_info['role']})")
    
    # On initialise la fenêtre principale en lui passant l'accès BDD et les infos de l'utilisateur
    app = MainWindow(db, user_info)
    app.mainloop()

if __name__ == "__main__":
    db = DBManager()
    
    # On lance le Login. Si succès, 'lancer_application_principale' sera exécutée.
    login_app = LoginWindow(db, lancer_application_principale)
    login_app.mainloop()