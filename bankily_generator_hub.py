#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BANKILY Generator Hub - Application Unifiée
Menu principal pour choisir le type de générateur de rapports PDF
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from datetime import datetime

class BankilyGeneratorHub:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 BANKILY Generator Hub - Centre de Génération de Rapports")
        self.root.geometry("1200x700")  # Plus large pour 3 cartes horizontales
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        # Définir une taille minimale
        self.root.minsize(1000, 600)
        
        # Centrer la fenêtre
        self.center_window()
        
        # Créer l'interface
        self.create_interface()
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """Crée l'interface principale"""
        # En-tête principal
        self.create_header()
        
        # Section des générateurs
        self.create_generators_section()
        
        # Section informations
        self.create_info_section()
        
        # Pied de page
        self.create_footer()
    
    def create_header(self):
        """Crée l'en-tête de l'application"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=120)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Logo et titre principal
        title_frame = tk.Frame(header_frame, bg='#2c3e50')
        title_frame.pack(expand=True, fill='both')
        
        # Titre principal
        tk.Label(
            title_frame,
            text="🏦 BANKILY",
            font=('Arial', 28, 'bold'),
            fg='#f39c12',
            bg='#2c3e50'
        ).pack(pady=(15, 5))
        
        tk.Label(
            title_frame,
            text="Centre de Génération de Rapports PDF",
            font=('Arial', 14),
            fg='white',
            bg='#2c3e50'
        ).pack()
        
        tk.Label(
            title_frame,
            text="Choisissez votre type de rapport",
            font=('Arial', 10, 'italic'),
            fg='#bdc3c7',
            bg='#2c3e50'
        ).pack(pady=(0, 15))
    
    def create_generators_section(self):
        """Crée la section des générateurs"""
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre de section
        tk.Label(
            main_frame,
            text="📊 Types de Générateurs Disponibles",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(pady=(0, 20))
        
        # Container horizontal pour les cartes
        cards_container = tk.Frame(main_frame, bg='#f0f0f0')
        cards_container.pack(fill='both', expand=True, padx=10)
        
        # Configuration des colonnes pour distribution égale
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1) 
        cards_container.grid_columnconfigure(2, weight=1)
        
        # Générateur Multi-Centres (colonne 0)
        centres_frame = tk.Frame(cards_container, bg='#f0f0f0')
        centres_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.create_generator_card(
            centres_frame,
            "🏢 Multi-Centres",
            "Génère un rapport par centre géographique",
            "• Colonne requise: CENTRE\n• Format: Relevé commerçant\n• Groupement par zones\n• Idéal pour analyser les performances par région",
            "#3498db",
            lambda: self.launch_generator("centres")
        )
        
        # Générateur Multi-Commerçants (colonne 1)
        commercants_frame = tk.Frame(cards_container, bg='#f0f0f0')
        commercants_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.create_generator_card(
            commercants_frame,
            "🛒 Multi-Commerçants",
            "Génère un rapport par commerçant individuel",
            "• Colonne requise: COMMERCANT\n• Format: Relevé commerçant\n• Groupement par boutiques\n• Parfait pour les rapports individuels de magasins",
            "#27ae60",
            lambda: self.launch_generator("commercants")
        )
        
        # Générateur Multi-Agents (colonne 2)
        agents_frame = tk.Frame(cards_container, bg='#f0f0f0')
        agents_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.create_generator_card(
            agents_frame,
            "👤 Multi-Agents",
            "Génère un rapport par agent BANKILY",
            "• Colonne requise: CODE_AGENT\n• Format: Relevé agent\n• Calcul des commissions\n• Spécialisé pour les transactions d'agents",
            "#8e44ad",
            lambda: self.launch_generator("agents")
        )
    
    def create_generator_card(self, parent, title, description, details, color, command):
        """Crée une carte pour un générateur"""
        # Frame principal de la carte - maintenant en pack pour remplir le parent
        card_frame = tk.Frame(parent, bg='white', relief='raised', bd=2)
        card_frame.pack(fill='both', expand=True)
        
        # En-tête de la carte
        header_frame = tk.Frame(card_frame, bg=color, height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=title,
            font=('Arial', 12, 'bold'),
            fg='white',
            bg=color
        ).pack(expand=True)
        
        # Contenu de la carte
        content_frame = tk.Frame(card_frame, bg='white')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Description
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=('Arial', 9, 'bold'),
            bg='white',
            fg='#2c3e50',
            wraplength=200,  # Ajustement du texte pour cartes plus étroites
            justify='left'
        )
        desc_label.pack(anchor='w', pady=(0, 8))
        
        # Détails
        details_label = tk.Label(
            content_frame,
            text=details,
            font=('Arial', 8),
            bg='white',
            fg='#7f8c8d',
            justify='left',
            wraplength=200,  # Ajustement du texte pour cartes plus étroites
            anchor='w'
        )
        details_label.pack(anchor='w', pady=(0, 15))
        
        # Bouton de lancement
        launch_btn = tk.Button(
            content_frame,
            text="🚀 Lancer",
            command=command,
            bg=color,
            fg='white',
            font=('Arial', 9, 'bold'),
            relief='flat',
            padx=12,
            pady=5,
            cursor='hand2'
        )
        launch_btn.pack(anchor='center', pady=(5, 0))
        
        # Effet hover
        def on_enter(e):
            launch_btn.config(bg=self.darken_color(color))
        
        def on_leave(e):
            launch_btn.config(bg=color)
        
        launch_btn.bind("<Enter>", on_enter)
        launch_btn.bind("<Leave>", on_leave)
    
    def create_info_section(self):
        """Crée la section d'informations"""
        info_frame = tk.LabelFrame(
            self.root,
            text="ℹ️ Informations Importantes",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        info_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        info_text = """📋 PRÉREQUIS:
• Python avec les bibliothèques: pandas, openpyxl, xlrd, reportlab, tkcalendar
• Fichiers Excel avec les colonnes appropriées selon le type choisi
• Logos optionnels: bpm.png et bankily.png dans le dossier de travail

🎯 FONCTIONNALITÉS COMMUNES:
• Interface graphique intuitive avec progression en temps réel
• Export ZIP avec tous les rapports générés
• Design professionnel BANKILY avec logos
• Gestion d'erreurs robuste et journal détaillé"""
        
        tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#34495e',
            justify='left'
        ).pack(padx=12, pady=8, anchor='w')
    
    def create_footer(self):
        """Crée le pied de page"""
        footer_frame = tk.Frame(self.root, bg='#34495e', height=50)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        # Informations de version et date
        version_info = f"BANKILY Generator Hub v1.0 | {datetime.now().strftime('%Y')}"
        
        tk.Label(
            footer_frame,
            text=version_info,
            font=('Arial', 9),
            fg='#bdc3c7',
            bg='#34495e'
        ).pack(expand=True)
    
    def darken_color(self, color):
        """Assombrit une couleur pour l'effet hover"""
        color_map = {
            "#3498db": "#2980b9",
            "#27ae60": "#229954", 
            "#8e44ad": "#7d3c98"
        }
        return color_map.get(color, color)
    
    def launch_generator(self, generator_type):
        """Lance le générateur sélectionné"""
        try:
            # Dictionnaire des fichiers de générateurs
            generators = {
                "centres": "interface_multi_centres.py",
                "commercants": "interface_multi_commercants.py", 
                "agents": "interface_multi_agents.py"
            }
            
            filename = generators[generator_type]
            
            # Vérifier si le fichier existe
            if not os.path.exists(filename):
                messagebox.showerror(
                    "Fichier non trouvé",
                    f"Le fichier '{filename}' est introuvable.\n\n"
                    f"Assurez-vous que tous les générateurs sont dans le même dossier que cette application."
                )
                return
            
            # Lancer le générateur directement sans popup
            subprocess.Popen([sys.executable, filename])
            
        except Exception as e:
            messagebox.showerror(
                "Erreur de lancement", 
                f"Impossible de lancer le générateur:\n{str(e)}"
            )
    
    def show_about(self):
        """Affiche la boîte À propos"""
        about_text = """BANKILY Generator Hub v1.0

Application unifiée pour la génération de rapports PDF BANKILY.

Fonctionnalités:
• 3 types de générateurs spécialisés
• Interface graphique moderne
• Export PDF professionnel
• Gestion multi-fichiers

Développé pour BANKILY
© 2025 - Tous droits réservés"""
        
        messagebox.showinfo("À propos", about_text)


