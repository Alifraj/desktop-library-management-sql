# ui/form_emprunt.py
import customtkinter as ctk
from tkinter import messagebox

class FormulaireEmprunt(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, callback_maj_tableau):
        super().__init__(parent)
        self.db_manager = db_manager
        self.callback_maj_tableau = callback_maj_tableau

        self.title("Nouvel Emprunt")
        self.geometry("400x350")
        self.resizable(False, False)
        self.grab_set() # Rend la fenêtre modale

        ctk.CTkLabel(self, text="Enregistrer un emprunt", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # 1. Récupération des données depuis la BDD
        self.livres_db = self.db_manager.get_all_livres()
        self.membres_db = self.db_manager.get_all_membres()

        # 2. Création des dictionnaires pour lier les noms aux IDs
        self.dict_livres = {f"{l['titre']} ({l['isbn']})": l['id_livre'] for l in self.livres_db} if self.livres_db else {}
        self.dict_membres = {f"{m['nom'].upper()} {m['prenom']}": m['id_membre'] for m in self.membres_db} if self.membres_db else {}

        # 3. Menu déroulant pour les Livres
        noms_livres = list(self.dict_livres.keys()) if self.dict_livres else ["Aucun livre disponible"]
        self.combo_livre = ctk.CTkComboBox(self, values=noms_livres, width=300)
        self.combo_livre.pack(pady=10)
        self.combo_livre.set("Sélectionner un livre" if self.dict_livres else "Aucun livre")

        # 4. Menu déroulant pour les Membres
        noms_membres = list(self.dict_membres.keys()) if self.dict_membres else ["Aucun membre trouvé"]
        self.combo_membre = ctk.CTkComboBox(self, values=noms_membres, width=300)
        self.combo_membre.pack(pady=10)
        self.combo_membre.set("Sélectionner un membre" if self.dict_membres else "Aucun membre")

        # 5. Bouton de validation
        btn_valider = ctk.CTkButton(self, text="Valider l'emprunt", command=self.valider_emprunt, fg_color="green", hover_color="darkgreen", width=300)
        btn_valider.pack(pady=30)

    def valider_emprunt(self):
        livre_selectionne = self.combo_livre.get()
        membre_selectionne = self.combo_membre.get()

        if livre_selectionne not in self.dict_livres or membre_selectionne not in self.dict_membres:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un livre et un membre valides.")
            return

        id_livre = self.dict_livres[livre_selectionne]
        id_membre = self.dict_membres[membre_selectionne]

        # Appel à la base de données
        success, message = self.db_manager.ajouter_emprunt(id_livre, id_membre)

        if success:
            messagebox.showinfo("Succès", message)
            self.callback_maj_tableau() # Rafraîchit le tableau des emprunts
            self.destroy() # Ferme le formulaire
        else:
            messagebox.showerror("Erreur", message)