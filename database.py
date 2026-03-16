import sqlite3
import os
from datetime import date

def init_db():
    """
    Initialise la DB Shekinah Worship v2.0 avec toutes les tables + champs Master Prompt.
    """
    db_path = 'shekinah_choir.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Table membres (Master Prompt: +statut, date_adhesion)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS membres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            pupitre TEXT NOT NULL CHECK(pupitre IN ('Soprano', 'Alto', 'Tenor', 'Basse')),
            telephone TEXT,
            email TEXT,
            date_adhesion DATE DEFAULT (date('now')),
            commentaires_coach TEXT,
            statut TEXT DEFAULT 'Actif' CHECK(statut IN ('Actif', 'Stagiaire', 'Suspendu')),
            actif BOOLEAN DEFAULT 1
        )
    ''')
    
    # Ajout champs si table existe déjà (idempotent)
    cursor.execute("PRAGMA table_info(membres)")
    cols = [row[1] for row in cursor.fetchall()]
    if 'statut' not in cols:
        cursor.execute("ALTER TABLE membres ADD COLUMN statut TEXT DEFAULT 'Actif'")
    if 'date_adhesion' not in cols:
        # Change ta ligne par celle-ci :
        cursor.execute("ALTER TABLE membres ADD COLUMN date_adhesion DATE DEFAULT '2026-01-01'")
    
    # Table finances (membre_id FK)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            membre_id INTEGER,
            montant REAL NOT NULL CHECK(montant >= 0),
            type TEXT NOT NULL CHECK(type IN ('Cotisation', 'Don')),
            motif TEXT,
            date_paiement DATE DEFAULT (date('now')),
            FOREIGN KEY (membre_id) REFERENCES membres(id)
        )
    ''')
    
    # Table communiques
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS communiques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            contenu TEXT,
            date_publication DATE DEFAULT (date('now')),
            priorite TEXT DEFAULT 'Normal' CHECK(priorite IN ('Normal', 'Urgent', 'Info'))
        )
    ''')
    
    # Tables existantes conservées
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chansons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            artiste TEXT,
            duree TEXT,
            type_chanson TEXT,
            partition_pdf_path TEXT,
            date_ajoutee DATE DEFAULT (date('now'))
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            membre_id INTEGER,
            seance_date DATE,
            present BOOLEAN DEFAULT 0,
            commentaire TEXT,
            FOREIGN KEY (membre_id) REFERENCES membres (id)
        )
    ''')
    
    # Index optimisés
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_membres_pupitre ON membres(pupitre)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_finances_membre_date ON finances(membre_id, date_paiement)')
    
    # Données exemples
    cursor.execute("INSERT OR IGNORE INTO membres (nom, pupitre, telephone, statut) VALUES "
                  "('Exemple1', 'Soprano', '+243999', 'Actif'), "
                  "('Exemple2', 'Tenor', '+243888', 'Stagiaire')")
    cursor.execute("INSERT OR IGNORE INTO finances (membre_id, montant, type, motif) VALUES "
                  "(1, 50000, 'Cotisation', 'Mensuelle'), "
                  "(1, 20000, 'Don', 'Offrande special')")
    cursor.execute("INSERT OR IGNORE INTO communiques (titre, contenu, priorite) VALUES "
                  "('Répétition', 'Vendredi 20h Eglise', 'Urgent'), "
                  "('Nouveau Chant', 'Apprendre Hosanna', 'Normal')")
    
    conn.commit()
    conn.close()
    print(f"✅ DB Shekinah v2.0 initialisée: {db_path}")
    print("Nouvelles tables: finances, communiques | Membres+statut/date_adhesion")

if __name__ == "__main__":
    init_db()
