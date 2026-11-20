# ui/form_livre.py
import customtkinter as ctk
from tkinter import messagebox

class FormulaireLivre(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, callback_maj_tableau, livre_data=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.callback_maj_tableau = callback_maj_tableau
        
        # Si livre_data contient des infos, on est en mode MODIFICATION, sinon en mode AJOUT
        self.livre_data = livre_data 

        titre_fenetre = "Modifier le livre" if self.livre_data else "Ajouter un nouveau livre"
        self.title(titre_fenetre)
        self.geometry("400x450")
        self.resizable(False, False)
        self.grab_set() 

        ctk.CTkLabel(self, text=titre_fenetre, font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Champs de saisie
        self.entry_titre = ctk.CTkEntry(self, placeholder_text="Titre du livre", width=250)
        self.entry_titre.pack(pady=10)

        self.entry_isbn = ctk.CTkEntry(self, placeholder_text="ISBN (ex: 978-1234567890)", width=250)
        self.entry_isbn.pack(pady=10)

        self.entry_annee = ctk.CTkEntry(self, placeholder_text="Année de publication", width=250)
        self.entry_annee.pack(pady=10)

        # Menu déroulant pour les auteurs
        self.auteurs_db = self.db_manager.get_all_auteurs()
        self.dict_auteurs = {} 
        noms_auteurs = []
        
        if self.auteurs_db:
            for a in self.auteurs_db:
                nom_complet = f"{a['nom']} {a['prenom']}"
                self.dict_auteurs[nom_complet] = a['id_auteur']
                noms_auteurs.append(nom_complet)
        else:
            noms_auteurs = ["Aucun auteur trouvé"]

        self.combo_auteur = ctk.CTkComboBox(self, values=noms_auteurs, width=250)
        self.combo_auteur.pack(pady=10)
        self.combo_auteur.set("Sélectionner un auteur" if self.auteurs_db else "Aucun auteur trouvé")

        # =================================================================
        # PRÉ-REMPLISSAGE DES CHAMPS SI ON EST EN MODE MODIFICATION
        # =================================================================
        if self.livre_data:
            self.entry_titre.insert(0, self.livre_data['titre'])
            self.entry_isbn.insert(0, self.livre_data['isbn'])
            self.entry_annee.insert(0, self.livre_data['annee'])
            self.combo_auteur.set(self.livre_data['auteur'])

        # Bouton
        texte_bouton = "Mettre à jour" if self.livre_data else "Enregistrer"
        btn_valider = ctk.CTkButton(self, text=texte_bouton, command=self.valider_formulaire, fg_color="#b8860b" if self.livre_data else "green", hover_color="#8b6508" if self.livre_data else "darkgreen", width=250)
        btn_valider.pack(pady=30)

    def valider_formulaire(self):
        titre = self.entry_titre.get().strip()
        isbn = self.entry_isbn.get().strip()
        annee = self.entry_annee.get().strip()
        auteur_selectionne = self.combo_auteur.get()

        if not titre or not isbn or not annee:
            messagebox.showwarning("Erreur", "Veuillez remplir le titre, l'ISBN et l'année.")
            return
            
        if not annee.isdigit():
            messagebox.showwarning("Erreur", "L'année doit être un nombre.")
            return

        if auteur_selectionne not in self.dict_auteurs:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un auteur valide.")
            return

        id_auteur = self.dict_auteurs[auteur_selectionne]

        # Choix de l'action selon le mode (Ajout ou Modification)
        if self.livre_data:
            # On passe l'ID du livre stocké au moment de l'ouverture
            success, message = self.db_manager.modifier_livre(self.livre_data['id'], titre, isbn, int(annee), id_auteur)
        else:
            success, message = self.db_manager.ajouter_livre(titre, isbn, int(annee), id_auteur)

        if success:
            messagebox.showinfo("Succès", message)
            self.callback_maj_tableau() 
            self.destroy() 
        else:
            messagebox.showerror("Erreur", message)