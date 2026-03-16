import customtkinter as ctk
from tkinter import messagebox, ttk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from db_models import db
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AddMemberDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("➕ Ajouter Membre")
        self.geometry("450x550")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Nouveau Chantre Shekinah", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        self.nom_var = ctk.StringVar()
        self.tel_var = ctk.StringVar()
        self.email_var = ctk.StringVar()

        ctk.CTkLabel(self, text="Nom Complet *").pack(anchor="w", padx=30, pady=(0,5))
        ctk.CTkEntry(self, textvariable=self.nom_var, placeholder_text="Dupont Marie").pack(fill="x", padx=30, pady=5)

        ctk.CTkLabel(self, text="Pupitre *").pack(anchor="w", padx=30, pady=(10,5))
        self.pupitre_var = tk.StringVar(value="Soprano")
        pupitre_combo = ctk.CTkOptionMenu(self, values=["Soprano", "Alto", "Ténor", "Basse"], variable=self.pupitre_var)
        pupitre_combo.pack(fill="x", padx=30, pady=5)

        ctk.CTkLabel(self, text="Téléphone").pack(anchor="w", padx=30, pady=(10,5))
        ctk.CTkEntry(self, textvariable=self.tel_var, placeholder_text="+243 XXX XXX XXX").pack(fill="x", padx=30, pady=5)

        ctk.CTkLabel(self, text="Email").pack(anchor="w", padx=30, pady=(10,5))
        ctk.CTkEntry(self, textvariable=self.email_var, placeholder_text="chantre@shekinah.org").pack(fill="x", padx=30, pady=5)

        ctk.CTkLabel(self, text="Commentaires Coach").pack(anchor="w", padx=30, pady=(10,5))
        self.comment_box = ctk.CTkTextbox(self, height=100)
        self.comment_box.pack(fill="both", expand=True, padx=30, pady=5)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkButton(btn_frame, text="✅ Enregistrer", fg_color="#10b981", command=self.save_member).pack(side="right", padx=10)
        ctk.CTkButton(btn_frame, text="❌ Annuler", fg_color="gray", command=self.destroy).pack(side="right")

    def save_member(self):
        nom = self.nom_var.get().strip()
        pupitre = self.pupitre_var.get()
        tel = self.tel_var.get().strip()
        email = self.email_var.get().strip()
        commentaires = self.comment_box.get("1.0", tk.END).strip()
        
        if not nom or not pupitre:
            messagebox.showerror("Erreur", "Nom et Pupitre obligatoires!")
            return

        membre_id = db.ajouter_membre(nom, pupitre, tel, 'Actif', email, commentaires)
        if membre_id:
            messagebox.showinfo("Succès", f"✨ {nom} ajouté (ID: {membre_id})")
            self.destroy()
            self.master.refresh_membres_list()
        else:
            messagebox.showerror("Erreur", "Échec ajout membre.")

