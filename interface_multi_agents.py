#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Graphique pour Rapports PDF Multi-Agents BANKILY
Génère un rapport séparé pour chaque agent à partir d'un seul fichier Excel
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkcalendar import DateEntry
import os
import zipfile
import tempfile
import shutil
from datetime import datetime, date
import threading

# Imports reportlab
try:
    import pandas as pd
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.colors import Color
    from reportlab.lib import colors
    REPORTLAB_OK = True
except ImportError as e:
    print(f"Erreur d'import: {e}")
    REPORTLAB_OK = False


class RapportMultiAgentsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("👤 Générateur de Rapports Multi-Agents - BANKILY")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.fichier_excel = None
        self.logo_bpm = None
        self.logo_bankily = None
        self.processing = False
        self.agents_data = {}
        
        # Vérification des dépendances
        if not REPORTLAB_OK:
            self.show_dependency_error()
            return
        
        # Setup styles
        self.setup_pdf_styles()
        
        # Interface
        self.create_interface()
        
        # Vérifier logos
        self.check_logos()
    
    def show_dependency_error(self):
        """Affiche erreur dépendances"""
        error_frame = tk.Frame(self.root, bg='#e74c3c', padx=20, pady=20)
        error_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            error_frame,
            text="❌ ERREUR DE DÉPENDANCES",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#e74c3c'
        ).pack(pady=10)
        
        tk.Label(
            error_frame,
            text="pip install pandas openpyxl xlrd reportlab tkcalendar",
            font=('Courier', 10),
            fg='white',
            bg='#c0392b',
            relief='sunken',
            padx=10,
            pady=10
        ).pack(pady=10)
    
    def setup_pdf_styles(self):
        """Configure styles PDF"""
        self.styles = getSampleStyleSheet()
        
        # Titre noir
        self.styles.add(ParagraphStyle(
            name='TitreAgent',
            parent=self.styles['Title'],
            fontSize=16,
            spaceAfter=15,
            alignment=1,
            textColor=colors.black
        ))
    
    def create_interface(self):
        """Crée l'interface"""
        # Titre
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        title_frame.pack(fill='x', padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="👤 Générateur de Rapports Multi-Agents",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(expand=True)
        
        # Sections
        self.create_logo_section()
        self.create_file_section()
        self.create_agents_section()
        self.create_controls()
        self.create_log_section()
        self.create_progress()
    
    def create_logo_section(self):
        """Section logos"""
        frame = tk.LabelFrame(
            self.root,
            text="📷 Logos",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        )
        frame.pack(fill='x', padx=10, pady=5)
        
        # Logo BPM
        bpm_frame = tk.Frame(frame, bg='#f0f0f0')
        bpm_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(bpm_frame, text="Logo BPM:", bg='#f0f0f0').pack(side='left')
        self.bpm_label = tk.Label(bpm_frame, text="Non sélectionné", bg='#f0f0f0', fg='gray')
        self.bpm_label.pack(side='left', padx=10)
        tk.Button(bpm_frame, text="Parcourir", command=self.select_bpm_logo).pack(side='right')
        
        # Logo BANKILY
        bankily_frame = tk.Frame(frame, bg='#f0f0f0')
        bankily_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(bankily_frame, text="Logo BANKILY:", bg='#f0f0f0').pack(side='left')
        self.bankily_label = tk.Label(bankily_frame, text="Non sélectionné", bg='#f0f0f0', fg='gray')
        self.bankily_label.pack(side='left', padx=10)
        tk.Button(bankily_frame, text="Parcourir", command=self.select_bankily_logo).pack(side='right')
    
    def create_file_section(self):
        """Section fichier Excel"""
        frame = tk.LabelFrame(
            self.root,
            text="📊 Fichier Excel Multi-Agents",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        )
        frame.pack(fill='x', padx=10, pady=5)
        
        # Sélection fichier
        file_frame = tk.Frame(frame, bg='#f0f0f0')
        file_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(
            file_frame,
            text="📁 Sélectionner Fichier Excel",
            command=self.select_file,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold')
        ).pack(side='left')
        
        self.file_label = tk.Label(file_frame, text="Aucun fichier sélectionné", bg='#f0f0f0', fg='gray')
        self.file_label.pack(side='left', padx=20)
    
    def create_agents_section(self):
        """Section des agents détectés"""
        frame = tk.LabelFrame(
            self.root,
            text="👤 Agents Détectés",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        )
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Info
        info_frame = tk.Frame(frame, bg='#f0f0f0')
        info_frame.pack(fill='x', padx=5, pady=5)
        
        self.agents_info_label = tk.Label(
            info_frame,
            text="Sélectionnez un fichier Excel pour voir les agents",
            bg='#f0f0f0',
            fg='gray'
        )
        self.agents_info_label.pack(side='left')
        
        # Liste des agents
        list_frame = tk.Frame(frame, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.agents_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode='extended',
            font=('Courier', 9)
        )
        self.agents_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.agents_listbox.yview)
    
    def create_controls(self):
        """Contrôles"""
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(fill='x', padx=10, pady=10)
        
        self.generate_btn = tk.Button(
            frame,
            text="🚀 Générer Rapports par Agent",
            command=self.generate_reports,
            bg='#8e44ad',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=5
        )
        self.generate_btn.pack(side='left')
        
        self.download_btn = tk.Button(
            frame,
            text="💾 Télécharger ZIP",
            command=self.download_zip,
            bg='#f39c12',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            state='disabled'
        )
        self.download_btn.pack(side='left', padx=10)
        
        self.status_label = tk.Label(frame, text="Prêt", bg='#f0f0f0', fg='green')
        self.status_label.pack(side='right')
    
    def create_log_section(self):
        """Journal"""
        frame = tk.LabelFrame(
            self.root,
            text="📝 Journal",
            font=('Arial', 9, 'bold'),
            bg='#f0f0f0'
        )
        frame.pack(fill='x', padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            frame,
            height=6,
            font=('Courier', 8),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.log_text.pack(fill='x', padx=5, pady=5)
    
    def create_progress(self):
        """Progression"""
        self.progress = ttk.Progressbar(self.root, mode='determinate')
        self.progress.pack(fill='x', padx=10, pady=5)
    
    def log_message(self, message):
        """Ajoute message au journal"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')
        self.root.update_idletasks()
    
    def check_logos(self):
        """Vérifie logos existants"""
        if os.path.exists("assets/bpm.png"):
            self.logo_bpm = "assets/bpm.png"
            self.bpm_label.config(text="bpm.png ✅", fg='green')
        
        if os.path.exists("assets/bankily.png"):
            self.logo_bankily = "assets/bankily.png"
            self.bankily_label.config(text="bankily.png ✅", fg='green')
    
    def select_bpm_logo(self):
        """Sélectionne logo BPM"""
        file_path = filedialog.askopenfilename(
            title="Logo BPM",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.logo_bpm = file_path
            self.bpm_label.config(text=f"{os.path.basename(file_path)} ✅", fg='green')
            self.log_message(f"Logo BPM: {os.path.basename(file_path)}")
    
    def select_bankily_logo(self):
        """Sélectionne logo BANKILY"""
        file_path = filedialog.askopenfilename(
            title="Logo BANKILY",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.logo_bankily = file_path
            self.bankily_label.config(text=f"{os.path.basename(file_path)} ✅", fg='green')
            self.log_message(f"Logo BANKILY: {os.path.basename(file_path)}")
    
    def select_file(self):
        """Sélectionne le fichier Excel"""
        file_path = filedialog.askopenfilename(
            title="Fichier Excel Multi-Agents",
            filetypes=[("Excel", "*.xls *.xlsx")]
        )
        
        if file_path:
            self.fichier_excel = file_path
            self.file_label.config(text=f"{os.path.basename(file_path)} ✅", fg='green')
            self.log_message(f"Fichier sélectionné: {os.path.basename(file_path)}")
            
            # Analyser les agents
            self.analyze_agents()
    
    def analyze_agents(self):
        """Analyse les agents dans le fichier"""
        try:
            self.log_message("🔍 Analyse des agents...")
            
            # Lire le fichier Excel en préservant les types de données
            if self.fichier_excel.endswith('.xls'):
                df = pd.read_excel(self.fichier_excel, engine='xlrd', dtype={'ID_TRS': str})
            else:
                df = pd.read_excel(self.fichier_excel, engine='openpyxl', dtype={'ID_TRS': str})
            
            # Vérifier si la colonne CODE_AGENT existe
            if 'CODE_AGENT' not in df.columns:
                messagebox.showerror("Erreur", "La colonne 'CODE_AGENT' est introuvable dans le fichier Excel")
                return
            
            # Nettoyer les données et conserver les ID comme strings
            df['ID_TRS'] = df['ID_TRS'].astype(str)
            
            # Grouper par agent
            agents_groups = df.groupby('CODE_AGENT')
            self.agents_data = {}
            
            # Vider la liste
            self.agents_listbox.delete(0, 'end')
            
            # Ajouter chaque agent
            for agent, data in agents_groups:
                count = len(data)
                total_commission = data['COMMISSION'].sum() if 'COMMISSION' in data.columns else 0
                
                self.agents_data[agent] = data
                
                # Afficher dans la liste
                display_text = f"Agent {agent:<10} | {count:>3} transactions | {total_commission:>8,.1f} MRU".replace(',', ' ')
                self.agents_listbox.insert('end', display_text)
            
            # Mettre à jour l'info
            self.agents_info_label.config(
                text=f"{len(self.agents_data)} agents détectés | {len(df)} transactions total",
                fg='green'
            )
            
            self.log_message(f"✅ {len(self.agents_data)} agents analysés")
            
        except Exception as e:
            self.log_message(f"❌ Erreur analyse: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse: {e}")
    
    def generate_reports(self):
        """Lance génération des rapports"""
        if not self.fichier_excel:
            messagebox.showwarning("Aucun fichier", "Sélectionnez un fichier Excel")
            return
        
        if not self.agents_data:
            messagebox.showwarning("Aucun agent", "Aucun agent détecté")
            return
        
        if self.processing:
            return
        
        self.processing = True
        self.generate_btn.config(state='disabled', text="⏳ Génération...")
        self.download_btn.config(state='disabled')
        
        thread = threading.Thread(target=self._process_agents)
        thread.daemon = True
        thread.start()
    
    def _process_agents(self):
        """Traite chaque agent"""
        try:
            self.log_message("🚀 Début génération multi-agents")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                pdf_files = []
                total_agents = len(self.agents_data)
                
                for i, (agent, data) in enumerate(self.agents_data.items()):
                    try:
                        self.log_message(f"👤 [{i+1}/{total_agents}] Agent: {agent}")
                        
                        pdf_path = self.create_agent_pdf(agent, data, temp_dir)
                        if pdf_path:
                            pdf_files.append(pdf_path)
                            transactions_count = len(data)
                            commission_total = data['COMMISSION'].sum()
                            self.log_message(f"✅ PDF Agent {agent}: {transactions_count} transactions, {commission_total:.1f} MRU")
                        
                        progress = ((i + 1) / total_agents) * 100
                        self.progress['value'] = progress
                        self.root.update_idletasks()
                        
                    except Exception as e:
                        self.log_message(f"❌ Erreur agent {agent}: {e}")
                
                if pdf_files:
                    self.log_message("📦 Création ZIP multi-agents...")
                    self.zip_path = self.create_zip(pdf_files)
                    self.log_message(f"🎉 ZIP créé: {len(pdf_files)} rapports agents")
                    self.root.after(0, lambda: self.download_btn.config(state='normal'))
                else:
                    self.log_message("❌ Aucun PDF généré")
        
        except Exception as e:
            self.log_message(f"❌ Erreur globale: {e}")
        
        finally:
            self.processing = False
            self.root.after(0, lambda: self.generate_btn.config(state='normal', text="🚀 Générer Rapports par Agent"))
            self.root.after(0, lambda: self.progress.config(value=0))
    
    def create_agent_pdf(self, code_agent, agent_data, output_dir):
        """Crée PDF pour un agent"""
        try:
            # Nom du PDF
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_pdf = f"Releve_Agent_{code_agent}_{date_str}.pdf"
            pdf_path = os.path.join(output_dir, nom_pdf)
            
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=1.5*cm,
                leftMargin=1.5*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            story = []
            
            # En-tête
            self.add_header(story, code_agent)
            
            # Informations agent
            self.add_agent_info(story, agent_data, code_agent)
            
            # Tableau des transactions
            self.add_transactions_table(story, agent_data)
            
            doc.build(story)
            return pdf_path
        
        except Exception as e:
            self.log_message(f"❌ Erreur PDF Agent {code_agent}: {e}")
            return None
    
    def add_header(self, story, code_agent):
        """En-tête style BANKILY"""
        # Logos
        if self.logo_bpm and os.path.exists(self.logo_bpm):
            if self.logo_bankily and os.path.exists(self.logo_bankily):
                data = [[
                    Image(self.logo_bpm, width=3*cm, height=2*cm, kind='proportional'),
                    "",
                    Image(self.logo_bankily, width=3*cm, height=2*cm)
                ]]
                table = Table(data, colWidths=[4*cm, 9*cm, 4*cm])
                table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                story.append(table)
                story.append(Spacer(1, 20))
        
        # Titre
        story.append(Paragraph(
            "<b>Relevé Agent BANKILY</b>", 
            self.styles['TitreAgent']
        ))
        story.append(Spacer(1, 20))
    
    def add_agent_info(self, story, df, code_agent):
        """Informations de l'agent"""
        # Calculer les dates automatiquement à partir des données de l'agent
        df['DATE_TRS'] = pd.to_datetime(df['DATE_TRS'])
        date_debut_auto = df['DATE_TRS'].min().strftime("%d/%m/%Y")
        date_fin_auto = df['DATE_TRS'].max().strftime("%d/%m/%Y")
        
        # CORRECTION: Largeur de colonne étiquette fixe pour alignement parfait
        largeur_etiquette = 4*cm
        largeur_valeur = 13*cm
        
        # Style commun pour toutes les informations - ALIGNEMENT UNIFORME
        style_info_uniforme = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ])
        
        # Dates avec espacement amélioré
        info1 = [["Date du :", f"{date_debut_auto}   jusqu'au   {date_fin_auto}"]]
        table1 = Table(info1, colWidths=[largeur_etiquette, largeur_valeur])
        table1.setStyle(style_info_uniforme)
        story.append(table1)
        story.append(Spacer(1, 2))
        
        # Code Agent
        info2 = [["Code Agent :", code_agent]]
        table2 = Table(info2, colWidths=[largeur_etiquette, largeur_valeur])
        table2.setStyle(style_info_uniforme)
        story.append(table2)
        story.append(Spacer(1, 2))
        
        # Nom aggregateur (vide pour l'instant)
        info3 = [["Nom aggregateur :", ""]]
        table3 = Table(info3, colWidths=[largeur_etiquette, largeur_valeur])
        table3.setStyle(style_info_uniforme)
        story.append(table3)
        story.append(Spacer(1, 2))
        
        # Totaux
        nombre_transactions = len(df)
        total_commission = df['COMMISSION'].sum()
        
        # Total transactions
        info4 = [["Total transaction :", f"{nombre_transactions}"]]
        table4 = Table(info4, colWidths=[largeur_etiquette, largeur_valeur])
        table4.setStyle(style_info_uniforme)
        story.append(table4)
        story.append(Spacer(1, 2))
        
        # Total commission
        info5 = [["Total commission :", f"{total_commission:,.1f}".replace(',', ' ')]]
        table5 = Table(info5, colWidths=[largeur_etiquette, largeur_valeur])
        table5.setStyle(style_info_uniforme)
        story.append(table5)
        
        story.append(Spacer(1, 20))
    
    def add_transactions_table(self, story, df):
        """Tableau des transactions"""
        # Trier par date
        df_sorted = df.sort_values('DATE_TRS', ascending=True)
        
        # En-têtes du tableau
        data = [["Date trs", "ID trs", "Type opération", "Tel Client", "Commission", "Montant"]]
        
        for _, row in df_sorted.iterrows():
            # Format de la date
            date_formatted = pd.to_datetime(row['DATE_TRS']).strftime('%d/%m/%Y\n%H:%M:%S')
            
            # ID transaction complet
            id_transaction = str(row['ID_TRS']).strip()
            if 'ID_TRS' in row and pd.notna(row['ID_TRS']):
                if isinstance(row['ID_TRS'], (int, float)):
                    id_transaction = f"{int(row['ID_TRS'])}"
                else:
                    id_transaction = str(row['ID_TRS']).strip()
            
            # Type d'opération
            type_operation = str(row['TYPE_OPERATION']) if 'TYPE_OPERATION' in row else ""
            
            # Téléphone client
            tel_client = str(row['TEL_CLIENT']) if 'TEL_CLIENT' in row else ""
            
            # Commission et montant
            commission = f"{row['COMMISSION']:,.1f}".replace(',', ' ') if 'COMMISSION' in row else "0"
            montant = f"{row['MONTANT']:,.0f}".replace(',', ' ') if 'MONTANT' in row else "0"
            
            data.append([
                date_formatted,
                id_transaction,
                type_operation,
                tel_client,
                commission,
                montant
            ])
        
        # Créer le tableau avec largeurs optimisées
        table = Table(data, colWidths=[2.8*cm, 4*cm, 2.8*cm, 2.8*cm, 2.3*cm, 2.3*cm])
        table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), Color(0.7, 0.8, 1.0)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Corps
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Date
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # ID
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # Type
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Tél
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),   # Commission
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),   # Montant
            
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            
            # Padding optimisé
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            
            # Gestion du texte long
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        
        story.append(table)
    
    def create_zip(self, pdf_files):
        """Crée ZIP"""
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"Rapports_Multi_Agents_{date_str}.zip"
        zip_path = os.path.join(os.getcwd(), zip_name)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for pdf_file in pdf_files:
                zipf.write(pdf_file, os.path.basename(pdf_file))
        
        return zip_path
    
    def download_zip(self):
        """Télécharge ZIP"""
        if hasattr(self, 'zip_path') and os.path.exists(self.zip_path):
            save_path = filedialog.asksaveasfilename(
                title="Sauvegarder ZIP",
                defaultextension=".zip",
                filetypes=[("ZIP", "*.zip")],
                initialname=os.path.basename(self.zip_path)
            )
            
            if save_path:
                try:
                    shutil.copy2(self.zip_path, save_path)
                    self.log_message(f"💾 Sauvegardé: {save_path}")
                    messagebox.showinfo("Succès", f"ZIP sauvegardé:\n{save_path}")
                except Exception as e:
                    self.log_message(f"❌ Erreur: {e}")
        else:
            messagebox.showwarning("Aucun fichier", "Pas de ZIP à télécharger")


