# 📚 Système de Gestion de Bibliothèque (Library Management System)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-green.svg)
![Security](https://img.shields.io/badge/Security-bcrypt-red.svg)

## 📖 À propos du projet

Ce projet est une application de bureau complète développée en **Python** pour la gestion informatisée d'une bibliothèque. Il propose une interface utilisateur moderne et sombre (Dark Mode) et repose sur une architecture logicielle modulaire séparant proprement l'interface graphique (UI) de l'accès aux données (Base de données).

L'application intègre un système de sécurité avancé avec hachage des mots de passe et un contrôle d'accès basé sur les rôles (**RBAC**), permettant des vues et des actions différentes selon si l'utilisateur est un Administrateur ou un simple Membre.

## ✨ Fonctionnalités Principales

* **🔒 Authentification Sécurisée :** Connexion et inscription avec hachage des mots de passe via `bcrypt` (protection contre les fuites de données).
* **👥 Gestion des Rôles (RBAC) :**
    * *Administrateur :* Accès total (CRUD complet sur les livres, membres, auteurs et emprunts).
    * *Membre :* Accès en lecture seule au catalogue et visualisation de ses propres emprunts.
* **📊 Tableau de Bord (Dashboard) :** Vue d'ensemble avec des statistiques en temps réel (Total des livres, membres, emprunts actifs).
* **📚 Gestion du Catalogue (CRUD) :** Ajout, modification, et suppression de livres et d'auteurs avec vérification des doublons (ISBN).
* **🔄 Système d'Emprunt Intelligent :** * Attribution de livres aux membres avec calcul automatique de la date de retour prévue (+14 jours).
    * Validation des retours en un clic.
* **🎨 Interface UI/UX Moderne :** Conçue avec `CustomTkinter` pour une expérience fluide, responsive et agréable à l'œil.

## 🛠️ Technologies Utilisées

* **Langage :** Python 3
* **Interface Graphique :** CustomTkinter & Tkinter (Treeview)
* **Base de Données :** MySQL
* **Sécurité :** `bcrypt` (Salage et hachage cryptographique)
* **Connecteur BDD :** `mysql-connector-python`

## 📂 Architecture du Projet

Le projet suit une architecture modulaire pour une meilleure maintenabilité :

```text
📁 bibliotheque_app/
│
├── 📄 main.py                 # Point d'entrée de l'application
├── 📄 db_manager.py           # Gestionnaire de base de données (Requêtes SQL)
├── 📄 config.py               # Identifiants de connexion MySQL (Fichier de configuration)
├── 📄 schema.sql              # Script de création de la base de données et des tables
│
└── 📁 ui/                     # Dossier contenant toutes les vues (Interface Utilisateur)
    ├── 📄 login_window.py     # Fenêtre de connexion
    ├── 📄 signup_window.py    # Fenêtre d'inscription
    ├── 📄 main_window.py      # Tableau de bord principal (Dashboard & Tableaux)
    ├── 📄 form_livre.py       # Fenêtre modale : Ajout/Modification de Livre
    ├── 📄 form_auteur.py      # Fenêtre modale : Ajout/Modification d'Auteur
    └── 📄 form_emprunt.py     # Fenêtre modale : Nouvel Emprunt