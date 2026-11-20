# ui/login_window.py
import customtkinter as ctk
from tkinter import messagebox
from ui.signup_window import SignupWindow

# Configuration globale du design CustomTkinter
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

class LoginWindow(ctk.CTk):
    def __init__(self, db_manager, on_login_success):
        super().__init__()

        self.db_manager = db_manager
        self.on_login_success = on_login_success 

        
        self.title("Connexion - Bibliothèque")
        self.geometry("400x450")
        self.resizable(False, False)

        # Centrer la fenêtre sur l'écran
        self.eval('tk::PlaceWindow . center')

        # Titre
        self.label_titre = ctk.CTkLabel(self, text="Bienvenue", font=ctk.CTkFont(size=30, weight="bold"))
        self.label_titre.pack(pady=(40, 10))
        
        self.label_sous_titre = ctk.CTkLabel(self, text="Connectez-vous pour continuer", font=ctk.CTkFont(size=14), text_color="gray")
        self.label_sous_titre.pack(pady=(0, 30))

        # Champ Email
        self.entry_email = ctk.CTkEntry(self, placeholder_text="Adresse Email", width=250, height=40)
        self.entry_email.pack(pady=10)

        # Champ Mot de passe
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*", width=250, height=40)
        self.entry_password.pack(pady=10)

        # Bouton de connexion
        self.btn_login = ctk.CTkButton(self, text="Se connecter", command=self.verifier_connexion, width=250, height=40, font=ctk.CTkFont(weight="bold"))
        self.btn_login.pack(pady=20)

        # Bouton pour ouvrir la fenêtre d'inscription (Désormais bien placé dans __init__)
        self.btn_open_signup = ctk.CTkButton(self, text="Pas encore de compte ? S'inscrire", 
                                             command=self.ouvrir_inscription, 
                                             fg_color="transparent", 
                                             text_color=("gray10", "gray90"), 
                                             hover_color=("gray70", "gray30"),
                                             width=250)
        self.btn_open_signup.pack(pady=10)

    def verifier_connexion(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if not email or not password:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

        # Appel à la base de données via notre manager
        user = self.db_manager.authenticate_user(email, password)

        if user:
            # Connexion réussie !
            self.entry_password.delete(0, 'end') 
            self.withdraw() 
            self.on_login_success(user) 
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")
            
    def ouvrir_inscription(self):
       
        SignupWindow(self, self.db_manager)