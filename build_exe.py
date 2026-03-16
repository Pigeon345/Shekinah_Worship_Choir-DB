import PyInstaller.__main__
import os

# Build .exe autonome (single file)
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',  # Pas de console
    '--name=Shekinah_Choir_Manager',
    '--icon=icon.ico',  # Ajouter icône si disponible
    '--add-data=*.db;.',
    '--hidden-import=customtkinter',
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
    '--collect-all=customtkinter',
])

print("✅ EXE généré: dist/Shekinah_Choir_Manager.exe")
print("Lancez-le directement !")
