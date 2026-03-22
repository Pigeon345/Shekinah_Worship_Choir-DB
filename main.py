#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shekinah Worship Choir Manager v3.0
GUI Desktop - CustomTkinter (dark mode)
Point d'entrée UNIQUE pour l'application
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from db_models import db
import tkinter as tk
import io
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ============================================
# UTILITY FUNCTIONS
# ============================================

def center_dialog(dialog, width, height):
    """Centre un dialogue sur l'écran"""
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    dialog.geometry(f"{width}x{height}+{x}+{y}")

# ============================================
# DIALOG CLASSES
# ============================================

class AddMemberDialog(ctk.CTkToplevel):
    """Dialogue d'ajout d'un nouveau membre"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("➕ Ajouter un nouveau chantre")

        # Dimensions par défaut plus compactes pour rendre la fenêtre moins imposante
        win_w, win_h = 620, 720

        self.geometry(f"{win_w}x{win_h}")
        self.minsize(600, 680)
        self.maxsize(700, 780)
        self.transient(parent)
        self.grab_set()
        self.resizable(True, True)

        # Centrer la fenêtre
        self.center_dialog(win_w, win_h)

        # Style moderne
        self.configure(fg_color="#1a1a2e")

        # Header avec icône
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))

        icon_label = ctk.CTkLabel(header_frame, text="👤", font=ctk.CTkFont(size=48))
        icon_label.pack(pady=(0,10))

        title_label = ctk.CTkLabel(header_frame, text="Nouveau Chantre Shekinah",
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack()

        # Formulaire dans un frame scrollable
        form_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=(10, 0))

        self.nom_var = ctk.StringVar()
        self.tel_var = ctk.StringVar()
        self.email_var = ctk.StringVar()

        # Champs avec labels améliorés
        fields = [
            ("👤 Nom Complet *", self.nom_var, "Dupont Marie"),
            ("📞 Téléphone", self.tel_var, "+243 XXX XXX XXX"),
            ("📧 Email", self.email_var, "chantre@shekinah.org")
        ]

        for icon_label_text, var, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10)

            label = ctk.CTkLabel(field_frame, text=icon_label_text,
                                font=ctk.CTkFont(size=14, weight="bold"))
            label.pack(anchor="w", pady=(0,5))

            entry = ctk.CTkEntry(field_frame, textvariable=var,
                                placeholder_text=placeholder, height=45,
                                font=ctk.CTkFont(size=12))
            entry.pack(fill="x")

        # Pupitre avec style amélioré
        pupitre_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        pupitre_frame.pack(fill="x", pady=15)

        pupitre_label = ctk.CTkLabel(pupitre_frame, text="🎵 Pupitre *",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        pupitre_label.pack(anchor="w", pady=(0,5))

        self.pupitre_var = tk.StringVar(value="Soprano")
        pupitre_combo = ctk.CTkOptionMenu(pupitre_frame,
                                         values=["Soprano", "Alto", "Tenor", "Basse"],
                                         variable=self.pupitre_var,
                                         height=45, font=ctk.CTkFont(size=12))
        pupitre_combo.pack(fill="x")

        # Commentaires
        comments_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        comments_frame.pack(fill="x", pady=15)

        comments_label = ctk.CTkLabel(comments_frame, text="💬 Commentaires Coach",
                                     font=ctk.CTkFont(size=14, weight="bold"))
        comments_label.pack(anchor="w", pady=(0,5))

        self.comment_box = ctk.CTkTextbox(comments_frame, height=120,
                                         font=ctk.CTkFont(size=12))
        self.comment_box.pack(fill="x")

        # Séparateur avant les boutons
        separator = ctk.CTkFrame(self, height=2, fg_color="#2d3748")
        separator.pack(fill="x", pady=(10, 0))

        # Boutons améliorés avec footer fixe
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom", padx=30, pady=20)

        cancel_btn = ctk.CTkButton(btn_frame, text="❌ Annuler",
                                  fg_color="#6b7280", height=50,
                                  command=self.destroy,
                                  font=ctk.CTkFont(size=14, weight="bold"))
        cancel_btn.pack(side="left", expand=True, padx=(0,10))

        save_btn = ctk.CTkButton(btn_frame, text="✅ Enregistrer",
                                fg_color="#10b981", height=50,
                                command=self.save_member,
                                font=ctk.CTkFont(size=14, weight="bold"))
        save_btn.pack(side="right", expand=True, padx=(10,0))

    def center_dialog(self, width, height):
        """Centre le dialogue sur l'écran"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

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
            messagebox.showerror("Erreur", "Échec ajout.")


