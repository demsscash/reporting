#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Graphique pour Rapports PDF Multi-Centres
Génère un rapport séparé pour chaque centre à partir d'un seul fichier Excel
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


class RapportMultiCentresGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Générateur de Rapports Multi-Centres - BANKILY")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.fichier_excel = None
        self.logo_bpm = None
        self.logo_bankily = None
        self.processing = False
        self.centres_data = {}
        
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
            name='TitreBanque',
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
            text="🏦 Générateur de Rapports Multi-Centres",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(expand=True)
        
        # Sections
        self.create_logo_section()
        self.create_file_section()
        self.create_centres_section()
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
    
    def create_date_section(self):
        """Section des dates"""
        frame = tk.LabelFrame(
            self.root,
            text="📅 Période du Rapport",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        )
        frame.pack(fill='x', padx=10, pady=5)
        
        # Date de début
        debut_frame = tk.Frame(frame, bg='#f0f0f0')
        debut_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(debut_frame, text="Date du:", bg='#f0f0f0', width=10).pack(side='left')
        self.date_debut = DateEntry(
            debut_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.date_debut.pack(side='left', padx=10)
        
        # Date de fin
        tk.Label(debut_frame, text="jusqu'au:", bg='#f0f0f0', width=10).pack(side='left', padx=(20, 0))
        self.date_fin = DateEntry(
            debut_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.date_fin.pack(side='left', padx=10)
        
        # Bouton date automatique
        tk.Button(
            debut_frame,
            text="📅 Aujourd'hui",
            command=self.set_today_dates,
            bg='#3498db',
            fg='white'
        ).pack(side='right')
    
    def create_file_section(self):
        """Section fichier Excel"""
        frame = tk.LabelFrame(
            self.root,
            text="📊 Fichier Excel Multi-Centres",
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
    
    def create_centres_section(self):
        """Section des centres détectés"""
        frame = tk.LabelFrame(
            self.root,
            text="🏢 Centres Détectés",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0'
        )
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Info
        info_frame = tk.Frame(frame, bg='#f0f0f0')
        info_frame.pack(fill='x', padx=5, pady=5)
        
        self.centres_info_label = tk.Label(
            info_frame,
            text="Sélectionnez un fichier Excel pour voir les centres",
            bg='#f0f0f0',
            fg='gray'
        )
        self.centres_info_label.pack(side='left')
        
        # Liste des centres
        list_frame = tk.Frame(frame, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.centres_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode='extended',
            font=('Courier', 9)
        )
        self.centres_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.centres_listbox.yview)
    
    def create_controls(self):
        """Contrôles"""
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(fill='x', padx=10, pady=10)
        
        self.generate_btn = tk.Button(
            frame,
            text="🚀 Générer Rapports par Centre",
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
    
    def set_today_dates(self):
        """Met la date d'aujourd'hui"""
        today = date.today()
        self.date_debut.set_date(today)
        self.date_fin.set_date(today)
        self.log_message(f"Dates mises à aujourd'hui: {today.strftime('%d/%m/%Y')}")
    
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
            title="Fichier Excel Multi-Centres",
            filetypes=[("Excel", "*.xls *.xlsx")]
        )
        
        if file_path:
            self.fichier_excel = file_path
            self.file_label.config(text=f"{os.path.basename(file_path)} ✅", fg='green')
            self.log_message(f"Fichier sélectionné: {os.path.basename(file_path)}")
            
            # Analyser les centres
            self.analyze_centres()
    
    def analyze_centres(self):
        """Analyse les centres dans le fichier"""
        try:
            self.log_message("🔍 Analyse des centres...")
            
            # Lire le fichier Excel en préservant les types de données
            if self.fichier_excel.endswith('.xls'):
                df = pd.read_excel(self.fichier_excel, engine='xlrd', dtype={'ID': str})
            else:
                df = pd.read_excel(self.fichier_excel, engine='openpyxl', dtype={'ID': str})
            
            # Vérifier si la colonne CENTRE existe
            if 'CENTRE' not in df.columns:
                messagebox.showerror("Erreur", "La colonne 'CENTRE' est introuvable dans le fichier Excel")
                return
            
            # Nettoyer les données et conserver les ID comme strings
            df['ID'] = df['ID'].astype(str)  # S'assurer que les ID restent des strings
            
            # Grouper par centre
            centres_groups = df.groupby('CENTRE')
            self.centres_data = {}
            
            # Vider la liste
            self.centres_listbox.delete(0, 'end')
            
            # Ajouter chaque centre
            for centre, data in centres_groups:
                count = len(data)
                total = data['MONTANT'].sum() if 'MONTANT' in data.columns else 0
                
                self.centres_data[centre] = data
                
                # Afficher dans la liste
                display_text = f"{centre:<20} | {count:>3} transactions | {total:>10,.0f} MRU".replace(',', ' ')
                self.centres_listbox.insert('end', display_text)
            
            # Mettre à jour l'info
            self.centres_info_label.config(
                text=f"{len(self.centres_data)} centres détectés | {len(df)} transactions total",
                fg='green'
            )
            
            self.log_message(f"✅ {len(self.centres_data)} centres analysés")
            
        except Exception as e:
            self.log_message(f"❌ Erreur analyse: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse: {e}")
    
    def generate_reports(self):
        """Lance génération des rapports"""
        if not self.fichier_excel:
            messagebox.showwarning("Aucun fichier", "Sélectionnez un fichier Excel")
            return
        
        if not self.centres_data:
            messagebox.showwarning("Aucun centre", "Aucun centre détecté")
            return
        
        if self.processing:
            return
        
        self.processing = True
        self.generate_btn.config(state='disabled', text="⏳ Génération...")
        self.download_btn.config(state='disabled')
        
        thread = threading.Thread(target=self._process_centres)
        thread.daemon = True
        thread.start()
    
    def _process_centres(self):
        """Traite chaque centre"""
        try:
            self.log_message("🚀 Début génération multi-centres")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                pdf_files = []
                total_centres = len(self.centres_data)
                
                for i, (centre, data) in enumerate(self.centres_data.items()):
                    try:
                        self.log_message(f"🏢 [{i+1}/{total_centres}] Centre: {centre}")
                        
                        pdf_path = self.create_centre_pdf(centre, data, temp_dir)
                        if pdf_path:
                            pdf_files.append(pdf_path)
                            transactions_count = len(data)
                            self.log_message(f"✅ PDF {centre}: {transactions_count} transactions")
                        
                        progress = ((i + 1) / total_centres) * 100
                        self.progress['value'] = progress
                        self.root.update_idletasks()
                        
                    except Exception as e:
                        self.log_message(f"❌ Erreur centre {centre}: {e}")
                
                if pdf_files:
                    self.log_message("📦 Création ZIP multi-centres...")
                    self.zip_path = self.create_zip(pdf_files)
                    self.log_message(f"🎉 ZIP créé: {len(pdf_files)} rapports")
                    self.root.after(0, lambda: self.download_btn.config(state='normal'))
                else:
                    self.log_message("❌ Aucun PDF généré")
        
        except Exception as e:
            self.log_message(f"❌ Erreur globale: {e}")
        
        finally:
            self.processing = False
            self.root.after(0, lambda: self.generate_btn.config(state='normal', text="🚀 Générer Rapports par Centre"))
            self.root.after(0, lambda: self.progress.config(value=0))
    
    def create_centre_pdf(self, centre_nom, centre_data, output_dir):
        """Crée PDF pour un centre"""
        try:
            # Nom du PDF
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_pdf = f"Rapport_{centre_nom.replace(' ', '_')}_{date_str}.pdf"
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
            self.add_header(story, centre_nom)
            
            # Tableau
            self.add_table(story, centre_data, centre_nom)
            
            # Résumé
            self.add_summary(story, centre_data)
            
            doc.build(story)
            return pdf_path
        
        except Exception as e:
            self.log_message(f"❌ Erreur PDF {centre_nom}: {e}")
            return None
    
    def add_header(self, story, centre_nom):
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
            "<b>Relevé de paiement commerçant BANKILY</b>", 
            self.styles['TitreBanque']
        ))
        story.append(Spacer(1, 20))
    
    def add_table(self, story, df, centre_nom):
        """Tableau style BANKILY"""
        # Calculer les dates automatiquement à partir des données du centre
        df['DATEP'] = pd.to_datetime(df['DATEP'])
        date_debut_auto = df['DATEP'].min().strftime("%d/%m/%Y")
        date_fin_auto = df['DATEP'].max().strftime("%d/%m/%Y")
        
        # Infos avec dates automatiques du centre
        style_commun = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ])
        
        # Première ligne - nom du centre
        info1 = [["Nom du centre :", centre_nom]]
        table1 = Table(info1, colWidths=[3.5*cm, 12.5*cm])
        table1.setStyle(style_commun)
        story.append(table1)
        
        # Deuxième ligne - dates automatiques du centre
        info2 = [["Date du :", date_debut_auto, "jusqu'au :", date_fin_auto]]
        table2 = Table(info2, colWidths=[3.5*cm, 3*cm, 2.5*cm, 7*cm])
        table2.setStyle(style_commun)
        story.append(table2)
        
        # Troisième ligne - numéro de compte
        info3 = [["No du compte :", "2000009"]]
        table3 = Table(info3, colWidths=[3.5*cm, 12.5*cm])
        table3.setStyle(style_commun)
        story.append(table3)
        
        story.append(Spacer(1, 15))
        
        # Totaux
        total_montant = df['MONTANT'].sum()
        
        totaux_data = [
            ["Total crédit :", f"{total_montant:,.1f} MRU".replace(',', ' ')],
            ["Total paiement :", f"{total_montant:,.1f} MRU".replace(',', ' ')]
        ]
        
        for ligne in totaux_data:
            table = Table([ligne], colWidths=[4*cm, 12*cm])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            story.append(table)
        
        story.append(Spacer(1, 20))
        
        # Tableau principal avec colonnes uniformes
        df_sorted = df.sort_values('DATEP', ascending=False)
        
        data = [["ID", "Date crédit compte", "Client", "Centre", "Montant de crédit"]]
        
        for _, row in df_sorted.iterrows():
            # Conserver l'ID complet comme string (avec les zéros en début)
            num_transaction = str(row['ID']).strip()
            # S'assurer qu'on ne perd pas les zéros du début
            if 'ID' in row and pd.notna(row['ID']):
                if isinstance(row['ID'], (int, float)):
                    # Si c'est un nombre, le convertir en string sans notation scientifique
                    num_transaction = f"{int(row['ID'])}"
                else:
                    num_transaction = str(row['ID']).strip()
            
            date_formatted = pd.to_datetime(row['DATEP']).strftime('%d/%m/%Y %H:%M')
            client = str(row['CLIENT']) if 'CLIENT' in row else ""
            
            data.append([
                num_transaction,  # ID complet conservé
                date_formatted,
                client,
                centre_nom,
                f"{row['MONTANT']:,.1f}".replace(',', ' ')
            ])
        
        # Tableau avec largeurs équilibrées pour éviter chevauchements
        table = Table(data, colWidths=[3.8*cm, 3.2*cm, 2.8*cm, 3.2*cm, 3*cm])
        table.setStyle(TableStyle([
            # En-tête bleu clair
            ('BACKGROUND', (0, 0), (-1, 0), Color(0.7, 0.8, 1.0)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Corps - texte uniforme
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),  # Taille uniforme
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # ID
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # Date
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # Client
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # Centre
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),   # Montant
            
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            
            # Padding uniforme pour éviter chevauchements
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            
            # Gestion du texte long
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
    
    def add_summary(self, story, df):
        """Résumé"""
        story.append(Spacer(1, 30))
        
        total = df['MONTANT'].sum()
        data = [[f"Total : {total:,.1f} MRU".replace(',', ' ')]]
        
        table = Table(data, colWidths=[17*cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ]))
        
        story.append(table)
    
    def create_zip(self, pdf_files):
        """Crée ZIP"""
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"Rapports_Multi_Centres_{date_str}.zip"
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
    app = RapportMultiCentresGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


"""
=== INSTALLATION REQUISE ===

pip install pandas openpyxl xlrd reportlab tkcalendar

=== UTILISATION ===

1. Lancez l'interface:
   python interface_multi_centres.py

2. Configurez les logos (optionnel):
   - Logo BPM (bpm.png)
   - Logo BANKILY (bankily.png)

3. Définissez la période:
   - Date du début
   - Date de fin
   - Ou cliquez "Aujourd'hui"

4. Sélectionnez votre fichier Excel:
   - Doit contenir une colonne "CENTRE"
   - Colonnes requises: ID, DATEP, CLIENT, MONTANT, CENTRE

5. Visualisez les centres détectés:
   - Liste avec nombre de transactions par centre
   - Montant total par centre

6. Générez les rapports:
   - Un PDF par centre automatiquement
   - Design BANKILY conservé
   - Nom du centre dans chaque rapport

7. Téléchargez le ZIP:
   - Tous les PDF regroupés
   - Nommage automatique avec timestamp

=== FONCTIONNALITÉS ===

✅ Séparation automatique par centre
✅ Rapport individuel pour chaque centre
✅ Dates personnalisables
✅ Design BANKILY préservé
✅ Logos BPM et BANKILY
✅ Export ZIP global
✅ Journal des opérations en temps réel
✅ Interface moderne et intuitive

=== STRUCTURE FICHIER EXCEL ===

Colonnes requises:
- ID: Identifiant de transaction
- DATEP: Date de la transaction
- CLIENT: Numéro client
- MONTANT: Montant de la transaction
- CENTRE: Nom du centre (ex: KSAR, ATAR, NEMA...)

Exemple:
ID                  | DATEP      | CLIENT   | MONTANT | CENTRE
0725062311123878750 | 2025-06-23 | 26040818 | 2100    | TARHILL
1225062310155366703 | 2025-06-23 | 48938988 | 2084    | BARKEOL
"""