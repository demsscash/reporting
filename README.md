# 🏦 BANKILY Generator Suite

Suite complète de générateurs de rapports PDF pour BANKILY.

## 📋 Description

Application unifiée permettant de générer des rapports PDF professionnels pour :
- 🏢 **Multi-Centres** : Rapports par centre géographique
- 🛒 **Multi-Commerçants** : Rapports par commerçant individuel  
- 👤 **Multi-Agents** : Rapports d'agents avec calcul de commissions

## 🚀 Utilisation rapide

### Pour Windows (Executables)
1. Téléchargez la dernière version depuis les [Actions](../../actions)
2. Extrayez le fichier ZIP
3. Lancez `BANKILY_Generator_Hub.exe`
4. Choisissez votre type de générateur

### Pour développeurs (Python)
```bash
# Installation des dépendances
pip install pandas openpyxl xlrd reportlab tkcalendar

# Lancement de l'application principale
python bankily_generator_hub.py
```

## 📁 Structure des fichiers

```
📂 BANKILY Generator/
├── 🏦 bankily_generator_hub.py          # Menu principal
├── 🏢 interface_multi_centres.py        # Générateur centres
├── 🛒 interface_multi_commercants.py    # Générateur commerçants
├── 👤 interface_multi_agents.py         # Générateur agents
├── 📂 assets/                           # Logos et ressources
│   ├── bpm.png
│   └── bankily.png
└── 📂 .github/workflows/                # Build automatique
    └── build-exe.yml
```

## 📊 Colonnes Excel requises

### Multi-Centres
- `ID`, `DATEP`, `CLIENT`, `MONTANT`, `CENTRE`

### Multi-Commerçants  
- `ID`, `DATEP`, `CLIENT`, `MONTANT`, `COMMERCANT`

### Multi-Agents
- `DATE_TRS`, `ID_TRS`, `TYPE_OPERATION`, `TEL_CLIENT`, `COMMISSION`, `MONTANT`, `CODE_AGENT`

## 🔧 Fonctionnalités

✅ Interface graphique moderne et intuitive  
✅ Génération automatique par groupe (centre/commerçant/agent)  
✅ Export ZIP avec tous les rapports  
✅ Design professionnel BANKILY avec logos  
✅ Calculs automatiques des totaux  
✅ Gestion d'erreurs robuste  
✅ Journal des opérations en temps réel  

## 📦 Build automatique

Les exécutables Windows sont automatiquement générés via GitHub Actions à chaque modification du code.

Pour télécharger la dernière version :
1. Allez dans l'onglet **Actions**
2. Cliquez sur le build le plus récent (✅ vert)
3. Téléchargez l'artifact **BANKILY-Windows-Executables**

## 🛠️ Développement

### Prérequis
- Python 3.11+
- Modules : pandas, openpyxl, xlrd, reportlab, tkcalendar

### Installation locale
```bash
git clone https://github.com/[votre-username]/bankily-generator.git
cd bankily-generator
pip install -r requirements.txt
python bankily_generator_hub.py
```

## 📞 Support

Pour toute question ou problème, ouvrez une issue dans ce repository.

---

**Développé pour BANKILY** 🏦  
© 2025 - Tous droits réservés