# ui/signup_window.py
import customtkinter as ctk
from tkinter import messagebox

class SignupWindow(ctk.CTkToplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager

        self.title("Créer un compte")
        self.geometry("400x550")
        self.resizable(False, False)
        
        # Rend la fenêtre modale (bloque la fenêtre en dessous)
        self.grab_set()
        
        self.label_titre = ctk.CTkLabel(self, text="Inscription", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_titre.pack(pady=(20, 20))

        # Champs du formulaire
        self.entry_nom = ctk.CTkEntry(self, placeholder_text="Nom", width=250)
        self.entry_nom.pack(pady=10)

        self.entry_prenom = ctk.CTkEntry(self, placeholder_text="Prénom", width=250)
        self.entry_prenom.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Adresse Email", width=250)
        self.entry_email.pack(pady=10)
        
        self.entry_tel = ctk.CTkEntry(self, placeholder_text="Téléphone", width=250)
        self.entry_tel.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*", width=250)
        self.entry_password.pack(pady=10)

        self.entry_confirm_password = ctk.CTkEntry(self, placeholder_text="Confirmer mot de passe", show="*", width=250)
        self.entry_confirm_password.pack(pady=10)

        # Bouton de validation
        self.btn_signup = ctk.CTkButton(self, text="S'inscrire", command=self.valider_inscription, width=250, font=ctk.CTkFont(weight="bold"))
        self.btn_signup.pack(pady=20)

    def valider_inscription(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        email = self.entry_email.get()
        tel = self.entry_tel.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        # Vérifications de base
        if not all([nom, prenom, email, password, confirm_password]):
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        if password != confirm_password:
            messagebox.showwarning("Erreur", "Les mots de passe ne correspondent pas.")
            return

        if len(password) < 6:
            messagebox.showwarning("Erreur", "Le mot de passe doit contenir au moins 6 caractères.")
            return

        # Appel à la base de données
        success, message = self.db_manager.register_user(nom, prenom, email, tel, password)

        if success:
            messagebox.showinfo("Succès", message)
            self.destroy() # Ferme la fenêtre d'inscription et retourne au login
        else:
            messagebox.showerror("Erreur", message)