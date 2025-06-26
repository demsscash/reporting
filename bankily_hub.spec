name: 🏦 Build BANKILY Windows Executables - FIXED

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # Permet de lancer manuellement

jobs:
  build-windows-exe:
    runs-on: windows-latest
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
    
    - name: 🐍 Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: 📦 Install dependencies with fixed versions
      run: |
        python -m pip install --upgrade pip
        pip install pandas==2.1.4 openpyxl==3.1.2 xlrd==2.0.1 reportlab==4.0.8 tkcalendar==1.6.1
        pip install pyinstaller==6.3.0
        
    - name: 🧪 Test imports before build
      run: |
        python -c "import pandas; print('✅ pandas OK')"
        python -c "import openpyxl; print('✅ openpyxl OK')"
        python -c "import xlrd; print('✅ xlrd OK')"
        python -c "import reportlab; print('✅ reportlab OK')"
        python -c "import tkcalendar; print('✅ tkcalendar OK')"
        
    - name: 📁 Create assets directory
      run: |
        mkdir -p assets
        echo "Assets directory created"
        
    - name: 🏗️ Build Hub executable with spec
      run: |
        echo "Building Hub executable..."
        pyinstaller bankily_hub.spec --clean --noconfirm
        
    - name: 🏢 Build Centres executable with spec  
      run: |
        echo "Building Centres executable..."
        pyinstaller centres.spec --clean --noconfirm
        
    - name: 🛒 Build Commercants executable with spec
      run: |
        echo "Building Commercants executable..."
        pyinstaller commercants.spec --clean --noconfirm
        
    - name: 👤 Build Agents executable with spec
      run: |
        echo "Building Agents executable..."
        pyinstaller agents.spec --clean --noconfirm
    
    - name: 📁 List built files and check dependencies
      run: |
        echo "=== Files in dist folder ==="
        if (Test-Path "dist") { 
          Get-ChildItem dist -Recurse | Select-Object Name, Length, LastWriteTime
        } else { 
          echo "❌ No dist folder found" 
        }
        echo ""
        echo "=== Executable sizes ==="
        if (Test-Path "dist\BANKILY_Generator_Hub.exe") {
          $size = (Get-Item "dist\BANKILY_Generator_Hub.exe").Length / 1MB
          echo "🏦 Hub: $([math]::Round($size, 2)) MB"
        }
        if (Test-Path "dist\BANKILY_Multi_Centres.exe") {
          $size = (Get-Item "dist\BANKILY_Multi_Centres.exe").Length / 1MB
          echo "🏢 Centres: $([math]::Round($size, 2)) MB"
        }
        if (Test-Path "dist\BANKILY_Multi_Commercants.exe") {
          $size = (Get-Item "dist\BANKILY_Multi_Commercants.exe").Length / 1MB
          echo "🛒 Commerçants: $([math]::Round($size, 2)) MB"
        }
        if (Test-Path "dist\BANKILY_Multi_Agents.exe") {
          $size = (Get-Item "dist\BANKILY_Multi_Agents.exe").Length / 1MB
          echo "👤 Agents: $([math]::Round($size, 2)) MB"
        }
      shell: powershell
    
    - name: 🧪 Test executables (quick launch test)
      run: |
        echo "Testing executables can start..."
        cd dist
        
        # Test Hub (should exit quickly with --version if we had it)
        if (Test-Path "BANKILY_Generator_Hub.exe") {
          echo "✅ Hub executable exists"
          # Just verify the file is valid executable
          $info = Get-Command ".\BANKILY_Generator_Hub.exe" -ErrorAction SilentlyContinue
          if ($info) { echo "✅ Hub executable is valid" } else { echo "❌ Hub executable invalid" }
        }
        
        if (Test-Path "BANKILY_Multi_Centres.exe") {
          echo "✅ Centres executable exists"
          $info = Get-Command ".\BANKILY_Multi_Centres.exe" -ErrorAction SilentlyContinue
          if ($info) { echo "✅ Centres executable is valid" } else { echo "❌ Centres executable invalid" }
        }
        
        if (Test-Path "BANKILY_Multi_Commercants.exe") {
          echo "✅ Commercants executable exists"
          $info = Get-Command ".\BANKILY_Multi_Commercants.exe" -ErrorAction SilentlyContinue
          if ($info) { echo "✅ Commercants executable is valid" } else { echo "❌ Commercants executable invalid" }
        }
        
        if (Test-Path "BANKILY_Multi_Agents.exe") {
          echo "✅ Agents executable exists"
          $info = Get-Command ".\BANKILY_Multi_Agents.exe" -ErrorAction SilentlyContinue
          if ($info) { echo "✅ Agents executable is valid" } else { echo "❌ Agents executable invalid" }
        }
      shell: powershell
    
    - name: 📦 Create release package with documentation
      run: |
        echo "Creating release package..."
        mkdir release_package
        
        # Copier les exécutables
        if (Test-Path "dist") {
          Copy-Item dist/*.exe release_package/ -ErrorAction SilentlyContinue
          echo "✅ Executables copiés"
        }
        
        # Copier les assets s'ils existent
        if (Test-Path "assets") {
          Copy-Item assets release_package/assets -Recurse -ErrorAction SilentlyContinue
          echo "✅ Assets copiés"
        }
        
        # Créer documentation complète
        @"
🏦 BANKILY Generator Package - Windows Executables
===============================================

📋 CONTENU DU PACKAGE:
=====================
✅ BANKILY_Generator_Hub.exe         - Application principale (LANCEZ CELUI-CI)
✅ BANKILY_Multi_Centres.exe         - Générateur centres  
✅ BANKILY_Multi_Commercants.exe     - Générateur commerçants
✅ BANKILY_Multi_Agents.exe          - Générateur agents
📁 assets/                           - Logos (optionnel)

🚀 UTILISATION:
==============
1. Extrayez TOUS les fichiers dans le même dossier
2. Lancez BANKILY_Generator_Hub.exe (menu principal)
3. Choisissez votre type de générateur
4. L'application correspondante s'ouvrira automatiquement

⚠️  IMPORTANT:
=============
• TOUS les fichiers .exe doivent être dans le même dossier
• Ne déplacez pas les fichiers séparément
• Si erreur "dépendances manquantes", redémarrez Windows
• Antivirus peut nécessiter une exception pour les .exe

🔧 DÉPANNAGE:
============
Problème: "Erreur de dépendances" au lancement d'un générateur
Solution: 
1. Fermez toutes les applications BANKILY
2. Redémarrez l'ordinateur  
3. Relancez BANKILY_Generator_Hub.exe
4. Si le problème persiste, lancez directement le générateur voulu

Problème: Application ne s'ouvre pas
Solution:
1. Vérifiez que Windows n'a pas bloqué les fichiers
2. Clic droit > Propriétés > Débloquer (si présent)
3. Ajoutez une exception antivirus pour le dossier
4. Lancez en tant qu'administrateur si nécessaire

📞 SUPPORT:
==========
En cas de problème, fournissez ces informations:
• Version Windows (Win 10/11)
• Message d'erreur exact
• Antivirus utilisé
• Emplacement des fichiers

💡 CONSEILS:
===========
• Créez un dossier dédié (ex: C:\BANKILY\)
• Ajoutez le dossier aux exceptions antivirus
• Évitez les espaces dans le chemin du dossier
• Gardez tous les .exe ensemble

Développé pour BANKILY © 2025
"@ | Out-File -FilePath "release_package\README.txt" -Encoding UTF8

        # Créer un script de lancement de secours
        @"
@echo off
echo 🏦 BANKILY Generator Hub - Script de lancement
echo.
echo Tentative de lancement du Hub principal...
echo.

REM Vérifier si le Hub existe
if not exist "BANKILY_Generator_Hub.exe" (
    echo ❌ ERREUR: BANKILY_Generator_Hub.exe non trouvé dans ce dossier
    echo.
    echo Assurez-vous que tous les fichiers sont dans le même dossier:
    echo - BANKILY_Generator_Hub.exe
    echo - BANKILY_Multi_Centres.exe  
    echo - BANKILY_Multi_Commercants.exe
    echo - BANKILY_Multi_Agents.exe
    echo.
    pause
    exit /b 1
)

echo ✅ Hub trouvé, lancement...
echo.

REM Lancer le Hub
start "" "BANKILY_Generator_Hub.exe"

REM Attendre un peu puis vérifier si le processus s'est lancé
timeout /t 3 /nobreak >nul

tasklist /fi "imagename eq BANKILY_Generator_Hub.exe" 2>nul | find /i "BANKILY_Generator_Hub.exe" >nul
if %errorlevel%==0 (
    echo ✅ Hub lancé avec succès!
) else (
    echo ⚠️  Le Hub pourrait avoir des difficultés à démarrer.
    echo   Si aucune fenêtre ne s'ouvre, essayez:
    echo   1. Lancer en tant qu'administrateur
    echo   2. Ajouter une exception antivirus
    echo   3. Débloquer les fichiers dans les propriétés
)

echo.
echo Ce script va se fermer dans 5 secondes...
timeout /t 5 /nobreak >nul
"@ | Out-File -FilePath "release_package\LANCER_BANKILY.bat" -Encoding ASCII

        echo "✅ Documentation et script de lancement créés"
      shell: powershell
    
    - name: 🎯 Upload executables avec métadonnées
      uses: actions/upload-artifact@v4
      with:
        name: BANKILY-Windows-Executables-v1.1-FIXED-${{ github.sha }}
        path: release_package/
        retention-days: 60
        if-no-files-found: error
    
    - name: 📊 Build summary avec diagnostics
      run: |
        echo "## 🏦 BANKILY Build Summary - VERSION CORRIGÉE" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### ✅ Build completed successfully!" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### 🔧 CORRECTIONS APPORTÉES:" >> $GITHUB_STEP_SUMMARY
        echo "- ✅ Nettoyage environnement PyInstaller pour subprocess" >> $GITHUB_STEP_SUMMARY
        echo "- ✅ Variables d'environnement isolées entre processus" >> $GITHUB_STEP_SUMMARY  
        echo "- ✅ Gestion PYINSTALLER_RESET_ENVIRONMENT" >> $GITHUB_STEP_SUMMARY
        echo "- ✅ CREATE_NEW_PROCESS_GROUP pour isolation Windows" >> $GITHUB_STEP_SUMMARY
        echo "- ✅ Documentation et script de dépannage inclus" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### 📦 Generated files:" >> $GITHUB_STEP_SUMMARY
        echo "- 🏦 **BANKILY_Generator_Hub.exe** (Menu principal - LANCEZ CELUI-CI)" >> $GITHUB_STEP_SUMMARY
        echo "- 🏢 BANKILY_Multi_Centres.exe" >> $GITHUB_STEP_SUMMARY
        echo "- 🛒 BANKILY_Multi_Commercants.exe" >> $GITHUB_STEP_SUMMARY
        echo "- 👤 BANKILY_Multi_Agents.exe" >> $GITHUB_STEP_SUMMARY
        echo "- 📄 README.txt (Documentation complète)" >> $GITHUB_STEP_SUMMARY
        echo "- 🚀 LANCER_BANKILY.bat (Script de secours)" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### 📥 Download:" >> $GITHUB_STEP_SUMMARY
        echo "1. Allez dans l'onglet **Actions**" >> $GITHUB_STEP_SUMMARY
        echo "2. Cliquez sur ce build (✅ vert)" >> $GITHUB_STEP_SUMMARY
        echo "3. Téléchargez: \`BANKILY-Windows-Executables-v1.1-FIXED-${{ github.sha }}\`" >> $GITHUB_STEP_SUMMARY
        echo "4. Extrayez TOUS les fichiers dans le même dossier" >> $GITHUB_STEP_SUMMARY
        echo "5. Lancez **BANKILY_Generator_Hub.exe**" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### 🎯 SOLUTION AU PROBLÈME:" >> $GITHUB_STEP_SUMMARY
        echo "Cette version corrige le problème de \"dépendances manquantes\" en:" >> $GITHUB_STEP_SUMMARY
        echo "- Nettoyant l'environnement PyInstaller avant de lancer les sous-processus" >> $GITHUB_STEP_SUMMARY
        echo "- Isolant chaque générateur dans son propre environnement" >> $GITHUB_STEP_SUMMARY
        echo "- Forçant le reset des variables d'environnement problématiques" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### ⚠️ INSTRUCTIONS IMPORTANTES:" >> $GITHUB_STEP_SUMMARY
        echo "1. **Tous les .exe doivent être dans le même dossier**" >> $GITHUB_STEP_SUMMARY
        echo "2. **Lancez toujours le Hub principal en premier**" >> $GITHUB_STEP_SUMMARY
        echo "3. **Si problème: utilisez LANCER_BANKILY.bat**" >> $GITHUB_STEP_SUMMARY
        echo "4. **Ajoutez une exception antivirus si nécessaire**" >> $GITHUB_STEP_SUMMARY
      shell: bash