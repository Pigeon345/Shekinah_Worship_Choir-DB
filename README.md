# Shekinah Worship Choir - App Desktop Moderne

## 🎵 App Gestion Chœur Professionnelle

**GUI CustomTkinter (Dark Mode Win11 style)** + SQLite + Exports Excel + .exe autonome.

## 🚀 Installation
```
pip install -r requirements.txt
python database.py  # Init DB
python main.py  # Lancer GUI
```

## 📱 Interface
- **👥 Membres**: Add/list par pupitre, statut, commentaires coach.
- **💰 Caisse**: Cotisations/dons/solde live (DB prête).
- **📊 Rapports**: Excel membres/caisse.
- **📈 Dashboard**: Stats/solde.

## 🔨 Build .exe
```
pip install pyinstaller
python build_exe.py
→ dist/Shekinah_Choir_Manager.exe
```

## 🗄️ DB (shekinah_choir.db)
- membres (statut ajouté)
- caisse (cotisations, dons, dépenses)
- chansons, presences, roles...

**Fonctionnel & prêt !** Testez `python main.py` après pip. Gloire à Dieu ! 🙌