def check_dependencies():
    """Vérifie les dépendances requises"""
    required_modules = ['pandas', 'reportlab', 'tkcalendar']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"""❌ MODULES MANQUANTS:

Les modules suivants sont requis mais non installés:
{', '.join(missing_modules)}

Pour installer:
pip install {' '.join(missing_modules)} openpyxl xlrd

L'application peut fonctionner mais les générateurs nécessiteront ces modules."""
        
        messagebox.showwarning("Dépendances manquantes", error_msg)
    
    return len(missing_modules) == 0


def main():
    """Lance l'application principale"""
    # Vérifier les dépendances
    check_dependencies()
    
    # Créer et lancer l'interface
    root = tk.Tk()
    app = BankilyGeneratorHub(root)
    root.mainloop()


if __name__ == "__main__":
    main()


"""
=== BANKILY GENERATOR HUB ===

Application unifiée qui centralise l'accès aux 3 générateurs de rapports BANKILY.

=== STRUCTURE DU PROJET ===

Votre dossier doit contenir ces fichiers:
├── bankily_generator_hub.py          # ← Ce fichier (menu principal)
├── interface_multi_centres.py        # Générateur centres
├── interface_multi_commercants.py    # Générateur commerçants  
├── interface_multi_agents.py         # Générateur agents
├── bpm.png                           # Logo BPM (optionnel)
└── bankily.png                       # Logo BANKILY (optionnel)

=== UTILISATION ===

1. Placez tous les fichiers dans le même dossier
2. Lancez: python bankily_generator_hub.py
3. Choisissez votre type de générateur
4. L'interface correspondante s'ouvrira automatiquement

=== FONCTIONNALITÉS ===

🎯 **Menu principal moderne**:
- Interface intuitive avec cartes visuelles
- Descriptions détaillées de chaque générateur
- Boutons de lancement directs
- Informations sur les prérequis

🚀 **Lancement automatique**:
- Vérification de l'existence des fichiers
- Ouverture des générateurs en sous-processus
- Messages de confirmation
- Gestion d'erreurs complète

📊 **3 générateurs intégrés**:
- Multi-Centres (colonne CENTRE)
- Multi-Commerçants (colonne COMMERCANT)  
- Multi-Agents (colonne CODE_AGENT)

⚡ **Fonctionnalités avancées**:
- Vérification des dépendances au démarrage
- Interface responsive et moderne
- Effets visuels (hover, couleurs)
- Fenêtre centrée automatiquement

=== AVANTAGES ===

✅ **Simplicité d'usage**: Un seul point d'entrée pour tous les générateurs
✅ **Interface moderne**: Design professionnel avec codes couleurs
✅ **Robustesse**: Vérifications et gestion d'erreurs complètes
✅ **Flexibilité**: Chaque générateur reste indépendant
✅ **Maintenance**: Centralisation des accès et informations

=== INSTALLATION COMPLÈTE ===

1. **Téléchargez tous les fichiers Python**:
   - bankily_generator_hub.py
   - interface_multi_centres.py
   - interface_multi_commercants.py
   - interface_multi_agents.py

2. **Installez les dépendances**:
   pip install pandas openpyxl xlrd reportlab tkcalendar

3. **Ajoutez les logos** (optionnel):
   - bpm.png
   - bankily.png

4. **Lancez l'application**:
   python bankily_generator_hub.py

Et voilà ! Vous avez maintenant un centre de contrôle complet pour tous vos rapports BANKILY.
"""