def main():
    """Lance l'application"""
    root = tk.Tk()
    app = RapportMultiAgentsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


"""
=== GÉNÉRATEUR DE RAPPORTS MULTI-AGENTS BANKILY ===

Ce script génère automatiquement des rapports PDF individuels pour chaque agent 
à partir d'un fichier Excel contenant les données de tous les agents.

=== INSTALLATION REQUISE ===

pip install pandas openpyxl xlrd reportlab tkcalendar

=== UTILISATION ===

1. Lancez l'interface:
   python interface_multi_agents.py

2. Configurez les logos (optionnel):
   - Logo BPM (bpm.png)
   - Logo BANKILY (bankily.png)

3. Sélectionnez votre fichier Excel:
   - Doit contenir une colonne "CODE_AGENT"
   - Colonnes requises: DATE_TRS, ID_TRS, TYPE_OPERATION, TEL_CLIENT, COMMISSION, MONTANT, CODE_AGENT

4. Visualisez les agents détectés:
   - Liste avec nombre de transactions par agent
   - Total des commissions par agent

5. Générez les rapports:
   - Un PDF par agent automatiquement
   - Format "Relevé Agent BANKILY" conforme au modèle
   - Calculs automatiques des totaux

6. Téléchargez le ZIP:
   - Tous les PDF regroupés
   - Nommage automatique avec timestamp

=== FONCTIONNALITÉS ===

✅ Séparation automatique par agent (CODE_AGENT)
✅ Rapport individuel pour chaque agent
✅ Format conforme au modèle BANKILY
✅ Calcul automatique des dates de période
✅ Total des transactions par agent
✅ Total des commissions par agent
✅ Logos BPM et BANKILY intégrés
✅ Export ZIP global
✅ Journal des opérations en temps réel
✅ Interface moderne et intuitive
✅ Gestion des différents types d'opérations
✅ Alignement parfait des informations

=== STRUCTURE FICHIER EXCEL ===

Colonnes requises:
- DATE_TRS: Date et heure de la transaction (format: YYYY-MM-DD HH:MM:SS)
- ID_TRS: Identifiant unique de transaction (ex: 0625062308383599295)
- TYPE_OPERATION: Type d'opération (Versement, Retrait client, Tr interne)
- TEL_CLIENT: Numéro de téléphone du client
- COMMISSION: Commission de l'agent (en MRU)
- MONTANT: Montant de la transaction (en MRU)
- CODE_AGENT: Code identificateur de l'agent (ex: 021340)

Exemple de données:
DATE_TRS            | ID_TRS              | TYPE_OPERATION | TEL_CLIENT | COMMISSION | MONTANT | CODE_AGENT
2025-06-23 08:38:35 | 0625062308383599295 | Versement      | 41886048   | 10         | 658     | 021340
2025-06-23 08:39:30 | 0625062308393052696 | Retrait client | 37300238   | 7.5        | 800     | 021340

=== FORMAT DU RAPPORT GÉNÉRÉ ===

Chaque rapport PDF contient:

1. **En-tête avec logos** BPM et BANKILY
2. **Titre**: "Relevé Agent BANKILY"
3. **Informations de l'agent**:
   - Date du: [calculée automatiquement] jusqu'au: [calculée automatiquement]
   - Code Agent: [CODE_AGENT]
   - Nom aggregateur: [vide - personnalisable]
   - Total transaction: [nombre de transactions]
   - Total commission: [somme des commissions en MRU]

4. **Tableau des transactions** avec colonnes:
   - Date trs (avec heure)
   - ID trs (identifiant complet)
   - Type opération
   - Tel Client
   - Commission
   - Montant

=== TYPES D'OPÉRATIONS SUPPORTÉS ===

- **Versement**: Dépôt d'argent (commission généralement 10 MRU)
- **Retrait client**: Retrait d'argent (commission variable: 5-35 MRU)
- **Tr interne**: Transfert interne (commission 0 MRU)

=== FONCTIONNALITÉS AVANCÉES ===

🔧 **Gestion intelligente**:
- Détection automatique du nombre d'agents
- Calcul automatique des périodes par agent
- Préservation des ID de transaction complets
- Formatage approprié des montants et commissions

📊 **Interface utilisateur**:
- Vue d'ensemble des agents détectés
- Progression en temps réel de la génération
- Journal détaillé des opérations
- Gestion d'erreurs robuste

🎯 **Qualité PDF**:
- Format A4 professionnel
- Alignement parfait des éléments
- Tableaux optimisés pour la lisibilité
- Design conforme aux standards BANKILY

=== COMPARAISON AVEC LE GÉNÉRATEUR CENTRES ===

Similitudes:
- Interface graphique identique
- Logique de génération similaire
- Export ZIP et gestion des logos
- Qualité PDF professionnelle

Différences:
- Colonnes spécifiques aux agents (CODE_AGENT, COMMISSION, etc.)
- Format de rapport "Relevé Agent" vs "Relevé commerçant"
- Calculs adaptés (commissions vs montants)
- Types d'opérations spécifiques aux agents

=== DÉPANNAGE ===

**Erreur "Colonne CODE_AGENT introuvable"**:
- Vérifiez que votre fichier Excel contient bien une colonne nommée exactement "CODE_AGENT"

**Erreur de format de date**:
- Assurez-vous que la colonne DATE_TRS est au format date/heure valide

**PDF vides ou incorrects**:
- Vérifiez que toutes les colonnes requises sont présentes
- Contrôlez les types de données (notamment ID_TRS en texte)

**Performance lente**:
- Pour de gros fichiers (>10000 lignes), la génération peut prendre plusieurs minutes
- Surveillez le journal pour suivre la progression
"""