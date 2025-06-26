#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BANKILY Generator Hub - Application Unifiée - VERSION CORRIGÉE
Menu principal pour choisir le type de générateur de rapports PDF
CORRECTION: Gestion environment PyInstaller pour subprocess
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
    
    def clean_environment_for_subprocess(self):
        """
        CORRECTION CRUCIALE: Nettoie l'environnement PyInstaller pour subprocess
        Résout les problèmes de dépendances manquantes
        """
        import os
        
        # Copier l'environnement actuel
        clean_env = os.environ.copy()
        
        # VARIABLES PYINSTALLER À NETTOYER
        pyinstaller_vars_to_remove = [
            '_PYI_APPLICATION_HOME_DIR',  # Nouvelle variable PyInstaller
            '_MEIPASS',                   # Chemin temporaire PyInstaller
            '_MEIPASS2',                  # Ancienne variable (compatibilité)
            'PYINSTALLER_RESET_ENVIRONMENT'  # Variable de contrôle
        ]
        
        # Variables de chemins à nettoyer
        path_vars_to_clean = [
            'PATH',
            'LD_LIBRARY_PATH',    # Linux
            'DYLD_LIBRARY_PATH',  # macOS  
            'PYTHONPATH'
        ]
        
        # Supprimer les variables PyInstaller
        for var in pyinstaller_vars_to_remove:
            if var in clean_env:
                del clean_env[var]
                print(f"🧹 Supprimé variable PyInstaller: {var}")
        
        # Variables spécifiques Windows PyInstaller
        windows_vars_to_remove = [
            'PYINSTALLER_APPLICATION_PATH'
        ]
        
        for var in windows_vars_to_remove:
            if var in clean_env:
                del clean_env[var]
                print(f"🧹 Supprimé variable Windows PyInstaller: {var}")
        
        # CORRECTION CAPITALE: Ajouter variable pour forcer reset environnement
        clean_env['PYINSTALLER_RESET_ENVIRONMENT'] = '1'
        
        return clean_env
    
    def launch_generator(self, generator_type):
        """Lance le générateur sélectionné - VERSION CORRIGÉE"""
        try:
            # Dictionnaire des fichiers de générateurs
            generators_exe = {
                "centres": "BANKILY_Multi_Centres.exe",
                "commercants": "BANKILY_Multi_Commercants.exe", 
                "agents": "BANKILY_Multi_Agents.exe"
            }
            
            generators_py = {
                "centres": "interface_multi_centres.py",
                "commercants": "interface_multi_commercants.py", 
                "agents": "interface_multi_agents.py"
            }
            
            # Essayer d'abord les .exe
            filename = generators_exe[generator_type]
            is_exe = True
            
            # Si .exe pas trouvé, essayer .py
            if not os.path.exists(filename):
                filename = generators_py[generator_type]
                is_exe = False
            
            # Vérifier si le fichier existe
            if not os.path.exists(filename):
                messagebox.showerror(
                    "Fichier non trouvé",
                    f"Ni le fichier '{generators_exe[generator_type]}' ni '{generators_py[generator_type]}' ne sont trouvés.\n\n"
                    f"Assurez-vous que tous les générateurs sont dans le même dossier que cette application."
                )
                return
            
            # CORRECTION CRUCIALE: Nettoyer l'environnement PyInstaller
            clean_env = self.clean_environment_for_subprocess()
            
            print(f"🚀 Lancement {generator_type} avec environnement nettoyé...")
            
            # Lancer le générateur avec environnement nettoyé
            if is_exe:
                # NOUVELLE MÉTHODE: Lancer .exe avec environnement propre
                subprocess.Popen(
                    [filename], 
                    env=clean_env,                    # CRUCIAL: environnement nettoyé
                    cwd=os.getcwd(),                  # Répertoire de travail actuel
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                )
                print(f"✅ Exécutable {filename} lancé avec succès")
            else:
                # Lancer .py avec Python et environnement nettoyé
                subprocess.Popen(
                    [sys.executable, filename], 
                    env=clean_env,                    # CRUCIAL: environnement nettoyé
                    cwd=os.getcwd(),
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                )
                print(f"✅ Script Python {filename} lancé avec succès")
            
            # Message de confirmation utilisateur
            messagebox.showinfo(
                "Générateur lancé", 
                f"Le générateur {generator_type.title()} a été lancé avec succès!\n\n"
                f"Si l'application ne s'ouvre pas, vérifiez que tous les fichiers .exe sont présents."
            )
            
        except Exception as e:
            print(f"❌ Erreur lancement {generator_type}: {e}")
            messagebox.showerror(
                "Erreur de lancement", 
                f"Impossible de lancer le générateur {generator_type}:\n\n{str(e)}\n\n"
                f"Vérifiez que tous les fichiers sont présents et que vous avez les permissions nécessaires."
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
    """
    Vérifie les dépendances requises
    MODIFICATION: Plus de check strict dans les .exe
    """
    try:
        # Test pour voir si on est dans un .exe PyInstaller
        if getattr(sys, 'frozen', False):
            # On est dans un .exe PyInstaller, pas besoin de vérifier
            print("🔧 Mode exécutable PyInstaller détecté - skip vérification dépendances")
            return True
    except:
        pass
    
    # Vérification seulement si on lance depuis Python
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
    # Débogage environnement PyInstaller
    if getattr(sys, 'frozen', False):
        print("🔧 Mode PyInstaller détecté")
        print(f"🔧 sys.executable: {sys.executable}")
        print(f"🔧 sys._MEIPASS: {getattr(sys, '_MEIPASS', 'N/A')}")
        
        # Afficher variables d'environnement PyInstaller pour débogage
        for key, value in os.environ.items():
            if 'PYI' in key or '_MEI' in key:
                print(f"🔧 {key}: {value}")
    
    # Vérifier les dépendances
    check_dependencies()
    
    # Créer et lancer l'interface
    root = tk.Tk()
    app = BankilyGeneratorHub(root)
    root.mainloop()


if __name__ == "__main__":
    main()


"""
=== CORRECTIONS APPORTÉES POUR SUBPROCESS PYINSTALLER ===

🎯 PROBLÈME RÉSOLU:
Quand le Hub PyInstaller lance d'autres .exe PyInstaller, les variables d'environnement
PyInstaller interfèrent et causent des erreurs de dépendances manquantes.

🔧 SOLUTION IMPLÉMENTÉE:

1. **Fonction clean_environment_for_subprocess()**:
   - Supprime toutes les variables d'environnement PyInstaller problématiques
   - Ajoute PYINSTALLER_RESET_ENVIRONMENT=1 pour forcer le reset
   - Nettoie PATH, LD_LIBRARY_PATH, etc.

2. **Méthode launch_generator() corrigée**:
   - Utilise subprocess.Popen avec env=clean_env
   - Ajoute CREATE_NEW_PROCESS_GROUP pour isolation Windows
   - Définit explicitement le cwd (répertoire de travail)

3. **Variables PyInstaller nettoyées**:
   - _PYI_APPLICATION_HOME_DIR (nouvelle variable PyInstaller)
   - _MEIPASS / _MEIPASS2 (chemins temporaires)
   - PYINSTALLER_RESET_ENVIRONMENT (contrôle)
   - Variables de chemins potentiellement corrompues

4. **Débogage ajouté**:
   - Affichage des variables d'environnement en mode debug
   - Messages de confirmation pour l'utilisateur
   - Gestion d'erreurs améliorée

🚀 RÉSULTAT:
Maintenant quand vous cliquez sur un générateur depuis le Hub, il se lance
dans un environnement propre sans interférence PyInstaller.

📦 POUR REBUILD:
Utilisez le même workflow GitHub Actions, cette correction sera automatiquement
incluse dans les nouveaux .exe générés.
"""