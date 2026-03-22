import PyInstaller.__main__
import os

# Build .exe autonome (single file)
PyInstaller.__main__.run([
    'runp.py',
    '--onefile',
    '--windowed',  # Pas de console
    '--name=Shekinah_Choir_Manager',
    # '--icon=icon.ico',  # Décommenter si icône disponible
    '--add-data=shekinah_choir.db;.',
    '--hidden-import=customtkinter',
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
    '--hidden-import=sqlite3',
    '--hidden-import=matplotlib',
    '--collect-all=customtkinter',
])

print("✅ EXE généré: dist/Shekinah_Choir_Manager.exe")
print("Lancez-le directement !")