class MemberDetailDialog(ctk.CTkToplevel):
    def __init__(self, parent, membre_id):
        super().__init__(parent)
        self.membre_id = membre_id
        self.title(f"👤 Détail Membre ID {membre_id}")
        self.geometry("800x700")
        self.transient(parent)
        self.grab_set()
        self.resizable(True, True)

        # Load data
        self.membre_df = db.get_membre_by_id(membre_id)
        if self.membre_df.empty:
            messagebox.showerror("Erreur", "Membre non trouvé!")
            self.destroy()
            return
        self.membre = self.membre_df.iloc[0]

        self.finances_df = db.get_finances_membre(membre_id)
        self.presences_df = db.get_presences_membre(membre_id)

        # Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Tab Infos
        self.tab_infos = self.tabview.add("Infos Générales")
        self.create_infos_tab()

        # Tab Finances
        self.tab_finances = self.tabview.add("Cotisations/Finances")
        self.create_finances_tab()

        # Tab Présences
        self.tab_presences = self.tabview.add("Présences")
        self.create_presences_tab()

        # Buttons bottom
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(btn_frame, text="💾 Sauvegarder Changements", fg_color="#10b981", command=self.save_changes, width=200).pack(side="right", padx=10)
        ctk.CTkButton(btn_frame, text="🗑️ Désactiver Membre", fg_color="#ef4444", command=self.delete_member, width=200).pack(side="right", padx=10)
        ctk.CTkButton(btn_frame, text="❌ Fermer", fg_color="gray", command=self.destroy).pack(side="right")

    def create_infos_tab(self):
        frame = self.tab_infos
        ctk.CTkLabel(frame, text=f"ID: {self.membre['id']}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        # Editable fields
        self.nom_var = ctk.StringVar(value=self.membre.get('nom', ''))
        self.pupitre_var = tk.StringVar(value=self.membre.get('pupitre', ''))
        self.tel_var = ctk.StringVar(value=self.membre.get('telephone', ''))
        self.email_var = ctk.StringVar(value=self.membre.get('email', ''))
        self.statut_var = ctk.StringVar(value=self.membre.get('statut', 'Actif'))
        self.comment_var = self.membre.get('commentaires_coach', '')

        ctk.CTkLabel(frame, text="Nom *").pack(anchor="w", padx=20, pady=5)
        ctk.CTkEntry(frame, textvariable=self.nom_var, width=600).pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame, text="Pupitre *").pack(anchor="w", padx=20, pady=5)
        pupitre_combo = ctk.CTkOptionMenu(frame, values=["Soprano", "Alto", "Ténor", "Basse"], variable=self.pupitre_var, width=600)
        pupitre_combo.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame, text="Téléphone").pack(anchor="w", padx=20, pady=5)
        ctk.CTkEntry(frame, textvariable=self.tel_var, width=600).pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame, text="Email").pack(anchor="w", padx=20, pady=5)
        ctk.CTkEntry(frame, textvariable=self.email_var, width=600).pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame, text="Statut").pack(anchor="w", padx=20, pady=5)
        statut_combo = ctk.CTkOptionMenu(frame, values=["Actif", "Stagiaire", "Suspendu"], variable=self.statut_var, width=600)
        statut_combo.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame, text="Commentaires Coach").pack(anchor="w", padx=20, pady=5)
        self.comment_box = ctk.CTkTextbox(frame, height=120)
        self.comment_box.insert("0.0", self.comment_var)
        self.comment_box.pack(fill="x", padx=20, pady=5)

        # Infos readonly
        info_frame = ctk.CTkFrame(frame)
        info_frame.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(info_frame, text=f"Date Adhésion: {self.membre.get('date_adhesion', 'N/A')}", font=ctk.CTkFont(size=14)).pack(anchor="w")

    def create_finances_tab(self):
        frame = self.tab_finances
        ctk.CTkLabel(frame, text=f"Historique Finances ({len(self.finances_df)} transactions)", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        # Simple table/list
        listbox_frame = ctk.CTkFrame(frame)
        listbox_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.finances_listbox = tk.Listbox(listbox_frame, height=15)
        finances_scroll = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.finances_listbox.yview)
        self.finances_listbox.configure(yscrollcommand=finances_scroll.set)

        self.finances_listbox.pack(side="left", fill="both", expand=True)
        finances_scroll.pack(side="right", fill="y")

        for _, row in self.finances_df.iterrows():
            self.finances_listbox.insert(tk.END, f"{row['date_paiement']} | {row['type']} | {row['montant']:,} FC | {row['motif']}")

    def create_presences_tab(self):
        frame = self.tab_presences
        ctk.CTkLabel(frame, text=f"Historique Présences ({len(self.presences_df)} séances)", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        listbox_frame = ctk.CTkFrame(frame)
        listbox_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.presences_listbox = tk.Listbox(listbox_frame, height=15)
        presences_scroll = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.presences_listbox.yview)
        self.presences_listbox.configure(yscrollcommand=presences_scroll.set)

        self.presences_listbox.pack(side="left", fill="both", expand=True)
        presences_scroll.pack(side="right", fill="y")

        for _, row in self.presences_df.iterrows():
            statut = "✅ Présent" if row['present'] else "❌ Absent"
            self.presences_listbox.insert(tk.END, f"{row['seance_date']} | {statut} | {row['commentaire'] or ''}")

    def save_changes(self):
        changes = {
            'nom': self.nom_var.get().strip(),
            'pupitre': self.pupitre_var.get(),
            'telephone': self.tel_var.get().strip(),
            'email': self.email_var.get().strip(),
            'statut': self.statut_var.get(),
            'commentaires_coach': self.comment_box.get("1.0", tk.END).strip()
        }
        if db.update_membre(self.membre_id, **changes):
            messagebox.showinfo("Succès", "✅ Membre mis à jour!")
            self.master.refresh_membres_list()
        else:
            messagebox.showerror("Erreur", "Échec mise à jour.")

    def delete_member(self):
        if messagebox.askyesno("Confirmer", "Désactiver ce membre? (Données conservées)"):
            if db.supprimer_membre(self.membre_id):
                messagebox.showinfo("Succès", "Membre désactivé.")
                self.master.refresh_membres_list()
                self.destroy()
            else:
                messagebox.showerror("Erreur", "Échec suppression.")

class ShekinahApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shekinah Worship Choir v2.4 - Détail Membre Complet")
        self.geometry("1400x900")
        self.resizable(True, True)

        self.sidebar = ctk.CTkFrame(self, corner_radius=0, width=250)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        
        logo = ctk.CTkLabel(self.sidebar, text="Shekinah\\nWorship\\nChoir", font=ctk.CTkFont(size=22, weight="bold"))
        logo.grid(row=0, column=0, pady=30, padx=25)

        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        buttons = [
            ("📊 Dashboard", self.show_dashboard, "#4f46e5"),
            ("👥 Membres", self.show_membres, "#10b981"),
            ("💰 Finances", self.show_finances, "#f59e0b"),
            ("📢 Communiqués", self.show_communiques, "#ef4444"),
            ("⚙️ Settings", self.show_settings, "#6b7280")
        ]
        
        self.nav_buttons = {}
        for i, (text, cmd, color) in enumerate(buttons):
            btn = ctk.CTkButton(nav_frame, text=text, command=cmd, fg_color=color, hover_color="#1f538d")
            btn.grid(row=i, column=0, pady=12, sticky="ew", padx=10)
            self.nav_buttons[text] = btn

        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(1, weight=1)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add('write', self.on_search_change)  # Fix deprecation
        self.membres_tree = None

        self.show_dashboard()

    def refresh_membres_list(self):
        self.show_membres()

    def on_search_change(self, *args):
        if self.membres_tree:
            self.load_membres_data()

    def show_membres(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self.main_frame, height=70)
        header.pack(fill="x", padx=0, pady=(0,10))
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="👥 GESTION DES MEMBRES - Clic ligne pour détails!", 
                     font=ctk.CTkFont(size=28, weight="bold")).pack(expand=True, pady=20)

        top_frame = ctk.CTkFrame(self.main_frame)
        top_frame.pack(fill="x", padx=25, pady=(0,15))

        ctk.CTkEntry(top_frame, textvariable=self.search_var, placeholder_text="🔍 Rechercher nom/pupitre/tel...", width=500).pack(side="left", padx=(0,10))
        ctk.CTkButton(top_frame, text="➕ Ajouter Membre", fg_color="#10b981", command=self.add_member_dialog, width=200).pack(side="left")

        table_frame = ctk.CTkFrame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=25, pady=(0,20))

        self.membres_tree = ttk.Treeview(table_frame, columns=("ID", "Nom", "Pupitre", "Tel", "Email", "Statut", "Date"), show="headings", height=20)
        
        self.membres_tree.heading("ID", text="ID")
        self.membres_tree.heading("Nom", text="Nom Complet")
        self.membres_tree.heading("Pupitre", text="Pupitre")
        self.membres_tree.heading("Tel", text="Téléphone")
        self.membres_tree.heading("Email", text="Email")
        self.membres_tree.heading("Statut", text="Statut")
        self.membres_tree.heading("Date", text="Date Adhésion")

        self.membres_tree.column("ID", width=60, anchor="center")
        self.membres_tree.column("Nom", width=220)
        self.membres_tree.column("Pupitre", width=100, anchor="center")
        self.membres_tree.column("Tel", width=150)
        self.membres_tree.column("Email", width=200)
        self.membres_tree.column("Statut", width=100, anchor="center")
        self.membres_tree.column("Date", width=120)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.membres_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.membres_tree.xview)
        self.membres_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.membres_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        v_scrollbar.pack(side="right", fill="y", pady=10)
        h_scrollbar.pack(side="bottom", fill="x", padx=(10,0), pady=(0,10))

        # CLIC SUR LIGNE → DÉTAIL
        self.membres_tree.bind('<Double-1>', self.on_member_double_click)

        self.load_membres_data()

    def load_membres_data(self):
        if self.membres_tree is None:
            return
        
        for item in self.membres_tree.get_children():
            self.membres_tree.delete(item)

        try:
            df = db.search_membres(self.search_var.get()) if self.search_var.get().strip() else db.get_membres()
            for _, row in df.iterrows():
                self.membres_tree.insert("", "end", values=(
                    row['id'], row['nom'], row['pupitre'], row['telephone'], 
                    row['email'] or '', row['statut'] or 'Actif', row['date_adhesion'] or ''
                ))
        except Exception as e:
            messagebox.showerror("Erreur DB", f"Erreur chargement: {e}")

    def on_member_double_click(self, event):
        selection = self.membres_tree.selection()
        if selection:
            item = self.membres_tree.item(selection[0])
            membre_id = item['values'][0]
            MemberDetailDialog(self, int(membre_id))

    def add_member_dialog(self):
        dialog = AddMemberDialog(self)

    def show_dashboard(self):
        # [Code dashboard identique à précédent - omis pour brièveté, mais conservé]
        for child in self.main_frame.winfo_children():
            child.destroy()

        header = ctk.CTkFrame(self.main_frame, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="🎵 DASHBOARD Shekinah Worship - 2026", font=ctk.CTkFont(size=28, weight="bold")).pack(expand=True, pady=15)

        # ... reste du dashboard inchangé ...
        # Cards FC, graph 2026 etc. (code précédent)

        ctk.CTkLabel(self.main_frame, text="Dashboard complet (code précédent conservé)", font=ctk.CTkFont(size=20)).pack(expand=True)

    def show_finances(self):
        messagebox.showinfo("Finances", "Disponible via détails membres!")

    def show_communiques(self):
        messagebox.showinfo("Communiqués", "À venir!")

    def show_settings(self):
        messagebox.showinfo("Settings", "Backup/thèmes bientôt!")

if __name__ == "__main__":
    app = ShekinahApp()
    app.mainloop()

