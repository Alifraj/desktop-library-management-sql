# ui/main_window.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from ui.form_livre import FormulaireLivre
from ui.form_emprunt import FormulaireEmprunt
from ui.form_auteur import FormulaireAuteur  # L'import pour les auteurs

class MainWindow(ctk.CTkToplevel):
    def __init__(self, db_manager, user_info):
        super().__init__()
        
        self.db_manager = db_manager
        self.user_info = user_info
        
        self.title("Système de Gestion - Bibliothèque")
        self.geometry("1000x600")
        self.minsize(800, 500)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # ==================== BARRE LATÉRALE ====================
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Espace flexible
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Bibliothèque", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        self.btn_accueil = ctk.CTkButton(self.sidebar_frame, text="🏠 Accueil", command=self.afficher_accueil)
        self.btn_accueil.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_livres = ctk.CTkButton(self.sidebar_frame, text="📚 Livres", command=self.afficher_livres)
        self.btn_livres.grid(row=2, column=0, padx=20, pady=10)
        
        # <-- NOUVEAU BOUTON AUTEURS -->
        self.btn_auteurs = ctk.CTkButton(self.sidebar_frame, text="✍️ Auteurs", command=self.afficher_auteurs)
        self.btn_auteurs.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_membres = ctk.CTkButton(self.sidebar_frame, text="👥 Membres", command=self.afficher_membres)
        self.btn_membres.grid(row=4, column=0, padx=20, pady=10)
        
        self.btn_emprunts = ctk.CTkButton(self.sidebar_frame, text="🔄 Emprunts", command=self.afficher_emprunts)
        self.btn_emprunts.grid(row=5, column=0, padx=20, pady=10)
        
        role_texte = "Administrateur" if self.user_info['role'] == 'admin' else "Membre"
        self.user_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.user_info['prenom']} {self.user_info['nom']}\n({role_texte})", font=ctk.CTkFont(size=12))
        self.user_label.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="s")
        
        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Déconnexion", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.deconnexion)
        self.btn_logout.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="s")
        
        # ==================== ZONE PRINCIPALE ====================
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        self.page_title = ctk.CTkLabel(self.main_frame, text="Tableau de Bord", font=ctk.CTkFont(size=28, weight="bold"))
        self.page_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.content_area = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_area.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self.afficher_accueil()

    def vider_contenu(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # ==================== VUE : ACCUEIL ====================
    def afficher_accueil(self):
        self.page_title.configure(text="Tableau de Bord")
        self.vider_contenu()

        nb_livres, nb_membres, nb_emprunts = self.db_manager.get_statistiques()

        ctk.CTkLabel(self.content_area, text=f"Bienvenue, {self.user_info['prenom']} !", font=ctk.CTkFont(size=20)).pack(pady=(10, 30))

        cards_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        cards_frame.pack(pady=20)

        card1 = ctk.CTkFrame(cards_frame, width=220, height=130, fg_color="#1f538d", corner_radius=15)
        card1.pack(side="left", padx=15)
        card1.pack_propagate(False)
        ctk.CTkLabel(card1, text="📚 Total Livres", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(card1, text=str(nb_livres), font=ctk.CTkFont(size=36, weight="bold")).pack()

        if self.user_info['role'] == 'admin':
            card2 = ctk.CTkFrame(cards_frame, width=220, height=130, fg_color="#27ae60", corner_radius=15)
            card2.pack(side="left", padx=15)
            card2.pack_propagate(False)
            ctk.CTkLabel(card2, text="👥 Total Membres", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5))
            ctk.CTkLabel(card2, text=str(nb_membres), font=ctk.CTkFont(size=36, weight="bold")).pack()

        titre_emprunt = "⏳ Emprunts en cours" if self.user_info['role'] == 'admin' else "Vos Emprunts"
        valeur_emprunt = str(nb_emprunts) if self.user_info['role'] == 'admin' else "Voir ->"
        
        card3 = ctk.CTkFrame(cards_frame, width=220, height=130, fg_color="#d35400", corner_radius=15)
        card3.pack(side="left", padx=15)
        card3.pack_propagate(False)
        ctk.CTkLabel(card3, text=titre_emprunt, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 5))
        ctk.CTkLabel(card3, text=valeur_emprunt, font=ctk.CTkFont(size=36, weight="bold")).pack()

    # ==================== VUE : LIVRES ====================
    def afficher_livres(self):
        self.page_title.configure(text="Gestion des Livres")
        self.vider_contenu()
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=30, fieldbackground="#2b2b2b", bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#1f538d", foreground="white", relief="flat", font=('Arial', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#14375e')])

        frame_tableau = ctk.CTkFrame(self.content_area)
        frame_tableau.pack(fill="both", expand=True, padx=10, pady=10)

        colonnes = ("id", "titre", "isbn", "annee", "auteur")
        self.tree_livres = ttk.Treeview(frame_tableau, columns=colonnes, show="headings", style="Treeview")
        
        self.tree_livres.heading("id", text="ID")
        self.tree_livres.heading("titre", text="Titre du Livre")
        self.tree_livres.heading("isbn", text="ISBN")
        self.tree_livres.heading("annee", text="Année")
        self.tree_livres.heading("auteur", text="Auteur")
        
        self.tree_livres.column("id", width=50, anchor="center")
        self.tree_livres.column("titre", width=250, anchor="w")
        self.tree_livres.column("isbn", width=120, anchor="center")
        self.tree_livres.column("annee", width=80, anchor="center")
        self.tree_livres.column("auteur", width=150, anchor="w")

        scrollbar = ttk.Scrollbar(frame_tableau, orient="vertical", command=self.tree_livres.yview)
        self.tree_livres.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree_livres.pack(side="left", fill="both", expand=True)

        self.charger_donnees_livres()

        frame_actions = ctk.CTkFrame(self.content_area, fg_color="transparent")
        frame_actions.pack(fill="x", padx=10, pady=10)

        if self.user_info['role'] == 'admin':
            ctk.CTkButton(frame_actions, text="➕ Ajouter", fg_color="green", hover_color="darkgreen", width=120, command=self.ouvrir_form_ajout_livre).pack(side="left", padx=5)
            ctk.CTkButton(frame_actions, text="✏️ Modifier", fg_color="#b8860b", hover_color="#8b6508", width=120, command=self.ouvrir_form_modification_livre).pack(side="left", padx=5)
            ctk.CTkButton(frame_actions, text="🗑️ Supprimer", fg_color="red", hover_color="darkred", width=120, command=self.supprimer_livre_selectionne).pack(side="left", padx=5)

    def charger_donnees_livres(self):
        for item in self.tree_livres.get_children():
            self.tree_livres.delete(item)
            
        livres = self.db_manager.get_all_livres()
        
        if livres:
            for livre in livres:
                auteur_complet = f"{livre['prenom']} {livre['nom']}" if livre['nom'] else "Inconnu"
                self.tree_livres.insert("", "end", values=(
                    livre['id_livre'], livre['titre'], livre['isbn'], livre['annee_publication'], auteur_complet
                ))

    def ouvrir_form_ajout_livre(self):
        FormulaireLivre(self, self.db_manager, self.charger_donnees_livres)

    def ouvrir_form_modification_livre(self):
        selection = self.tree_livres.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord cliquer sur un livre.")
            return
            
        valeurs = self.tree_livres.item(selection[0], "values")
        livre_data = {'id': valeurs[0], 'titre': valeurs[1], 'isbn': valeurs[2], 'annee': valeurs[3], 'auteur': valeurs[4]}
        FormulaireLivre(self, self.db_manager, self.charger_donnees_livres, livre_data)

    def supprimer_livre_selectionne(self):
        selection = self.tree_livres.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord cliquer sur un livre.")
            return
            
        valeurs = self.tree_livres.item(selection[0], "values")
        id_livre, titre_livre = valeurs[0], valeurs[1]
        
        if messagebox.askyesno("Confirmation", f"Voulez-vous supprimer '{titre_livre}' ?"):
            success, message = self.db_manager.supprimer_livre(id_livre)
            messagebox.showinfo("Succès", message) if success else messagebox.showerror("Erreur", message)
            if success: self.charger_donnees_livres()

    # ==================== NOUVELLE VUE : AUTEURS ====================
    def afficher_auteurs(self):
        self.page_title.configure(text="Gestion des Auteurs")
        self.vider_contenu()

        frame_tableau = ctk.CTkFrame(self.content_area)
        frame_tableau.pack(fill="both", expand=True, padx=10, pady=10)

        colonnes = ("id", "nom", "prenom")
        self.tree_auteurs = ttk.Treeview(frame_tableau, columns=colonnes, show="headings", style="Treeview")
        
        self.tree_auteurs.heading("id", text="ID")
        self.tree_auteurs.heading("nom", text="Nom")
        self.tree_auteurs.heading("prenom", text="Prénom")
        
        self.tree_auteurs.column("id", width=80, anchor="center")
        self.tree_auteurs.column("nom", width=250, anchor="w")
        self.tree_auteurs.column("prenom", width=250, anchor="w")

        scrollbar = ttk.Scrollbar(frame_tableau, orient="vertical", command=self.tree_auteurs.yview)
        self.tree_auteurs.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_auteurs.pack(side="left", fill="both", expand=True)

        self.charger_donnees_auteurs()

        frame_actions = ctk.CTkFrame(self.content_area, fg_color="transparent")
        frame_actions.pack(fill="x", padx=10, pady=10)

        # Seul un admin a le droit d'ajouter, modifier ou supprimer des auteurs
        if self.user_info['role'] == 'admin':
            ctk.CTkButton(frame_actions, text="➕ Ajouter", fg_color="green", hover_color="darkgreen", width=120, command=self.ouvrir_form_ajout_auteur).pack(side="left", padx=5)
            ctk.CTkButton(frame_actions, text="✏️ Modifier", fg_color="#b8860b", hover_color="#8b6508", width=120, command=self.ouvrir_form_modification_auteur).pack(side="left", padx=5)
            ctk.CTkButton(frame_actions, text="🗑️ Supprimer", fg_color="red", hover_color="darkred", width=120, command=self.supprimer_auteur_selectionne).pack(side="left", padx=5)

    def charger_donnees_auteurs(self):
        for item in self.tree_auteurs.get_children():
            self.tree_auteurs.delete(item)
            
        auteurs = self.db_manager.get_all_auteurs()
        if auteurs:
            for auteur in auteurs:
                self.tree_auteurs.insert("", "end", values=(
                    auteur['id_auteur'], auteur['nom'].upper(), auteur['prenom'].capitalize()
                ))

    def ouvrir_form_ajout_auteur(self):
        FormulaireAuteur(self, self.db_manager, self.charger_donnees_auteurs)

    def ouvrir_form_modification_auteur(self):
        selection = self.tree_auteurs.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord cliquer sur un auteur.")
            return
            
        valeurs = self.tree_auteurs.item(selection[0], "values")
        auteur_data = {'id': valeurs[0], 'nom': valeurs[1], 'prenom': valeurs[2]}
        FormulaireAuteur(self, self.db_manager, self.charger_donnees_auteurs, auteur_data)

    def supprimer_auteur_selectionne(self):
        selection = self.tree_auteurs.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez d'abord cliquer sur un auteur.")
            return
            
        valeurs = self.tree_auteurs.item(selection[0], "values")
        id_auteur = valeurs[0]
        nom_auteur = f"{valeurs[2]} {valeurs[1]}"
        
        if messagebox.askyesno("Confirmation", f"Voulez-vous supprimer l'auteur '{nom_auteur}' ?"):
            success, message = self.db_manager.supprimer_auteur(id_auteur)
            messagebox.showinfo("Succès", message) if success else messagebox.showerror("Erreur", message)
            if success: self.charger_donnees_auteurs()

    # ==================== VUE : MEMBRES ====================
    def afficher_membres(self):
        self.page_title.configure(text="Gestion des Membres")
        self.vider_contenu()
        
        if self.user_info['role'] != 'admin':
            ctk.CTkLabel(self.content_area, text="🚫 Accès restreint\n\nSection réservée aux administrateurs.", text_color="red", font=ctk.CTkFont(size=16)).pack(pady=80)
            return

        frame_tableau = ctk.CTkFrame(self.content_area)
        frame_tableau.pack(fill="both", expand=True, padx=10, pady=10)

        colonnes = ("id", "nom", "prenom", "email", "telephone", "role")
        self.tree_membres = ttk.Treeview(frame_tableau, columns=colonnes, show="headings", style="Treeview")
        
        self.tree_membres.heading("id", text="ID")
        self.tree_membres.heading("nom", text="Nom")
        self.tree_membres.heading("prenom", text="Prénom")
        self.tree_membres.heading("email", text="Email")
        self.tree_membres.heading("telephone", text="Téléphone")
        self.tree_membres.heading("role", text="Rôle")
        
        self.tree_membres.column("id", width=50, anchor="center")
        self.tree_membres.column("nom", width=120, anchor="w")
        self.tree_membres.column("prenom", width=120, anchor="w")
        self.tree_membres.column("email", width=200, anchor="w")
        self.tree_membres.column("telephone", width=120, anchor="center")
        self.tree_membres.column("role", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tableau, orient="vertical", command=self.tree_membres.yview)
        self.tree_membres.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_membres.pack(side="left", fill="both", expand=True)

        self.charger_donnees_membres()

    def charger_donnees_membres(self):
        for item in self.tree_membres.get_children():
            self.tree_membres.delete(item)
            
        membres = self.db_manager.get_all_membres()
        if membres:
            for m in membres:
                role_format = "Admin" if m['role'] == 'admin' else "Membre"
                self.tree_membres.insert("", "end", values=(
                    m['id_membre'], m['nom'].upper(), m['prenom'].capitalize(), m['email'], m['telephone'], role_format
                ))

    # ==================== VUE : EMPRUNTS ====================
    def afficher_emprunts(self):
        titre = "Tous les Emprunts" if self.user_info['role'] == 'admin' else "Mes Emprunts"
        self.page_title.configure(text=titre)
        self.vider_contenu()

        frame_tableau = ctk.CTkFrame(self.content_area)
        frame_tableau.pack(fill="both", expand=True, padx=10, pady=10)

        colonnes = ("id", "livre", "membre", "date_emprunt", "date_prevue", "statut")
        self.tree_emprunts = ttk.Treeview(frame_tableau, columns=colonnes, show="headings", style="Treeview")
        
        self.tree_emprunts.heading("id", text="ID")
        self.tree_emprunts.heading("livre", text="Livre")
        self.tree_emprunts.heading("membre", text="Emprunteur")
        self.tree_emprunts.heading("date_emprunt", text="Date d'emprunt")
        self.tree_emprunts.heading("date_prevue", text="Retour prévu")
        self.tree_emprunts.heading("statut", text="Statut")
        
        self.tree_emprunts.column("id", width=50, anchor="center")
        self.tree_emprunts.column("livre", width=200, anchor="w")
        self.tree_emprunts.column("membre", width=150, anchor="w")
        self.tree_emprunts.column("date_emprunt", width=100, anchor="center")
        self.tree_emprunts.column("date_prevue", width=100, anchor="center")
        self.tree_emprunts.column("statut", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tableau, orient="vertical", command=self.tree_emprunts.yview)
        self.tree_emprunts.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_emprunts.pack(side="left", fill="both", expand=True)

        self.charger_donnees_emprunts()

        frame_actions_emprunts = ctk.CTkFrame(self.content_area, fg_color="transparent")
        frame_actions_emprunts.pack(fill="x", padx=10, pady=10)

        if self.user_info['role'] == 'admin':
            ctk.CTkButton(frame_actions_emprunts, text="➕ Nouvel Emprunt", fg_color="green", hover_color="darkgreen", width=180, command=self.ouvrir_form_emprunt).pack(side="left", padx=5)
            ctk.CTkButton(frame_actions_emprunts, text="📥 Marquer comme rendu", fg_color="#b8860b", hover_color="#8b6508", width=180, command=self.rendre_emprunt_selectionne).pack(side="left", padx=5)

    def charger_donnees_emprunts(self):
        for item in self.tree_emprunts.get_children():
            self.tree_emprunts.delete(item)
            
        id_filtre = None if self.user_info['role'] == 'admin' else self.user_info['id_membre']
        emprunts = self.db_manager.get_emprunts(id_filtre)
        
        if emprunts:
            for e in emprunts:
                emprunteur = f"{e['prenom'].capitalize()} {e['nom'].upper()}"
                statut = f"✅ Rendu ({e['date_retour_effective']})" if e['date_retour_effective'] else "⏳ En cours"
                self.tree_emprunts.insert("", "end", values=(
                    e['id_emprunt'], e['livre'], emprunteur, e['date_emprunt'], e['date_retour_prevue'], statut
                ))

    def rendre_emprunt_selectionne(self):
        selection = self.tree_emprunts.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Veuillez cliquer sur un emprunt.")
            return
            
        valeurs = self.tree_emprunts.item(selection[0], "values")
        if "Rendu" in valeurs[5]:
            messagebox.showinfo("Information", "Ce livre a déjà été rendu.")
            return
            
        if messagebox.askyesno("Confirmation", "Valider le retour de ce livre ?"):
            success, message = self.db_manager.rendre_livre(valeurs[0])
            messagebox.showinfo("Succès", message) if success else messagebox.showerror("Erreur", message)
            if success: self.charger_donnees_emprunts()

    def ouvrir_form_emprunt(self):
        FormulaireEmprunt(self, self.db_manager, self.charger_donnees_emprunts)

    def deconnexion(self):
        self.master.deiconify()
        self.destroy()