-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_bibliotheque;
USE gestion_bibliotheque;

-- 1. Table des Auteurs
CREATE TABLE Auteurs (
    id_auteur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL
);

-- 2. Table des Livres
CREATE TABLE Livres (
    id_livre INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    annee_publication INT,
    id_auteur INT,
    FOREIGN KEY (id_auteur) REFERENCES Auteurs(id_auteur) ON DELETE SET NULL
);

-- 3. Table des Membres (Mise à jour avec authentification)
CREATE TABLE Membres (
    id_membre INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20),
    mot_de_passe VARCHAR(255) NOT NULL, -- Stockera le mot de passe haché
    role VARCHAR(50) DEFAULT 'membre'   -- 'admin' ou 'membre'
);

-- 4. Table des Emprunts
CREATE TABLE Emprunts (
    id_emprunt INT AUTO_INCREMENT PRIMARY KEY,
    id_livre INT NOT NULL,
    id_membre INT NOT NULL,
    date_emprunt DATE NOT NULL,
    date_retour_prevue DATE NOT NULL,
    date_retour_effective DATE,
    FOREIGN KEY (id_livre) REFERENCES Livres(id_livre) ON DELETE CASCADE,
    FOREIGN KEY (id_membre) REFERENCES Membres(id_membre) ON DELETE CASCADE
);

-- ==========================================
-- INSERTION DES DONNÉES DE TEST
-- ==========================================

INSERT INTO Auteurs (nom, prenom) VALUES 
('Hugo', 'Victor'),
('Asimov', 'Isaac'),
('Lovelace', 'Ada');

INSERT INTO Livres (titre, isbn, annee_publication, id_auteur) VALUES 
('Les Misérables', '978-2070409228', 1862, 1),
('Fondation', '978-2070360536', 1951, 2),
('I, Robot', '978-0553294385', 1950, 2);

-- Ajout de membres avec mots de passe hachés (Le mot de passe en clair est 'password123' pour les deux)
-- Le hash SHA-256 de 'password123' est 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'
INSERT INTO Membres (nom, prenom, email, telephone, mot_de_passe, role) VALUES 
('Admin', 'Principal', 'admin@bibliotheque.com', '0000000000', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'admin'),
('Dupont', 'Marie', 'marie.dupont@email.com', '0601020304', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'membre');

INSERT INTO Emprunts (id_livre, id_membre, date_emprunt, date_retour_prevue, date_retour_effective) VALUES 
(2, 2, '2026-03-20', '2026-04-03', NULL);