#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Point d'entrée principal pour la gestion de la base de données Shekinah Worship Choir.
Initialise la DB si nécessaire, puis lance le menu interactif.
"""

import pandas as pd
import os
import sys
from datetime import datetime
import sqlite3

# Importer nos modules
try:
    from database import init_db
    import app as choir_app  # Sera amélioré
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assure-toi d'avoir installé les dépendances: pip install -r requirements.txt")
    sys.exit(1)

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("🎵 BASE DE DONNÉES SHEKINAH WORSHIP CHOIR 🎵")
        print("="*50)
        print("1. 👥 Gérer les membres (ajouter, lister, modifier)")
        print("2. 🎤 Gérer le répertoire (ajouter chanson)")
        print("3. 📊 Rapport Excel (membres, présences)")
        print("4. 🗓️  Enregistrer présences")
        print("5. 🔄 Initialiser/Reset DB")
        print("0. ❌ Quitter")
        choix = input("\nVotre choix (0-5): ").strip()

        if choix == '1':
            gerer_membres()
        elif choix == '2':
            gerer_chansons()
        elif choix == '3':
            generer_rapports()
        elif choix == '4':
            enregistrer_presence()
        elif choix == '5':
            init_db()
        elif choix == '0':
            print("👋 Au revoir ! Gloire à Dieu !")
            break
        else:
            print("❌ Choix invalide !")

def gerer_membres():
    print("\n👥 GESTION MEMBRES")
    print("a) Ajouter | l) Lister | m) Modifier")
    action = input("Action (a/l/m): ").lower()
    if action == 'a':
        nom = input("Nom: ")
        pupitre = input("Pupitre (Soprano/Alto/Tenor/Basse): ")
        tel = input("Téléphone: ")
        email = input("Email (optionnel): ")
        comm = input("Commentaires coach (optionnel): ")
        choir_app.ajouter_membre(nom, pupitre, tel, comm)
        # Note: email ajouté dans DB, mais fonction app.py à updater
    elif action == 'l':
        lister_membres()
    elif action == 'm':
        print("Modification à implémenter.")

def lister_membres():
    conn = choir_app.connecter_db()
    df = pd.read_sql_query("SELECT * FROM membres WHERE actif=1 ORDER BY pupitre, nom", conn)
    conn.close()
    print(df.to_string(index=False))
    input("Appuyez sur Entrée...")

# Autres fonctions (placeholders pour l'instant)
def gerer_chansons():
    print("\n🎤 Ajout chanson")
    titre = input("Titre: ")
    artiste = input("Artiste: ")
    duree = input("Durée (MM:SS): ")
    type_c = input("Type (Louange/Adoration/Autre): ")
    path = input("Chemin partition PDF (optionnel): ")
    ajouter_chanson(titre, artiste, duree, type_c, path)

def ajouter_chanson(titre, artiste, duree, type_c, path):
    conn = choir_app.connecter_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chansons (titre, artiste, duree, type_chanson, partition_pdf_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (titre, artiste, duree, type_c, path))
    conn.commit()
    conn.close()
    print(f"✨ Chanson '{titre}' ajoutée !")

def generer_rapports():
    print("\n📊 Rapports")
    choir_app.exporter_vers_excel("membres", "Rapport_Membres_Shekinah")
    # Plus à ajouter

def enregistrer_presence():
    print("\n🗓️ Présences")
    lister_membres()
    membre_id = int(input("ID membre: "))
    date = input("Date (YYYY-MM-DD) ou aujourd'hui: ") or datetime.now().strftime("%Y-%m-%d")
    present = input("Présent (o/n): ").lower() == 'o'
    comm = input("Commentaire: ")
    conn = choir_app.connecter_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO presences (membre_id, seance_date, present, commentaire)
        VALUES (?, ?, ?, ?)
    ''', (membre_id, date, present, comm))
    conn.commit()
    conn.close()
    print("✅ Présence enregistrée !")

if __name__ == "__main__":
    print("🚀 Lancement Shekinah Choir DB...")
    init_db()  # Assure DB prête
    menu_principal()
