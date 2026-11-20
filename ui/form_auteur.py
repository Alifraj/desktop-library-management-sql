# ui/form_auteur.py
import customtkinter as ctk
from tkinter import messagebox

class FormulaireAuteur(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, callback_maj_tableau, auteur_data=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.callback_maj_tableau = callback_maj_tableau
        self.auteur_data = auteur_data 

        titre_fenetre = "Modifier l'auteur" if self.auteur_data else "Ajouter un auteur"
        self.title(titre_fenetre)
        self.geometry("350x300")
        self.resizable(False, False)
        self.grab_set() 

        ctk.CTkLabel(self, text=titre_fenetre, font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Champs de saisie
        self.entry_nom = ctk.CTkEntry(self, placeholder_text="Nom de famille", width=250)
        self.entry_nom.pack(pady=10)

        self.entry_prenom = ctk.CTkEntry(self, placeholder_text="Prénom", width=250)
        self.entry_prenom.pack(pady=10)

        # Pré-remplissage si modification
        if self.auteur_data:
            self.entry_nom.insert(0, self.auteur_data['nom'])
            self.entry_prenom.insert(0, self.auteur_data['prenom'])

        # Bouton Validation
        texte_bouton = "Mettre à jour" if self.auteur_data else "Enregistrer"
        btn_valider = ctk.CTkButton(self, text=texte_bouton, command=self.valider_formulaire, 
                                    fg_color="#b8860b" if self.auteur_data else "green", 
                                    hover_color="#8b6508" if self.auteur_data else "darkgreen", 
                                    width=250)
        btn_valider.pack(pady=30)

    def valider_formulaire(self):
        nom = self.entry_nom.get().strip()
        prenom = self.entry_prenom.get().strip()

        if not nom or not prenom:
            messagebox.showwarning("Erreur", "Veuillez remplir le nom et le prénom.")
            return

        # Appel à la base de données (Modification ou Ajout)
        if self.auteur_data:
            success, message = self.db_manager.modifier_auteur(self.auteur_data['id'], nom, prenom)
        else:
            success, message = self.db_manager.ajouter_auteur(nom, prenom)

        if success:
            messagebox.showinfo("Succès", message)
            self.callback_maj_tableau() 
            self.destroy() 
        else:
            messagebox.showerror("Erreur", message)