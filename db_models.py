import sqlite3
from contextlib import contextmanager
from typing import Optional, List
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import base64
from pandas.io.formats.style import Styler

class ShekinahDB:
    DB_PATH = 'shekinah_choir.db'

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.DB_PATH)
        try:
            yield conn
        finally:
            conn.close()

    def validate_data(self, nom: str, montant: Optional[float] = None) -> bool:
        if not nom or len(nom.strip()) == 0:
            return False
        if montant is not None and montant <= 0:
            return False
        return True

    def ajouter_membre(self, nom: str, pupitre: str, telephone: str, statut: str = 'Actif', email: Optional[str] = None, commentaires: Optional[str] = None) -> Optional[int]:
        if not self.validate_data(nom):
            return None
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO membres (nom, pupitre, telephone, statut, email, commentaires_coach, date_adhesion)
                VALUES (?, ?, ?, ?, ?, ?, date('now'))
            ''', (nom, pupitre, telephone, statut, email, commentaires))
            conn.commit()
            return cursor.lastrowid

    def ajouter_finances(self, membre_id: int, montant: float, type_p: str, motif: str = '') -> bool:
        if not self.validate_data('', montant):
            return False
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO finances (membre_id, montant, type, motif)
                VALUES (?, ?, ?, ?)
            ''', (membre_id, montant, type_p, motif))
            conn.commit()
            return True

    def ajouter_communique(self, titre: str, contenu: str, priorite: str = 'Normal') -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO communiques (titre, contenu, priorite)
                VALUES (?, ?, ?)
            ''', (titre, contenu, priorite))
            conn.commit()
            return cursor.lastrowid

    def search_membres(self, query: str) -> pd.DataFrame:
        query = f"%{query}%"
        with self.get_connection() as conn:
            df = pd.read_sql_query(
                "SELECT * FROM membres WHERE actif=1 AND (nom LIKE ? OR pupitre LIKE ? OR telephone LIKE ?) ORDER BY nom",
                conn, params=(query, query, query)
            )
        return df

    def get_membres(self) -> pd.DataFrame:
        with self.get_connection() as conn:
            return pd.read_sql_query("SELECT * FROM membres WHERE actif=1 ORDER BY pupitre, nom", conn)

    def get_membre_by_id(self, membre_id: int) -> pd.DataFrame:
        """Détails complet membre par ID."""
        with self.get_connection() as conn:
            df = pd.read_sql_query(
                "SELECT * FROM membres WHERE id = ? AND actif=1", 
                conn, params=(membre_id,)
            )
            return df if not df.empty else pd.DataFrame()

    def update_membre(self, membre_id: int, **kwargs) -> bool:
        """Mettre à jour membre (champs sécurisés)."""
        fields = ['nom', 'pupitre', 'telephone', 'email', 'statut', 'commentaires_coach']
        updates = [f"{f}=?" for f in fields if f in kwargs]
        if not updates:
            return False
        values = [kwargs.get(f) for f in fields if f in kwargs] + [membre_id]
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE membres SET {', '.join(updates)} WHERE id = ?", values)
            conn.commit()
            return cursor.rowcount > 0

    def get_finances_membre(self, membre_id: int) -> pd.DataFrame:
        """Historique finances membre."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM finances WHERE membre_id = ? ORDER BY date_paiement DESC", 
                conn, params=(membre_id,)
            )

    def get_presences_membre(self, membre_id: int) -> pd.DataFrame:
        """Historique présences membre."""
        with self.get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM presences WHERE membre_id = ? ORDER BY seance_date DESC", 
                conn, params=(membre_id,)
            )

    def supprimer_membre(self, membre_id: int) -> bool:
        """Désactiver membre (soft delete)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE membres SET actif=0 WHERE id = ?", (membre_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_finances(self) -> pd.DataFrame:
        with self.get_connection() as conn:
            return pd.read_sql_query("SELECT * FROM finances ORDER BY date_paiement DESC", conn)

    def get_communiques(self) -> pd.DataFrame:
        with self.get_connection() as conn:
            return pd.read_sql_query("SELECT * FROM communiques ORDER BY date_publication DESC", conn)

    def get_solde_caisse(self) -> float:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(montant), 0) FROM finances WHERE type IN ('Cotisation', 'Don')
            """)
            return cursor.fetchone()[0]

    def get_finances_mensuel(self) -> pd.DataFrame:
        with self.get_connection() as conn:
            df = pd.read_sql_query("""
                SELECT strftime('%Y-%m', date_paiement) as mois, 
                       SUM(montant) as total 
                FROM finances GROUP BY mois ORDER BY mois
            """, conn)
            return df

    def export_excel_formaté(self, table: str, filename: str):
        if table == 'membres':
            df = self.get_membres()
            df_group = df.groupby('pupitre').apply(lambda x: x).reset_index(drop=True)
            with pd.ExcelWriter(f"{filename}.xlsx", engine='openpyxl') as writer:
                df_group.to_excel(writer, sheet_name='Membres', index=False)
                worksheet = writer.sheets['Membres']
                for col in worksheet.columns:
                    max_length = 0
                    column = col[0].column_letter
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column].width = adjusted_width
                # Titres gras
                from openpyxl.styles import Font
                for cell in worksheet[1]:
                    cell.font = Font(bold=True)
        elif table == 'finances':
            df = self.get_finances()
            df.to_excel(f"{filename}.xlsx", index=False)
        return f"{filename}.xlsx"

    def generer_communique_png(self, communique_id: int) -> str:
        df = self.get_communiques()
        row = df[df['id'] == communique_id].iloc[0]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis('tight')
        ax.axis('off')
        ax.text(0.5, 0.6, row['titre'], fontsize=20, ha='center', va='center', weight='bold', color='#FFD700')
        ax.text(0.5, 0.4, row['contenu'], fontsize=14, ha='center', va='center', wrap=True)
        ax.text(0.5, 0.2, f"Priorité: {row['priorite']} - {row['date_publication']}", fontsize=12, ha='center')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close()
        return f"data:image/png;base64,{img_str}"

    def sync_ready(self) -> dict:
        """Stub pour future Firebase sync."""
        return {"status": "ready", "records": self.get_membres().to_dict('records')}

# Instance globale
db = ShekinahDB()