class MemberDetailDialog(ctk.CTkToplevel):
    """Dialogue de détail membre avec onglets améliorés"""
    def __init__(self, parent, membre_id):
        super().__init__(parent)
        self.membre_id = membre_id
        self.title(f"Detail Membre #{membre_id}")

        # Dimensions ajustées pour que tout reste visible (action buttons visibles en bas)
        win_w, win_h = 920, 660

        self.geometry(f"{win_w}x{win_h}")
        self.minsize(900, 640)
        self.maxsize(1100, 700)
        self.transient(parent)
        self.grab_set()
        self.resizable(True, False)

        # Centrer la fenêtre
        self.center_dialog(win_w, win_h)

        # Style moderne
        self.configure(fg_color="#1a1a2e")

        # Empêcher d'être trop petit
        self.minsize(860, 620)

        # Raccourcis clavier utile (Ctrl+S pour enregistrer)
        self.bind('<Control-s>', lambda e: self.save_changes())
        self.bind('<Escape>', lambda e: self.destroy())

        # Header avec informations du membre
        self.create_header()

        # Conteneur principal pour les onglets + actions sticky
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(10, 0))
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Onglets améliorés
        self.tabview = ctk.CTkTabview(self.content_frame)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0,10))

        # Chargement des données
        self.load_member_data()

        # Création des onglets
        self.tab_infos = self.tabview.add("Informations")
        self.create_infos_tab()

        self.tab_finances = self.tabview.add("Finances")
        self.create_finances_tab()

        self.tab_presences = self.tabview.add("Presences")
        self.create_presences_tab()

        # Boutons d'action améliorés
        self.create_action_buttons()

    def center_dialog(self, width, height):
        """Centre le dialogue sur l'écran"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_header(self):
        """Crée l'en-tête avec les informations principales du membre"""
        header_frame = ctk.CTkFrame(self, fg_color="#2563eb", corner_radius=15)
        header_frame.pack(fill="x", padx=25, pady=25)

        # Informations principales
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=25, pady=20)

        # ID et nom
        id_name_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        id_name_frame.pack(fill="x", pady=(0,10))

        id_label = ctk.CTkLabel(id_name_frame, text=f"ID: {self.membre_id}",
                               font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
        id_label.pack(side="left")

        # Chargement des données pour l'en-tête
        membre_df = db.get_membre_by_id(self.membre_id)
        if not membre_df.empty:
            membre = membre_df.iloc[0]
            nom = membre['nom']
            pupitre = membre['pupitre']
            statut = membre['statut']

            nom_label = ctk.CTkLabel(id_name_frame, text=nom,
                                   font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
            nom_label.pack(side="left", padx=(20,0))

            # Pupitre et statut
            details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            details_frame.pack(fill="x")

            pupitre_colors = {
                "Soprano": "#f59e0b",
                "Alto": "#8b5cf6",
                "Tenor": "#06b6d4",
                "Basse": "#ef4444"
            }

            pupitre_color = pupitre_colors.get(pupitre, "#6b7280")
            pupitre_label = ctk.CTkLabel(details_frame, text=f"Pupitre: {pupitre}",
                                        font=ctk.CTkFont(size=14), text_color=pupitre_color)
            pupitre_label.pack(side="left", padx=(0,20))

            statut_color = "#10b981" if statut == "Actif" else "#ef4444"
            statut_label = ctk.CTkLabel(details_frame, text=f"Statut: {statut}",
                                       font=ctk.CTkFont(size=14), text_color=statut_color)
            statut_label.pack(side="left")

    def load_member_data(self):
        """Charge les données du membre"""
        self.membre_df = db.get_membre_by_id(self.membre_id)
        if self.membre_df.empty:
            self.destroy()
            return
        self.membre = self.membre_df.iloc[0]
        self.finances_df = db.get_finances_membre(self.membre_id)
        self.presences_df = db.get_presences_membre(self.membre_id)

    def delete_transaction(self, finance_id):
        if not messagebox.askyesno('Confirmer', 'Supprimer cette transaction ?'):
            return

        if db.supprimer_finance(finance_id):
            messagebox.showinfo('Supprimé', 'Transaction supprimée avec succès.')
            self.refresh_member_data()
        else:
            messagebox.showerror('Erreur', 'Impossible de supprimer la transaction.')

    def create_infos_tab(self):
        """Crée l'onglet d'informations avec formulaire amélioré"""
        frame = self.tab_infos

        # Formulaire dans un scrollable frame
        form_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre de section
        section_title = ctk.CTkLabel(form_frame, text="Informations Personnelles",
                                   font=ctk.CTkFont(size=20, weight="bold"))
        section_title.pack(pady=(0,20))

        # Variables
        self.nom_var = ctk.StringVar(value=self.membre['nom'])
        self.pupitre_var = ctk.StringVar(value=self.membre['pupitre'])
        self.tel_var = ctk.StringVar(value=self.membre['telephone'] or '')
        self.email_var = ctk.StringVar(value=self.membre['email'] or '')
        self.statut_var = ctk.StringVar(value=self.membre['statut'])

        # Champs organisés en sections
        fields_data = [
            ("Nom complet *", self.nom_var, "text", "Dupont Marie"),
            ("Telephone", self.tel_var, "text", "+243 XXX XXX XXX"),
            ("Email", self.email_var, "text", "chantre@shekinah.org"),
            ("Pupitre *", self.pupitre_var, "option", ["Soprano", "Alto", "Tenor", "Basse"]),
            ("Statut", self.statut_var, "option", ["Actif", "Inactif"])
        ]

        for label_text, var, field_type, placeholder in fields_data:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=8)

            label = ctk.CTkLabel(field_frame, text=label_text,
                               font=ctk.CTkFont(size=14, weight="bold"))
            label.pack(anchor="w", pady=(0,5))

            if field_type == "text":
                entry = ctk.CTkEntry(field_frame, textvariable=var,
                                   placeholder_text=placeholder, height=40,
                                   font=ctk.CTkFont(size=12))
                entry.pack(fill="x")
            elif field_type == "option":
                option_menu = ctk.CTkOptionMenu(field_frame, values=placeholder,
                                              variable=var, height=40,
                                              font=ctk.CTkFont(size=12))
                option_menu.pack(fill="x")

        # Commentaires
        comments_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        comments_frame.pack(fill="x", pady=15)

        comments_label = ctk.CTkLabel(comments_frame, text="Commentaires Coach",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        comments_label.pack(anchor="w", pady=(0,5))

        self.comment_box = ctk.CTkTextbox(comments_frame, height=120,
                                        font=ctk.CTkFont(size=12))
        self.comment_box.pack(fill="x")
        self.comment_box.insert("1.0", self.membre['commentaires_coach'] or '')

    def create_finances_tab(self):
        """Crée l'onglet finances avec historique et actions améliorées"""
        frame = self.tab_finances

        # Header avec statistiques
        header_frame = ctk.CTkFrame(frame, fg_color="#1a1a2e", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=15)

        stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=15)

        if not self.finances_df.empty:
            total_by_devise = self.finances_df.groupby('devise')['montant'].sum().to_dict()
            total_FC = total_by_devise.get('FC', 0)
            total_USD = total_by_devise.get('$', 0)
        else:
            total_FC = 0
            total_USD = 0

        nb_transactions = len(self.finances_df)

        stat1 = ctk.CTkLabel(stats_frame, text=f"Total cotise: {total_FC:,.0f} FC, {total_USD:,.0f} $",
                           font=ctk.CTkFont(size=16, weight="bold"), text_color="#10b981")
        stat1.pack(side="left", padx=(0,30))

        stat2 = ctk.CTkLabel(stats_frame, text=f"Transactions: {nb_transactions}",
                           font=ctk.CTkFont(size=16), text_color="#3b82f6")
        stat2.pack(side="left")

        # Bouton d'ajout
        add_btn = ctk.CTkButton(header_frame, text="Ajouter Cotisation",
                               command=self.add_cotisation_dialog,
                               fg_color="#10b981", height=40, width=180,
                               font=ctk.CTkFont(size=13, weight="bold"))
        add_btn.pack(side="right", padx=20)

        # Liste des transactions
        list_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(10,20))

        if self.finances_df.empty:
            empty_label = ctk.CTkLabel(list_frame, text="Aucune transaction financiere",
                                     font=ctk.CTkFont(size=16), text_color="#888888")
            empty_label.pack(pady=50)
        else:
            # Trier par date décroissante
            finances_sorted = self.finances_df.sort_values('date_paiement', ascending=False)

            for _, row in finances_sorted.iterrows():
                # Carte pour chaque transaction
                transaction_card = ctk.CTkFrame(list_frame, fg_color="#2a2a3e", corner_radius=8)
                transaction_card.pack(fill="x", pady=5)

                card_content = ctk.CTkFrame(transaction_card, fg_color="transparent")
                card_content.pack(fill="x", padx=15, pady=10)

                # Date et type
                header_tx = ctk.CTkFrame(card_content, fg_color="transparent")
                header_tx.pack(fill="x", pady=(0,5))

                date_label = ctk.CTkLabel(header_tx, text=row['date_paiement'],
                                        font=ctk.CTkFont(size=12), text_color="#cccccc")
                date_label.pack(side="left")

                type_label = ctk.CTkLabel(header_tx, text=f"Type: {row['type']}",
                                         font=ctk.CTkFont(size=12, weight="bold"),
                                         text_color="#3b82f6")
                type_label.pack(side="right")

                # Montant et motif
                amount_frame = ctk.CTkFrame(card_content, fg_color="transparent")
                amount_frame.pack(fill="x")

                tx_devise = row.get('devise', 'FC') if 'devise' in row else 'FC'
                amount_label = ctk.CTkLabel(amount_frame, text=f"{row['montant']:,.0f} {tx_devise}",
                                          font=ctk.CTkFont(size=18, weight="bold"),
                                          text_color="#10b981")
                amount_label.pack(side="left")

                motif = row['motif'] or "Sans motif"
                motif_label = ctk.CTkLabel(amount_frame, text=motif,
                                         font=ctk.CTkFont(size=12), text_color="#888888")
                motif_label.pack(side="right")

                # Bouton d'annulation
                cancel_btn = ctk.CTkButton(card_content, text="❌ Annuler",
                                          fg_color="#ef4444", height=30, width=100,
                                          font=ctk.CTkFont(size=11),
                                          command=lambda fid=row['id']: self.delete_transaction(fid))
                cancel_btn.pack(side="right", padx=(10, 0), pady=(10, 0))

    def add_cotisation_dialog(self):
        """Dialogue amélioré pour ajouter une cotisation avec scrollbar et footer fixe"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajouter Cotisation")
        # Dimensions plus grandes pour meilleur affichage
        dw, dh = 700, 650
        dialog.geometry(f"{dw}x{dh}")
        dialog.minsize(680, 620)
        dialog.maxsize(750, 700)
        dialog.resizable(True, True)
        dialog.transient(self)
        dialog.grab_set()
        center_dialog(dialog, dw, dh)
        dialog.configure(fg_color="#1a1a2e")

        # Header
        header_frame = ctk.CTkFrame(dialog, fg_color="#2563eb", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=20)

        title_label = ctk.CTkLabel(header_frame, text="Nouvelle Cotisation",
                                 font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        title_label.pack(pady=15)

        # Formulaire dans un scrollable frame
        form_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(15, 0))

        # Variables
        self.cotisation_montant_var = ctk.StringVar()
        self.cotisation_type_var = tk.StringVar(value="Cotisation")
        self.cotisation_motif_var = ctk.StringVar()
        self.cotisation_devise_var = tk.StringVar(value="FC")
        self.cotisation_date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        # Champs
        fields = [
            ("Montant *", self.cotisation_montant_var, "entry", "50000"),
            ("Devise", self.cotisation_devise_var, "option", ["FC", "$"]),
            ("Date", self.cotisation_date_var, "entry", "YYYY-MM-DD"),
            ("Type", self.cotisation_type_var, "option", ["Cotisation", "Don", "Autre"]),
            ("Motif", self.cotisation_motif_var, "entry", "Mensuelle, Speciale...")
        ]

        for label_text, var, field_type, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10)

            label = ctk.CTkLabel(field_frame, text=label_text,
                               font=ctk.CTkFont(size=14, weight="bold"))
            label.pack(anchor="w", pady=(0,5))

            if field_type == "entry":
                entry = ctk.CTkEntry(field_frame, textvariable=var,
                                   placeholder_text=placeholder, height=40,
                                   font=ctk.CTkFont(size=12))
                entry.pack(fill="x")
            elif field_type == "option":
                option_menu = ctk.CTkOptionMenu(field_frame, values=placeholder,
                                              variable=var, height=40,
                                              font=ctk.CTkFont(size=12))
                option_menu.pack(fill="x")

        # Séparateur avant footer
        separator = ctk.CTkFrame(dialog, height=2, fg_color="#2e2f4a")
        separator.pack(side="bottom", fill="x", padx=20, pady=(10, 0))

        # Boutons d'action au pied de la fenêtre (fixes)
        btn_frame = ctk.CTkFrame(dialog, fg_color="#111827", corner_radius=10)
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        inner_btn = ctk.CTkFrame(btn_frame, fg_color="transparent")
        inner_btn.pack(fill="x", padx=10, pady=8)

        cancel_btn = ctk.CTkButton(inner_btn, text="Annuler",
                                 fg_color="#6b7280", height=45,
                                 command=dialog.destroy,
                                 font=ctk.CTkFont(size=14, weight="bold"))
        cancel_btn.pack(side="left", expand=True, padx=(0,10))

        save_btn = ctk.CTkButton(inner_btn, text="Ajouter Cotisation",
                               fg_color="#10b981", height=45,
                               command=lambda: self.save_cotisation(dialog),
                               font=ctk.CTkFont(size=14, weight="bold"))
        save_btn.pack(side="right", expand=True, padx=(10,0))

    def save_cotisation(self, dialog):
        """Sauvegarde la cotisation avec validation améliorée"""
        try:
            # Validation du montant
            montant_text = self.cotisation_montant_var.get().strip().replace(',', '').replace(' ', '')
            if not montant_text:
                raise ValueError("Le montant est obligatoire")

            montant = float(montant_text)
            if montant <= 0:
                raise ValueError("Le montant doit être positif")
            if montant > 10000000:  # Limite à 10M FC
                raise ValueError("Montant trop élevé (max 10.000.000 FC)")

            # Récupérer la devise sélectionnée
            devise = self.cotisation_devise_var.get()

            # Validation de la date
            date_str = self.cotisation_date_var.get().strip()
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Format de date invalide (YYYY-MM-DD)")

            # Validation du motif
            motif = self.cotisation_motif_var.get().strip()
            if not motif:
                motif = "Sans motif"
            
            # Ajouter la devise au motif pour affichage
            motif_with_currency = f"{motif} ({devise})"

            # Pour cotisation membre, on utilise le membre comme source (donateurs externes gérés séparément)
            source = self.membre.get('nom') if self.membre is not None else None

            membre_id_for_record = self.membre_id
            don_type = self.cotisation_type_var.get()

            # Sauvegarde
            if db.ajouter_finances(membre_id_for_record, montant, don_type, motif_with_currency, source, date_str, devise):
                messagebox.showinfo("Succès", f"Cotisation de {montant:,.0f} {devise} ajoutée avec succès !")
                dialog.destroy()
                self.refresh_member_data()
            else:
                messagebox.showerror("Erreur", "Échec de l'ajout de la cotisation : montant, type ou date invalide.")

        except ValueError as e:
            messagebox.showerror("Erreur de validation", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue : {e}")

    def create_presences_tab(self):
        """Crée l'onglet présences avec historique amélioré"""
        frame = self.tab_presences

        # Header avec statistiques
        header_frame = ctk.CTkFrame(frame, fg_color="#1a1a2e", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=15)

        stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=15)

        total_presences = len(self.presences_df)
        presences_present = len(self.presences_df[self.presences_df['present'] == 1]) if not self.presences_df.empty else 0
        taux_presence = (presences_present / total_presences * 100) if total_presences > 0 else 0

        stat1 = ctk.CTkLabel(stats_frame, text=f"Total seances: {total_presences}",
                           font=ctk.CTkFont(size=16, weight="bold"), text_color="#3b82f6")
        stat1.pack(side="left", padx=(0,30))

        stat2 = ctk.CTkLabel(stats_frame, text=f"Present: {presences_present}",
                           font=ctk.CTkFont(size=16), text_color="#10b981")
        stat2.pack(side="left", padx=(0,30))

        stat3 = ctk.CTkLabel(stats_frame, text=f"Taux: {taux_presence:.1f}%",
                           font=ctk.CTkFont(size=16), text_color="#f59e0b")
        stat3.pack(side="left")

        # Bouton d'ajout
        add_btn = ctk.CTkButton(header_frame, text="Marquer Presence",
                               command=self.add_presence_dialog,
                               fg_color="#3b82f6", height=40, width=180,
                               font=ctk.CTkFont(size=13, weight="bold"))
        add_btn.pack(side="right", padx=20)

        # Liste des présences
        list_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(10,20))

        if self.presences_df.empty:
            empty_label = ctk.CTkLabel(list_frame, text="Aucune presence enregistree",
                                     font=ctk.CTkFont(size=16), text_color="#888888")
            empty_label.pack(pady=50)
        else:
            # Trier par date décroissante
            presences_sorted = self.presences_df.sort_values('seance_date', ascending=False)

            for _, row in presences_sorted.iterrows():
                # Carte pour chaque présence
                presence_card = ctk.CTkFrame(list_frame, fg_color="#2a2a3e", corner_radius=8)
                presence_card.pack(fill="x", pady=5)

                card_content = ctk.CTkFrame(presence_card, fg_color="transparent")
                card_content.pack(fill="x", padx=15, pady=10)

                # Date et statut
                header_pr = ctk.CTkFrame(card_content, fg_color="transparent")
                header_pr.pack(fill="x", pady=(0,5))

                date_label = ctk.CTkLabel(header_pr, text=row['seance_date'],
                                        font=ctk.CTkFont(size=14, weight="bold"))
                date_label.pack(side="left")

                statut = "Present" if row['present'] else "Absent"
                statut_color = "#10b981" if row['present'] else "#ef4444"
                statut_label = ctk.CTkLabel(header_pr, text=statut,
                                          font=ctk.CTkFont(size=14, weight="bold"),
                                          text_color=statut_color)
                statut_label.pack(side="right")

                # Commentaire
                if row['commentaire'] and row['commentaire'].strip():
                    comment_frame = ctk.CTkFrame(card_content, fg_color="transparent")
                    comment_frame.pack(fill="x")

                    comment_label = ctk.CTkLabel(comment_frame, text=f"Note: {row['commentaire']}",
                                               font=ctk.CTkFont(size=12), text_color="#888888")
                    comment_label.pack(anchor="w")

    def add_presence_dialog(self):
        """Dialogue amélioré pour marquer une présence"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Marquer Presence")
        # Dimensions fixes correspondant aux screenshots
        dw, dh = 620, 500
        dialog.geometry(f"{dw}x{dh}")
        dialog.minsize(600, 480)
        dialog.maxsize(640, 520)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        center_dialog(dialog, dw, dh)
        dialog.configure(fg_color="#1a1a2e")

        # Header
        header_frame = ctk.CTkFrame(dialog, fg_color="#2563eb", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=20)

        title_label = ctk.CTkLabel(header_frame, text="Marquer Presence",
                                 font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        title_label.pack(pady=15)

        # Formulaire
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

        # Variables
        self.presence_date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.presence_present_var = tk.BooleanVar(value=True)
        self.presence_comment_var = ctk.StringVar()

        # Champs
        fields = [
            ("Date de la seance *", self.presence_date_var, "entry", "YYYY-MM-DD"),
            ("Commentaire (optionnel)", self.presence_comment_var, "entry", "Motif d'absence, remarques...")
        ]

        for label_text, var, field_type, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10)

            label = ctk.CTkLabel(field_frame, text=label_text,
                               font=ctk.CTkFont(size=14, weight="bold"))
            label.pack(anchor="w", pady=(0,5))

            if field_type == "entry":
                entry = ctk.CTkEntry(field_frame, textvariable=var,
                                   placeholder_text=placeholder, height=40,
                                   font=ctk.CTkFont(size=12))
                entry.pack(fill="x")

        # Case à cocher pour présence
        presence_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        presence_frame.pack(fill="x", pady=10)

        presence_label = ctk.CTkLabel(presence_frame, text="Statut de presence",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        presence_label.pack(anchor="w", pady=(0,5))

        presence_checkbox = ctk.CTkCheckBox(presence_frame, text="Present a la seance",
                                          variable=self.presence_present_var,
                                          font=ctk.CTkFont(size=12))
        presence_checkbox.pack(anchor="w")

        # Boutons
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)

        cancel_btn = ctk.CTkButton(btn_frame, text="Annuler",
                                 fg_color="#6b7280", height=45,
                                 command=dialog.destroy,
                                 font=ctk.CTkFont(size=14, weight="bold"))
        cancel_btn.pack(side="left", expand=True, padx=(0,10))

        save_btn = ctk.CTkButton(btn_frame, text="Enregistrer Presence",
                               fg_color="#3b82f6", height=45,
                               command=lambda: self.save_presence(dialog),
                               font=ctk.CTkFont(size=14, weight="bold"))
        save_btn.pack(side="right", expand=True, padx=(10,0))

    def save_presence(self, dialog):
        """Sauvegarde la présence avec validation améliorée"""
        try:
            # Validation de la date
            date_str = self.presence_date_var.get().strip()
            try:
                # Vérifier que la date n'est pas dans le futur
                presence_date = datetime.strptime(date_str, "%Y-%m-%d")
                if presence_date > datetime.now():
                    raise ValueError("La date ne peut pas être dans le futur")
            except ValueError as e:
                if "time data" in str(e):
                    raise ValueError("Format de date invalide (YYYY-MM-DD)")
                raise

            # Vérifier si une présence existe déjà pour cette date
            existing_presence = self.presences_df[self.presences_df['seance_date'] == date_str]
            if not existing_presence.empty:
                if not messagebox.askyesno("Confirmation",
                                         f"Une presence existe deja pour le {date_str}. Voulez-vous la modifier ?"):
                    return

            present = 1 if self.presence_present_var.get() else 0
            comment = self.presence_comment_var.get().strip()

            # Sauvegarde (utilise une fonction à implémenter dans db_models)
            if db.ajouter_presence(self.membre_id, date_str, present, comment):
                statut = "presente" if present else "absente"
                messagebox.showinfo("Succès", f"Presence {statut} enregistree pour le {date_str} !")
                dialog.destroy()
                self.refresh_member_data()
            else:
                messagebox.showerror("Erreur", "Échec de l'enregistrement de la presence.")

        except ValueError as e:
            messagebox.showerror("Erreur de validation", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue : {e}")

    def create_action_buttons(self):
        """Crée les boutons d'action au pied de la fenêtre (fixes)"""
        btn_frame = ctk.CTkFrame(self, fg_color="#111827", corner_radius=10)
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        # Séparer le corps de l'onglet et le footer
        separator = ctk.CTkFrame(self, height=2, fg_color="#2e2f4a")
        separator.pack(side="bottom", fill="x", padx=20)

        # Boutons d'action
        save_btn = ctk.CTkButton(btn_frame, text="Enregistrer Modifications",
                               command=self.save_changes, fg_color="#10b981",
                               height=45, font=ctk.CTkFont(size=13, weight="bold"))
        save_btn.pack(side="left", expand=True, padx=(0,10), pady=8)

        delete_btn = ctk.CTkButton(btn_frame, text="Désactiver Membre",
                                 command=self.soft_delete, fg_color="#ef4444",
                                 height=45, font=ctk.CTkFont(size=13, weight="bold"))
        delete_btn.pack(side="left", expand=True, padx=(0,10), pady=8)

        close_btn = ctk.CTkButton(btn_frame, text="Fermer",
                                command=self.destroy, fg_color="#6b7280",
                                height=45, font=ctk.CTkFont(size=13, weight="bold"))
        close_btn.pack(side="right", expand=True, padx=(10,0), pady=8)

    def refresh_member_data(self):
        """Actualise toutes les données du membre"""
        self.load_member_data()

        # Recréer les onglets avec les nouvelles données
        self.tabview.delete("Informations")
        self.tab_infos = self.tabview.add("Informations")
        self.create_infos_tab()

        self.tabview.delete("Finances")
        self.tab_finances = self.tabview.add("Finances")
        self.create_finances_tab()

        self.tabview.delete("Presences")
        self.tab_presences = self.tabview.add("Presences")
        self.create_presences_tab()

        # Rafraîchir la liste des membres dans la fenêtre parent
        if hasattr(self.master, 'refresh_membres_list'):
            self.master.refresh_membres_list()

    def save_changes(self):
        data = {
            'nom': self.nom_var.get(),
            'pupitre': self.pupitre_var.get(),
            'telephone': self.tel_var.get(),
            'email': self.email_var.get(),
            'statut': self.statut_var.get(),
            'commentaires_coach': self.comment_box.get("1.0", tk.END)
        }
        if db.update_membre(self.membre_id, **data):
            messagebox.showinfo("Succès", "✅ Membre mis à jour !")
            self.master.refresh_membres_list()
        else:
            messagebox.showerror("Erreur", "❌ Échec mise à jour.")

    def soft_delete(self):
        if messagebox.askyesno("Confirmer", "Désactiver membre (soft delete) ?"):
            db.supprimer_membre(self.membre_id)
            messagebox.showinfo("Terminé", "Membre désactivé.")
            self.master.refresh_membres_list()
            self.destroy()


