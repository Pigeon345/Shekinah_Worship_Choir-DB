#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Point d'entrée principal pour la gestion de la base de données Shekinah Worship Choir.
Initialise la DB si nécessaire, puis lance le menu interactif.
"""

import sys

def main():
    """Lance l'application GUI Shekinah Choir."""
    try:
        from database import init_db
        from main import ShekinahApp

        # Initialiser DB si nécessaire
        print("🚀 Initialisation base de données...")
        init_db()

        # Lancer GUI
        print("🎵 Lancement Shekinah Worship Choir Manager...")
        app = ShekinahApp()
        app.mainloop()

    except ImportError as e:
        print(f"❌ Erreur import: {e}")
        print("📦 Installe les dépendances: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