# ============================================
# MAIN APPLICATION
# ============================================

class ShekinahApp(ctk.CTk):
    """Application principale Shekinah Worship Choir Manager"""
    def __init__(self):
        super().__init__()
        self.title("🎵 Shekinah Worship Choir Manager v3.0")
        
        # Taille par défaut pour correspondre à l'image (hauteur/largeur fixe)
        window_width, window_height = 1200, 760
        self.geometry(f"{window_width}x{window_height}")

        # Limites de redimensionnement pour préserver le layout : on ne peut pas trop réduire ni trop agrandir
        self.minsize(1100, 700)
        self.maxsize(1600, 900)
        self.resizable(True, True)

        # Centrer la fenêtre au démarrage
        self.center_window(window_width, window_height)

        # Configuration des couleurs et thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Sidebar améliorée
        self.sidebar = ctk.CTkFrame(self, corner_radius=15, width=300, fg_color="#1a1a2e")
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        # Header de la sidebar
        header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=30)

        logo_label = ctk.CTkLabel(header_frame, text="🎵", font=ctk.CTkFont(size=48))
        logo_label.pack(pady=(0,10))

        title_label = ctk.CTkLabel(header_frame, text="Shekinah\nWorship Choir",
                                  font=ctk.CTkFont(size=20, weight="bold"), justify="center")
        title_label.pack()

        version_label = ctk.CTkLabel(header_frame, text="v3.0", font=ctk.CTkFont(size=12),
                                    text_color="#888888")
        version_label.pack(pady=(5,0))

        # Séparateur
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="#3b82f6")
        separator.pack(fill="x", padx=20, pady=20)

        # Navigation améliorée
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, padx=15, pady=(0,20))

        nav_items = [
            ("🏠 Dashboard", "Dashboard", "Tableau de bord général"),
            ("👥 Membres", "Membres", "Gestion des chantres"),
            ("💰 Finances", "Finances", "Suivi financier"),
            ("🎁 Dons Externes", "DonsExternes", "Dons non-membres"),
            ("📢 Communiqués", "Communiqués", "Annonces et messages"),
            ("⚙️ Paramètres", "Paramètres", "Configuration système")
        ]

        self.buttons = {}
        self.show_commands = {
            "Dashboard": self.show_dashboard,
            "Membres": self.show_membres,
            "Finances": self.show_finances,
            "DonsExternes": self.show_external_donations,
            "Communiqués": self.show_communiques,
            "Paramètres": self.show_settings
        }

        for text, key, tooltip in nav_items:
            btn = ctk.CTkButton(nav_frame, text=text,
                               command=lambda k=key: [self.update_nav_styles(k), self.show_commands[k]()],
                               height=55, fg_color="transparent", text_color="#ffffff",
                               hover_color="#2563eb", corner_radius=10,
                               font=ctk.CTkFont(size=14, weight="bold"))
            btn.pack(fill="x", pady=5)
            self.buttons[key] = btn

        # Footer de la sidebar
        footer_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer_frame.pack(fill="x", padx=20, pady=(0,20))

        status_label = ctk.CTkLabel(footer_frame, text="🟢 Système opérationnel",
                                   font=ctk.CTkFont(size=11), text_color="#10b981")
        status_label.pack(anchor="w")

        # Main area avec fond dégradé
        self.main_frame = ctk.CTkFrame(self, fg_color="#0f172a")
        self.main_frame.grid(row=0, column=1, sticky="nswe", padx=0, pady=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        self.membres_tree = None
        self.member_list_window = None
        # Raccourcis clavier
        self.bind('<Control-n>', lambda e: self.add_member_dialog())
        self.bind('<Control-d>', lambda e: self.delete_selected_member())
        self.bind('<F5>', lambda e: self.show_dashboard())
        self.bind('<Control-f>', lambda e: self.focus_search())
        # Animation d'ouverture
        self.after(100, self.show_dashboard)

        self.show_dashboard()

    def update_nav_styles(self, active_key):
        """Met à jour les styles des boutons de navigation avec animation"""
        for key, btn in self.buttons.items():
            if key == active_key:
                btn.configure(fg_color="#2563eb", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color="#cccccc")

    def clear_main_frame(self):
        """Nettoie le frame principal avec animation de fondu"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def center_window(self, width, height):
        """Centre la fenêtre sur l'écran"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_tooltip(self, widget, text):
        """Affiche un tooltip informatif"""
        def enter(event):
            tooltip = ctk.CTkToplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = ctk.CTkLabel(tooltip, text=text, fg_color="#1a1a2e",
                                text_color="#ffffff", corner_radius=6, padx=10, pady=5)
            label.pack()

            def leave(event):
                tooltip.destroy()

            widget.tooltip = tooltip
            widget.bind('<Leave>', leave)

        widget.bind('<Enter>', enter)

    def focus_search(self):
        """Met le focus sur la barre de recherche"""
        if hasattr(self, 'search_var') and self.search_var:
            # Si on est dans la section membres, focus sur la recherche
            if hasattr(self, 'membres_tree') and self.membres_tree:
                # Simuler un clic sur la section membres pour s'assurer qu'elle est active
                self.show_membres()
                # Le focus sera automatiquement sur la barre de recherche

    def show_dashboard(self):
        self.update_nav_styles("Dashboard")
        self.clear_main_frame()

        # Header amélioré avec animation
        header = ctk.CTkFrame(self.main_frame, height=120, corner_radius=20, fg_color="#1a1a2e")
        header.pack(fill="x", pady=(30,0), padx=30)
        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(expand=True)

        icon_label = ctk.CTkLabel(title_frame, text="📊", font=ctk.CTkFont(size=56))
        icon_label.pack(side="left", padx=(0,25))

        text_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        text_frame.pack(side="left")

        title = ctk.CTkLabel(text_frame, text="Tableau de Bord Shekinah",
                            font=ctk.CTkFont(size=32, weight="bold"))
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(text_frame, text="Vue d'ensemble des activités du chœur",
                               font=ctk.CTkFont(size=16), text_color="#888888")
        subtitle.pack(anchor="w", pady=(5,0))

        # Date et heure (sans emoji pour compatibilité)
        controls_frame = ctk.CTkFrame(header, fg_color="transparent")
        controls_frame.pack(side="right", padx=20)

        refresh_cards_btn = ctk.CTkButton(controls_frame, text="🔄 Actualiser", 
                                          command=self.show_dashboard,
                                          fg_color="#2563eb", hover_color="#1e40af",
                                          height=35, width=140,
                                          font=ctk.CTkFont(size=12, weight="bold"))
        refresh_cards_btn.pack(side="right", padx=(0,10))

        datetime_label = ctk.CTkLabel(controls_frame,
                                     text=datetime.now().strftime("%d/%m/%Y   %H:%M"),
                                     font=ctk.CTkFont(size=14), text_color="#cccccc")
        datetime_label.pack(side="right")

        # Cartes de statistiques avec animations
        cards_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cards_container.pack(fill="x", padx=30, pady=30)
        cards_container.grid_columnconfigure((0,1,2), weight=1)

        # Données réelles
        solde = db.get_solde_caisse()
        membres_count = len(db.get_membres())
        finances_df = db.get_finances()
        finances_count = len(finances_df)

        current_month = datetime.now().strftime('%Y-%m')
        trans_this_month = 0
        if not finances_df.empty:
            trans_this_month = len(finances_df[finances_df['date_paiement'].str.startswith(current_month)])

        cards = [
            ("CAISSE TOTALE", f"{int(solde):,} FC", "#22c55e", "Solde actuel de la tresorerie", None),
            ("CHANTRES ACTIFS", f"{membres_count}", "#3b82f6", "Nombre total de membres actifs", ('statut', 'Actif')),
            ("TRANSACTIONS", f"{trans_this_month}", "#f97316", f"Ce mois ({current_month})", None)
        ]

        for col, (title, value, color, tooltip, target) in enumerate(cards):
            card = ctk.CTkFrame(cards_container, fg_color=color, height=160, corner_radius=20)
            card.grid(row=0, column=col, padx=15, pady=10, sticky="ew")
            card.grid_propagate(False)

            def card_click(evt=None, t=target):
                if t is not None:
                    self.show_membres(filter_key=t[0], filter_value=t[1])
                else:
                    self.show_membres()

            card.bind("<Button-1>", card_click)

            # Header de la carte
            card_header = ctk.CTkFrame(card, fg_color="transparent")
            card_header.pack(fill="x", padx=20, pady=(20,10))

            ctk.CTkLabel(card_header, text=title, font=ctk.CTkFont(size=14, weight="bold"),
                        text_color="white").pack(anchor="w")

            # Valeur principale
            value_frame = ctk.CTkFrame(card, fg_color="transparent")
            value_frame.pack(fill="x", padx=20, pady=(0,15))

            ctk.CTkLabel(value_frame, text=value, font=ctk.CTkFont(size=36, weight="bold"),
                        text_color="white").pack(anchor="w")

            # Tooltip
            ctk.CTkLabel(value_frame, text=tooltip, font=ctk.CTkFont(size=11),
                        text_color="#e0e0e0").pack(anchor="w", pady=(5,0))

        # Section graphique améliorée
        graph_section = ctk.CTkFrame(self.main_frame, corner_radius=20, fg_color="#1a1a2e")
        graph_section.pack(fill="x", padx=30, pady=(0,30))

        graph_header = ctk.CTkFrame(graph_section, fg_color="transparent")
        graph_header.pack(fill="x", padx=30, pady=20)

        graph_title = ctk.CTkLabel(graph_header, text="Evolution Financiere Mensuelle",
                                  font=ctk.CTkFont(size=24, weight="bold"))
        graph_title.pack(side="left")

        graph_frame = ctk.CTkFrame(graph_section, height=380, corner_radius=15)
        graph_frame.pack(fill="x", padx=30, pady=(0,30))
        graph_frame.pack_propagate(False)

        # Génération du graphique
        self.generate_financial_chart(graph_frame)

        # Section objectifs
        objectives_section = ctk.CTkFrame(self.main_frame, corner_radius=20, fg_color="#1a1a2e")
        objectives_section.pack(fill="x", padx=30, pady=(0,30))

        obj_header = ctk.CTkFrame(objectives_section, fg_color="transparent")
        obj_header.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(obj_header, text="Objectifs 2026", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")

        target = 2000000
        pct = min(solde / target * 100 if target > 0 else 0, 100)

        progress_container = ctk.CTkFrame(objectives_section, fg_color="transparent")
        progress_container.pack(fill="x", padx=30, pady=(0,30))

        # Informations de progression
        progress_info = ctk.CTkFrame(progress_container, fg_color="transparent")
        progress_info.pack(fill="x", pady=(0,20))

        info_text = f"Actuel : {int(solde):,} FC   |   Objectif : {target:,} FC   |   Progression : {pct:.1f}%"
        ctk.CTkLabel(progress_info, text=info_text, font=ctk.CTkFont(size=16, weight="bold")).pack()

        # Barre de progression stylisée
        progress_frame = ctk.CTkFrame(progress_container, fg_color="#2a2a3e", corner_radius=10)
        progress_frame.pack(fill="x", pady=(0,10))

        prog_bar = ctk.CTkProgressBar(progress_frame, width=1100, height=40,
                                     progress_color="#10b981", corner_radius=10)
        prog_bar.set(pct/100)
        prog_bar.pack(pady=20, padx=20)

        # Actions rapides
        actions_frame = ctk.CTkFrame(self.main_frame, corner_radius=20, fg_color="#1a1a2e")
        actions_frame.pack(fill="x", padx=30, pady=(0,30))

        actions_header = ctk.CTkFrame(actions_frame, fg_color="transparent")
        actions_header.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(actions_header, text="Actions Rapides", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")

        actions_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
        actions_container.pack(fill="x", padx=30, pady=(0,30))

        quick_actions = [
            ("Nouveau Membre", self.add_member_dialog, "#10b981"),
            ("Ajouter Cotisation", lambda: self.show_finances(), "#3b82f6"),
            ("Rapport Mensuel", lambda: self.show_finances(), "#f59e0b")
        ]

        for action_text, action_cmd, color in quick_actions:
            action_btn = ctk.CTkButton(actions_container, text=action_text,
                                      command=action_cmd, fg_color=color,
                                      height=50, width=200, corner_radius=10,
                                      font=ctk.CTkFont(size=14, weight="bold"))
            action_btn.pack(side="left", padx=10)

    def generate_financial_chart(self, parent_frame):
        """Génère le graphique financier avec style amélioré"""
        finances_mensuel = db.get_finances_mensuel()
        if finances_mensuel.empty:
            ctk.CTkLabel(parent_frame, text="Aucune donnée financière disponible",
                        font=ctk.CTkFont(size=16)).pack(expand=True)
            return

        monthly_series = finances_mensuel.set_index('mois')['total']
        months = monthly_series.index.tolist()
        values = monthly_series.tolist()

        fig, ax = plt.subplots(figsize=(16, 5), facecolor='#1a1a2e')
        ax.set_facecolor('#1a1a2e')

        colors = ['#10b981' if v >= 0 else '#ef4444' for v in values]
        bars = ax.bar(months, values, color=colors, alpha=0.9, edgecolor='#ffffff',
                     linewidth=2, width=0.6)

        # Améliorations du graphique
        ax.set_title('Recettes Mensuelles (FC)', fontsize=22, fontweight='bold',
                    color='white', pad=30)
        ax.set_ylabel('Montant (FC)', fontsize=16, color='white', labelpad=15)
        ax.tick_params(colors='white', labelsize=14, rotation=45)
        ax.grid(axis='y', alpha=0.3, color='white', linestyle='--')

        # Ajouter les valeurs sur les barres
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + (max(values) * 0.02),
                   f'{int(value):,}', ha='center', va='bottom', fontsize=12,
                   fontweight='bold', color='white')

        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, facecolor='#1a1a2e',
                   bbox_inches='tight', edgecolor='none')
        buf.seek(0)
        plt.close()

        img = Image.open(buf)
        chart_img = ctk.CTkImage(img, size=(1350, 320))
        ctk.CTkLabel(parent_frame, image=chart_img, text="").pack(pady=20)

    def show_membres(self, filter_key=None, filter_value=None):
        self.update_nav_styles("Membres")
        self.clear_main_frame()
        self.current_members_filter = (filter_key, filter_value)

        # Header amélioré
        header = ctk.CTkFrame(self.main_frame, height=100, corner_radius=15, fg_color="#1a1a2e")
        header.pack(fill="x", pady=(30,0), padx=30)
        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(expand=True)

        icon_label = ctk.CTkLabel(title_frame, text="👥", font=ctk.CTkFont(size=48))
        icon_label.pack(side="left", padx=(0,20))

        text_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        text_frame.pack(side="left")

        title = ctk.CTkLabel(text_frame, text="Gestion Membres Shekinah",
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(text_frame, text="Administration des chantres et pupitres",
                               font=ctk.CTkFont(size=14), text_color="#888888")
        subtitle.pack(anchor="w")

        # Barre d'outils améliorée
        toolbar = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#1a1a2e")
        toolbar.pack(fill="x", padx=30, pady=20)

        # Section recherche
        search_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_frame.pack(fill="x", padx=25, pady=20)

        search_icon = ctk.CTkLabel(search_frame, text="🔍", font=ctk.CTkFont(size=20))
        search_icon.pack(side="left", padx=(0,15))

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var,
                                   placeholder_text="Rechercher par nom, pupitre, téléphone...",
                                   height=50, font=ctk.CTkFont(size=14))
        search_entry.pack(side="left", fill="x", expand=True, padx=(0,20))

        refresh_members_btn = ctk.CTkButton(search_frame, text="🔄 Actualiser",
                                            command=self.show_membres,
                                            fg_color="#2563eb", hover_color="#1e40af",
                                            height=50, width=140,
                                            font=ctk.CTkFont(size=13, weight="bold"))
        refresh_members_btn.pack(side="left", padx=(0,10))

        # Boutons d'action
        actions_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        add_btn = ctk.CTkButton(actions_frame, text="➕ Ajouter Membre",
                               command=self.add_member_dialog,
                               fg_color="#10b981", height=50, width=180,
                               font=ctk.CTkFont(size=13, weight="bold"),
                               corner_radius=10)
        add_btn.pack(side="left", padx=(0,10))

        delete_btn = ctk.CTkButton(actions_frame, text="🗑️ Supprimer sélection",
                                  command=self.delete_selected_member,
                                  fg_color="#ef4444", height=50, width=200,
                                  font=ctk.CTkFont(size=13, weight="bold"),
                                  corner_radius=10)
        delete_btn.pack(side="left")

        export_btn = ctk.CTkButton(actions_frame, text="📄 Export PDF",
                                   command=self.export_members_pdf,
                                   fg_color="#2563eb", height=50, width=180,
                                   font=ctk.CTkFont(size=13, weight="bold"),
                                   corner_radius=10)
        export_btn.pack(side="left", padx=(10,0))

        # Statistiques rapides - Design amélioré
        stats_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#1a1a2e")
        stats_frame.pack(fill="x", padx=30, pady=(0,20))

        # Configuration de la grille pour un meilleur responsive
        stats_frame.grid_columnconfigure((0,1,2), weight=1)
        stats_frame.grid_rowconfigure(0, weight=1)
        stats_frame.grid_rowconfigure(1, weight=1)

        try:
            membres_df = db.get_membres()
            total_membres = len(membres_df)
            actifs = len(membres_df[membres_df['statut'] == 'Actif'])
            inactifs_df = db.get_membres(include_inactifs=True)
            inactifs = len(inactifs_df[inactifs_df['actif'] == 0])
            pupitres = membres_df['pupitre'].value_counts()

            stats_data = [
                ("Total Membres", f"{total_membres}", "#3b82f6", "Voir tous", None),
                ("Membres Actifs", f"{actifs}", "#10b981", "Voir actifs", ("statut", "Actif")),
                ("Membres Inactifs", f"{inactifs}", "#ef4444", "Voir inactifs", ("actif", 0)),
                ("Soprano", f"{pupitres.get('Soprano', 0)}", "#f59e0b", "Voir soprano", ("pupitre", "Soprano")),
                ("Alto", f"{pupitres.get('Alto', 0)}", "#8b5cf6", "Voir alto", ("pupitre", "Alto")),
                ("Tenor", f"{pupitres.get('Tenor', 0)}", "#06b6d4", "Voir tenor", ("pupitre", "Tenor")),
                ("Basse", f"{pupitres.get('Basse', 0)}", "#ef4444", "Voir basse", ("pupitre", "Basse"))
            ]

            for i, (label, value, color, tooltip, target) in enumerate(stats_data):
                row = i // 3  # 3 cartes par ligne
                col = i % 3

                stat_card = ctk.CTkFrame(stats_frame, fg_color=color, height=90, corner_radius=12)
                stat_card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
                stat_card.grid_propagate(False)

                def make_card_click(t):
                    def card_click(event=None):
                        if t is None:
                            self.show_membres()
                        elif t[0] == 'actif':
                            self.show_membres(filter_key='actif', filter_value=0)
                        else:
                            self.show_membres(filter_key=t[0], filter_value=t[1])
                    return card_click

                click_handler = make_card_click(target)
                stat_card.bind("<Button-1>", click_handler)
                stat_card.bind("<Enter>", lambda e: stat_card.configure(fg_color=color if color.startswith('#') else color, border_width=2))
                stat_card.bind("<Leave>", lambda e: stat_card.configure(border_width=0))

                # Header avec icône et label
                header_frame = ctk.CTkFrame(stat_card, fg_color="transparent")
                header_frame.pack(fill="x", padx=15, pady=(12,5))

                label_widget = ctk.CTkLabel(header_frame, text=label, font=ctk.CTkFont(size=13, weight="bold"),
                            text_color="white")
                label_widget.pack(anchor="w")

                # Valeur principale centrée
                value_frame = ctk.CTkFrame(stat_card, fg_color="transparent")
                value_frame.pack(fill="x", padx=15, pady=(0,12))

                value_widget = ctk.CTkLabel(value_frame, text=value, font=ctk.CTkFont(size=28, weight="bold"),
                            text_color="white")
                value_widget.pack(anchor="center")

                # Tooltip au survol (optionnel - peut être ajouté plus tard)
                # self.show_tooltip(stat_card, tooltip)

        except Exception as e:
            error_frame = ctk.CTkFrame(stats_frame, fg_color="#ef4444", corner_radius=10)
            error_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
            ctk.CTkLabel(error_frame, text=f"Erreur chargement stats: {e}",
                        font=ctk.CTkFont(size=14), text_color="white").pack(pady=15, padx=15)

        # Table des membres
        table_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0,30))

        table_header = ctk.CTkFrame(table_frame, fg_color="#1a1a2e", corner_radius=10)
        table_header.pack(fill="x", padx=20, pady=15)

        table_title = ctk.CTkButton(table_header, text="📋 Liste des Membres",
                                    command=self.open_member_list_window,
                                    fg_color="#2563eb",
                                    hover_color="#1e40af",
                                    height=40,
                                    corner_radius=10,
                                    font=ctk.CTkFont(size=18, weight="bold"))
        table_title.pack(pady=10)

        scroll_frame = ctk.CTkScrollableFrame(table_frame, corner_radius=10)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

        # Style amélioré pour la Treeview
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                       background="#1a1a2e",
                       foreground="#ffffff",
                       rowheight=35,
                       fieldbackground="#1a1a2e",
                       borderwidth=0,
                       font=('Segoe UI', 11))
        style.configure("Treeview.Heading",
                       background="#2563eb",
                       foreground="#ffffff",
                       font=('Segoe UI', 12, 'bold'),
                       borderwidth=0)
        style.map('Treeview', background=[('selected', '#2563eb')])

        self.membres_tree = ttk.Treeview(scroll_frame,
                                        columns=("ID", "Nom", "Pupitre", "Tel", "Email", "Statut", "Date"),
                                        show="headings", height=15, selectmode="extended")

        columns_config = [
            ("ID", 80, "center"),
            ("Nom", 280, "w"),
            ("Pupitre", 130, "center"),
            ("Tel", 170, "w"),
            ("Email", 240, "w"),
            ("Statut", 120, "center"),
            ("Date", 150, "center")
        ]

        for col, width, anchor in columns_config:
            self.membres_tree.heading(col, text=col)
            self.membres_tree.column(col, width=width, anchor=anchor)

        self.membres_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.membres_tree.bind("<Double-1>", self.on_member_select)

        self.search_var.trace_add('write', lambda *args: self.refresh_membres_list())
        self.refresh_membres_list()

    def refresh_membres_list(self):
        if self.membres_tree is None:
            return
            
        for item in self.membres_tree.get_children():
            self.membres_tree.delete(item)

        try:
            if self.search_var.get():
                df = db.search_membres(self.search_var.get())
            else:
                key, value = getattr(self, 'current_members_filter', (None, None))
                if key is None:
                    df = db.get_membres()
                elif key == 'actif' and value == 0:
                    df = db.get_membres(include_inactifs=True)
                    df = df[df['actif'] == 0]
                elif key == 'statut':
                    df = db.get_membres(statut=value, include_inactifs=True)
                elif key == 'pupitre':
                    df = db.get_membres(pupitre=value)
                else:
                    df = db.get_membres()

            for i, (_, row) in enumerate(df.iterrows()):
                values = (row['id'], row['nom'], row['pupitre'], row['telephone'] or '', row['email'] or '', row.get('statut', ''), row.get('date_adhesion', ''))
                self.membres_tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def export_members_pdf(self):
        try:
            if self.search_var.get():
                df = db.search_membres(self.search_var.get())
            else:
                key, value = getattr(self, 'current_members_filter', (None, None))
                if key is None:
                    df = db.get_membres(include_inactifs=True)
                elif key == 'actif' and value == 0:
                    df = db.get_membres(include_inactifs=True)
                    df = df[df['actif'] == 0]
                elif key == 'statut':
                    df = db.get_membres(statut=value, include_inactifs=True)
                elif key == 'pupitre':
                    df = db.get_membres(pupitre=value)
                else:
                    df = db.get_membres(include_inactifs=True)

            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.lib import colors
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

                pdf_path = "membres_export.pdf"
                doc = SimpleDocTemplate(pdf_path, pagesize=letter)

                table_data = [["ID", "Nom", "Pupitre", "Tel", "Email", "Statut", "Date"]]
                for _, row in df.iterrows():
                    table_data.append([
                        row.get('id', ''),
                        row.get('nom', ''),
                        row.get('pupitre', ''),
                        row.get('telephone', ''),
                        row.get('email', ''),
                        row.get('statut', ''),
                        row.get('date_adhesion', '')
                    ])

                table = Table(table_data, repeatRows=1)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2563eb')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.gray),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
                ]))

                story = [Paragraph('Liste des membres', getSampleStyleSheet()['Title']), Spacer(1, 12), table]
                doc.build(story)

                messagebox.showinfo('Export PDF', f'PDF exporté : {pdf_path}')
            except ImportError:
                xlsx_path = 'membres_export.xlsx'
                df.to_excel(xlsx_path, index=False)
                messagebox.showwarning('PDF non disponible',
                                       'Le package reportlab est introuvable. Installez-le via "pip install reportlab" pour générer un PDF.\n'
                                       f'Export Excel effectué : {xlsx_path}')
        except Exception as e:
            messagebox.showerror('Erreur export', str(e))

    def on_member_select(self, event):
        selection = self.membres_tree.selection()
        if selection:
            item = self.membres_tree.item(selection)
            membre_id = item['values'][0]
            MemberDetailDialog(self, int(membre_id))

    def open_member_list_window(self):
        """Ouvre une fenêtre modale avec la liste complète des membres."""
        if self.member_list_window is not None and tk.Toplevel.winfo_exists(self.member_list_window):
            self.member_list_window.lift()
            self.member_list_window.focus_force()
            return

        self.member_list_window = ctk.CTkToplevel(self)
        window = self.member_list_window
        window.title("📋 Liste des Membres")
        window.geometry("1100x720")
        window.minsize(1000, 620)
        window.transient(self)
        window.protocol("WM_DELETE_WINDOW", self._close_member_list_window)
        center_dialog(window, 1100, 720)

        container = ctk.CTkFrame(window, fg_color="#0f172a")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        search_frame = ctk.CTkFrame(container, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 10))

        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=search_var,
                                   placeholder_text="Rechercher par nom, pupitre, téléphone...",
                                   height=40, font=ctk.CTkFont(size=13))
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        refresh_btn = ctk.CTkButton(search_frame, text="🔄 Actualiser",
                                    fg_color="#2563eb", hover_color="#1e40af",
                                    command=lambda: refresh_window_list(),
                                    height=40, width=140,
                                    font=ctk.CTkFont(size=13, weight="bold"))
        refresh_btn.pack(side="right", padx=(0, 10))

        def delete_selected_from_window():
            sel = members_tree.selection()
            if not sel:
                messagebox.showwarning("Sélection requise", "Sélectionne au moins un membre à supprimer")
                return

            num_selected = len(sel)
            if num_selected == 1:
                item = members_tree.item(sel[0])
                membre_id = item['values'][0]
                membre_nom = item['values'][1]
                if not messagebox.askyesno("Confirmation", f"Supprimer (soft-delete) le membre '{membre_nom}' (ID: {membre_id}) ?"):
                    return
            else:
                if not messagebox.askyesno("Confirmation", f"Supprimer {num_selected} membre(s) sélectionnés ?"):
                    return

            deleted_count = 0
            for item_id in sel:
                item = members_tree.item(item_id)
                membre_id = item['values'][0]
                if db.supprimer_membre(membre_id):
                    deleted_count += 1

            if deleted_count > 0:
                messagebox.showinfo("Supprimé", f"{deleted_count} membre(s) désactivé(s) avec succès.")
                refresh_window_list()
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer les membres sélectionnés.")

        delete_btn = ctk.CTkButton(search_frame, text="🗑️ Supprimer sélection",
                                   command=delete_selected_from_window,
                                   fg_color="#ef4444", hover_color="#dc2626",
                                   height=40, width=200,
                                   font=ctk.CTkFont(size=13, weight="bold"))
        delete_btn.pack(side="right", padx=(10, 0))

        close_btn = ctk.CTkButton(search_frame, text="Fermer",
                                  fg_color="#6b7280", hover_color="#4b5563",
                                  command=window.destroy,
                                  height=40, width=120,
                                  font=ctk.CTkFont(size=13, weight="bold"))
        close_btn.pack(side="right")

        tree_frame = ctk.CTkFrame(container, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="#1a1a2e",
                        foreground="#ffffff",
                        rowheight=32,
                        fieldbackground="#1a1a2e",
                        borderwidth=0,
                        font=('Segoe UI', 11))
        style.configure("Treeview.Heading",
                        background="#2563eb",
                        foreground="#ffffff",
                        font=('Segoe UI', 12, 'bold'),
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#2563eb')])

        members_tree = ttk.Treeview(tree_frame,
                                    columns=("ID", "Nom", "Pupitre", "Tel", "Email", "Statut", "Date"),
                                    show="headings", height=18, selectmode="extended")

        cols = [("ID", 80, "center"), ("Nom", 280, "w"), ("Pupitre", 130, "center"),
                ("Tel", 170, "w"), ("Email", 240, "w"), ("Statut", 120, "center"), ("Date", 150, "center")]
        for col, width, anchor in cols:
            members_tree.heading(col, text=col)
            members_tree.column(col, width=width, anchor=anchor)

        members_tree.pack(fill="both", expand=True, padx=10, pady=10)

        def refresh_window_list(*args):
            query = search_var.get().strip()
            if query:
                df = db.search_membres(query)
            else:
                df = db.get_membres()

            for item in members_tree.get_children():
                members_tree.delete(item)

            for _, row in df.iterrows():
                members_tree.insert("", "end", values=(row['id'], row['nom'], row['pupitre'],
                                                       row['telephone'] or '', row['email'] or '',
                                                       row.get('statut', ''), row.get('date_adhesion', '')))

        search_var.trace_add('write', refresh_window_list)

        def on_double_click(event):
            sel = members_tree.selection()
            if sel:
                item = members_tree.item(sel)
                m_id = item['values'][0]
                MemberDetailDialog(self, int(m_id))

        members_tree.bind("<Double-1>", on_double_click)

        refresh_window_list()

    def _close_member_list_window(self):
        if self.member_list_window is not None:
            try:
                self.member_list_window.destroy()
            except Exception:
                pass
        self.member_list_window = None

    def add_member_dialog(self):
        dialog = AddMemberDialog(self)

    def delete_selected_member(self):
        if self.membres_tree is None:
            return

        selection = self.membres_tree.selection()
        if not selection:
            messagebox.showwarning("Sélection requise", "Sélectionne au moins un membre à supprimer")
            return

        num_selected = len(selection)
        if num_selected == 1:
            item = self.membres_tree.item(selection[0])
            membre_id = item['values'][0]
            membre_nom = item['values'][1]
            if not messagebox.askyesno("Confirmation", f"Supprimer (soft-delete) le membre '{membre_nom}' (ID: {membre_id}) ?"):
                return
        else:
            if not messagebox.askyesno("Confirmation", f"Supprimer (soft-delete) {num_selected} membres sélectionnés ?"):
                return

        deleted_count = 0
        for item_id in selection:
            item = self.membres_tree.item(item_id)
            membre_id = item['values'][0]
            if db.supprimer_membre(membre_id):
                deleted_count += 1

        if deleted_count > 0:
            messagebox.showinfo("Supprimé", f"{deleted_count} membre(s) désactivé(s) avec succès.")
            self.refresh_membres_list()
        else:
            messagebox.showerror("Erreur", "Impossible de supprimer les membres sélectionnés.")

    def delete_transaction(self, finance_id):
        if not messagebox.askyesno('Confirmer', 'Supprimer cette transaction ?'):
            return

        if db.supprimer_finance(finance_id):
            messagebox.showinfo('Supprimé', 'Transaction supprimée avec succès.')
            # rafraîchir la vue actuelle
            if getattr(self, 'current_members_filter', None) is not None:
                self.show_membres(*self.current_members_filter)
            else:
                self.show_external_donations()
        else:
            messagebox.showerror('Erreur', 'Impossible de supprimer la transaction.')

    def cancel_external_donation(self, finance_id):
        """Annule (supprime) un don externe et rafraîchit la liste."""
        if not messagebox.askyesno('Confirmation', 'Annuler ce don externe ?'):
            return

        if db.supprimer_finance(finance_id):
            messagebox.showinfo('Annulé', 'Don externe annulé avec succès.')
            self.show_external_donations()
        else:
            messagebox.showerror('Erreur', 'Impossible d\'annuler ce don.')

    def show_finances(self):
        self.update_nav_styles("Finances")
        self.clear_main_frame()
        
        header = ctk.CTkFrame(self.main_frame, height=80)
        header.pack(fill="x", pady=(30,0))
        header.pack_propagate(False)
        title = ctk.CTkLabel(header, text="💰 Gestion Finances", font=ctk.CTkFont(size=32, weight="bold"))
        title.pack(expand=True)
        
        ctk.CTkLabel(self.main_frame, text="Module Finances en développement...", 
                    font=ctk.CTkFont(size=18)).pack(pady=50)

    def show_external_donations(self):
        """Affiche les dons externes avec gestion complète"""
        self.update_nav_styles("DonsExternes")
        self.clear_main_frame()

        # Header
        header = ctk.CTkFrame(self.main_frame, height=100)
        header.pack(fill="x", pady=(30, 20), padx=30)
        header.pack_propagate(False)

        header_left = ctk.CTkFrame(header, fg_color="transparent")
        header_left.pack(side="left", fill="x", expand=True)

        title = ctk.CTkLabel(header_left, text="🎁 Dons Externes", font=ctk.CTkFont(size=32, weight="bold"))
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(header_left, text="Suivi des dons provenant de sources externes",
                               font=ctk.CTkFont(size=14), text_color="#888888")
        subtitle.pack(anchor="w", pady=(5, 0))

        # Bouton d'ajout
        add_btn = ctk.CTkButton(header, text="➕ Ajouter Don",
                               command=self.add_external_donation_dialog,
                               fg_color="#10b981", height=45, width=150,
                               font=ctk.CTkFont(size=13, weight="bold"))
        add_btn.pack(side="right")

        # Récupérer les dons externes (membre_id IS NULL ou source non-vide)
        finances_df = db.get_finances()
        external_donations = finances_df[
            (finances_df['type'] == 'Don') & 
            (finances_df['source'].notna())
        ].copy().sort_values('date_paiement', ascending=False)

        # Statistiques
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=20)

        if not external_donations.empty:
            total_by_devise = external_donations.groupby('devise')['montant'].sum().to_dict()
            total_fc = total_by_devise.get('FC', 0)
            total_usd = total_by_devise.get('$', 0)
        else:
            total_fc = 0
            total_usd = 0
        nombre_dons = len(external_donations)

        stat_cards = [
            (f"Total Dons: {total_fc:,.0f} FC / {total_usd:,.0f} $", "#10b981"),
            (f"Nombre Dons: {nombre_dons}", "#3b82f6")
        ]

        for stat_text, color in stat_cards:
            stat_card = ctk.CTkFrame(stats_frame, fg_color=color, corner_radius=10)
            stat_card.pack(side="left", padx=10, pady=10)

            stat_label = ctk.CTkLabel(stat_card, text=stat_text, 
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     text_color="white")
            stat_label.pack(padx=20, pady=15)

        # Tableau des dons
        list_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=30, pady=(20, 30))

        if external_donations.empty:
            empty_label = ctk.CTkLabel(list_frame, text="Aucun don externe enregistré",
                                      font=ctk.CTkFont(size=16), text_color="#888888")
            empty_label.pack(pady=50)
        else:
            for _, row in external_donations.iterrows():
                # Carte pour chaque don
                don_card = ctk.CTkFrame(list_frame, fg_color="#2a2a3e", corner_radius=10)
                don_card.pack(fill="x", pady=8)

                card_content = ctk.CTkFrame(don_card, fg_color="transparent")
                card_content.pack(fill="x", padx=20, pady=15)

                # En-tête (source + date)
                header_don = ctk.CTkFrame(card_content, fg_color="transparent")
                header_don.pack(fill="x", pady=(0, 10))

                source = row['source'] or "Externe"
                source_label = ctk.CTkLabel(header_don, text=f"Source: {source}",
                                           font=ctk.CTkFont(size=14, weight="bold"),
                                           text_color="#3b82f6")
                source_label.pack(side="left")

                date_label = ctk.CTkLabel(header_don, text=row['date_paiement'],
                                         font=ctk.CTkFont(size=12), text_color="#888888")
                date_label.pack(side="right")

                # Montant et motif
                amount_frame = ctk.CTkFrame(card_content, fg_color="transparent")
                amount_frame.pack(fill="x")

                donation_devise = row.get('devise', 'FC') if 'devise' in row else 'FC'
                montant_label = ctk.CTkLabel(amount_frame, text=f"{row['montant']:,.0f} {donation_devise}",
                                           font=ctk.CTkFont(size=18, weight="bold"),
                                           text_color="#10b981")
                montant_label.pack(side="left")

                motif = row['motif'] or "Sans motif"
                motif_label = ctk.CTkLabel(amount_frame, text=motif,
                                          font=ctk.CTkFont(size=12), text_color="#888888")
                motif_label.pack(side="right")

                # Bouton annuler don externe
                actions_don_frame = ctk.CTkFrame(card_content, fg_color="transparent")
                actions_don_frame.pack(fill="x", pady=(10, 0))

                cancel_don_btn = ctk.CTkButton(actions_don_frame, text="✖️ Annuler",
                                                fg_color="#ef4444", hover_color="#dc2626",
                                                height=35, width=120,
                                                font=ctk.CTkFont(size=12, weight="bold"),
                                                command=lambda fid=row['id']: self.cancel_external_donation(fid))
                cancel_don_btn.pack(side="right")

    def add_external_donation_dialog(self):
        """Dialogue pour ajouter un don externe"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajouter Don Externe")
        dw, dh = 700, 600
        dialog.geometry(f"{dw}x{dh}")
        dialog.minsize(680, 580)
        dialog.maxsize(750, 650)
        dialog.resizable(True, True)
        dialog.transient(self)
        dialog.grab_set()
        center_dialog(dialog, dw, dh)
        dialog.configure(fg_color="#1a1a2e")

        # Header
        header_frame = ctk.CTkFrame(dialog, fg_color="#10b981", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=20)

        title_label = ctk.CTkLabel(header_frame, text="Nouveau Don Externe",
                                 font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        title_label.pack(pady=15)

        # Formulaire scrollable
        form_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(15, 0))

        # Variables
        self.don_montant_var = ctk.StringVar()
        self.don_source_var = ctk.StringVar()
        self.don_motif_var = ctk.StringVar()
        self.don_devise_var = tk.StringVar(value="FC")
        self.don_date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        # Champs
        fields = [
            ("Montant *", self.don_montant_var, "entry", "100000"),
            ("Devise", self.don_devise_var, "option", ["FC", "$"]),
            ("Source / Donateur *", self.don_source_var, "entry", "Organisation, Personne..."),
            ("Date", self.don_date_var, "entry", "YYYY-MM-DD"),
            ("Motif", self.don_motif_var, "entry", "Campagne, Collecte, Offrande...")
        ]

        for label_text, var, field_type, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10)

            label = ctk.CTkLabel(field_frame, text=label_text,
                               font=ctk.CTkFont(size=14, weight="bold"))
            label.pack(anchor="w", pady=(0, 5))

            if field_type == "entry":
                entry = ctk.CTkEntry(field_frame, textvariable=var,
                                   placeholder_text=placeholder, height=40,
                                   font=ctk.CTkFont(size=12))
                entry.pack(fill="x")
            elif field_type == "option":
                option_menu = ctk.CTkOptionMenu(field_frame, values=placeholder,
                                              variable=var, height=40,
                                              font=ctk.CTkFont(size=12))
                option_menu.pack(fill="x")

        # Séparateur
        separator = ctk.CTkFrame(dialog, height=2, fg_color="#2e2f4a")
        separator.pack(side="bottom", fill="x", padx=20, pady=(10, 0))

        # Boutons
        btn_frame = ctk.CTkFrame(dialog, fg_color="#111827", corner_radius=10)
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        inner_btn = ctk.CTkFrame(btn_frame, fg_color="transparent")
        inner_btn.pack(fill="x", padx=10, pady=8)

        cancel_btn = ctk.CTkButton(inner_btn, text="Annuler",
                                 fg_color="#6b7280", height=45,
                                 command=dialog.destroy,
                                 font=ctk.CTkFont(size=14, weight="bold"))
        cancel_btn.pack(side="left", expand=True, padx=(0, 10))

        save_btn = ctk.CTkButton(inner_btn, text="Enregistrer Don",
                               fg_color="#10b981", height=45,
                               command=lambda: self.save_external_donation(dialog),
                               font=ctk.CTkFont(size=14, weight="bold"))
        save_btn.pack(side="right", expand=True, padx=(10, 0))

    def save_external_donation(self, dialog):
        """Sauvegarde un don externe"""
        try:
            # Validation montant
            montant_text = self.don_montant_var.get().strip().replace(',', '').replace(' ', '')
            if not montant_text:
                raise ValueError("Le montant est obligatoire")

            montant = float(montant_text)
            if montant <= 0:
                raise ValueError("Le montant doit être positif")

            # Récupérer la devise sélectionnée
            devise = self.don_devise_var.get()

            # Validation source
            source = self.don_source_var.get().strip()
            if not source:
                raise ValueError("La source du don est obligatoire")

            # Validation date
            date_str = self.don_date_var.get().strip()
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Format de date invalide (YYYY-MM-DD)")

            # Motif
            motif = self.don_motif_var.get().strip()
            if not motif:
                motif = "Don externe"
            
            # Ajouter la devise au motif pour affichage
            motif_with_currency = f"{motif} ({devise})"

            # Sauvegarde (membre_id = None pour don externe)
            if db.ajouter_finances(None, montant, "Don", motif_with_currency, source, date_str, devise):
                messagebox.showinfo("Succès", f"Don de {montant:,.0f} {devise} de {source} enregistré !")
                dialog.destroy()
                self.show_external_donations()
            else:
                messagebox.showerror("Erreur", "Impossible d'enregistrer le don.")

        except ValueError as e:
            messagebox.showerror("Erreur de validation", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue : {e}")

    def show_communiques(self):
        """Affiche la page des communiqués"""
        self.update_nav_styles("Communiqués")
        self.clear_main_frame()
        
        header = ctk.CTkFrame(self.main_frame, height=80)
        header.pack(fill="x", pady=(30,0))
        header.pack_propagate(False)
        title = ctk.CTkLabel(header, text="📢 Communiqués", font=ctk.CTkFont(size=32, weight="bold"))
        title.pack(expand=True)
        
        ctk.CTkLabel(self.main_frame, text="Module Communiqués en développement...", 
                    font=ctk.CTkFont(size=18)).pack(pady=50)

    def show_settings(self):
        self.update_nav_styles("Paramètres")
        self.clear_main_frame()
        
        header = ctk.CTkFrame(self.main_frame, height=80)
        header.pack(fill="x", pady=(30,0))
        header.pack_propagate(False)
        title = ctk.CTkLabel(header, text="⚙️ Paramètres", font=ctk.CTkFont(size=32, weight="bold"))
        title.pack(expand=True)
        
        ctk.CTkLabel(self.main_frame, text="Module Paramètres en développement...", 
                    font=ctk.CTkFont(size=18)).pack(pady=50)


if __name__ == "__main__":
    app = ShekinahApp()
    app.mainloop()
