#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installationsscript für die Ehemaligen-Datenerfassungsplattform
================================================================

Dieses Script:
- Installiert alle nötigen Abhängigkeiten
- Setzt die Datenbank auf
- Erstellt einen Systemtask für den Autostart

Autor: GitHub Copilot
Datum: September 2025
"""

import os
import sys
import subprocess
import sqlite3
import hashlib
import platform
from pathlib import Path

# Farben für die Konsole
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def check_python_version():
    """Überprüft die Python-Version"""
    print_info("Überprüfe Python-Version...")
    
    if sys.version_info < (3, 7):
        print_error("Python 3.7 oder höher wird benötigt!")
        print_error(f"Aktuelle Version: {sys.version}")
        return False
    
    print_success(f"Python-Version OK: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Installiert die benötigten Python-Pakete"""
    print_info("Installiere Python-Abhängigkeiten...")
    
    requirements = ["flask"]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_success(f"Paket '{package}' installiert")
        except subprocess.CalledProcessError:
            print_error(f"Fehler beim Installieren von '{package}'")
            return False
    
    return True



def setup_database():
    """Initialisiert die SQLite-Datenbank"""
    print_info("Initialisiere Datenbank...")
    
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Prüfe ob die Tabelle bereits existiert und füge fehlende Spalten hinzu
        try:
            # Prüfe ob datenschutz_datum Spalte existiert
            cursor.execute("PRAGMA table_info(schueler_daten)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Füge fehlende Spalten hinzu falls sie nicht existieren
            if 'datenschutz_einwilligung' not in columns:
                cursor.execute('ALTER TABLE schueler_daten ADD COLUMN datenschutz_einwilligung BOOLEAN NOT NULL DEFAULT 1')
            
            if 'datenschutz_datum' not in columns:
                cursor.execute('ALTER TABLE schueler_daten ADD COLUMN datenschutz_datum TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                
        except sqlite3.OperationalError:
            # Tabelle existiert noch nicht, wird unten erstellt
            pass
        
        # Tabelle für Abitur-Jahrgänge
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS abitur_jahrgaenge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jahrgang INTEGER UNIQUE NOT NULL,
                aktiv BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabelle für Schülerdaten
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schueler_daten (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jahrgang_id INTEGER NOT NULL,
                vorname TEXT NOT NULL,
                nachname TEXT NOT NULL,
                email TEXT NOT NULL,
                datenschutz_einwilligung BOOLEAN NOT NULL DEFAULT 1,
                datenschutz_datum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (jahrgang_id) REFERENCES abitur_jahrgaenge (id)
            )
        ''')
        
        # Admin-Tabelle
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                benutzername TEXT UNIQUE NOT NULL,
                passwort_hash TEXT NOT NULL
            )
        ''')
        
        # Standard-Jahrgänge hinzufügen (2020-2030)
        for jahr in range(2020, 2031):
            cursor.execute('INSERT OR IGNORE INTO abitur_jahrgaenge (jahrgang) VALUES (?)', (jahr,))
        
        # Standard-Admin erstellen (admin/password)
        admin_passwort = hashlib.sha256('password'.encode()).hexdigest()
        cursor.execute('INSERT OR IGNORE INTO admins (benutzername, passwort_hash) VALUES (?, ?)', 
                       ('admin', admin_passwort))
        
        conn.commit()
        conn.close()
        
        print_success("Datenbank initialisiert")
        print_success("Standard-Jahrgänge (2020-2030) hinzugefügt")
        print_success("Admin-Benutzer erstellt: admin/password")
        
        return True
        
    except Exception as e:
        print_error(f"Fehler bei der Datenbank-Initialisierung: {e}")
        return False

def create_autostart_task():
    """Erstellt einen Autostart-Task für das System"""
    print_info("Erstelle Autostart-Task...")
    
    current_dir = os.path.abspath('.')
    python_path = sys.executable
    system_name = platform.system().lower()
    
    if system_name == "linux":
        # Linux systemd Service
        service_content = f"""[Unit]
Description=Ehemaligen Datenerfassung
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'www-data')}
WorkingDirectory={current_dir}
ExecStart={python_path} main.py
Restart=always
RestartSec=3
Environment=PYTHONPATH={current_dir}

[Install]
WantedBy=multi-user.target
"""
        
        try:
            with open('/tmp/datenerfassung.service', 'w') as f:
                f.write(service_content)
            
            print_success("Linux systemd Service erstellt: /tmp/datenerfassung.service")
            print_warning("Führen Sie folgende Befehle als root aus:")
            print_info("  sudo mv /tmp/datenerfassung.service /etc/systemd/system/")
            print_info("  sudo systemctl daemon-reload")
            print_info("  sudo systemctl enable datenerfassung")
            print_info("  sudo systemctl start datenerfassung")
            
        except Exception as e:
            print_warning(f"Linux Service-Datei konnte nicht erstellt werden: {e}")
    
    elif system_name == "darwin":  # macOS
        # macOS LaunchAgent
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.datenerfassung.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{current_dir}/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{current_dir}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/datenerfassung.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/datenerfassung-error.log</string>
</dict>
</plist>
"""
        
        try:
            home_dir = os.path.expanduser('~')
            launchagents_dir = os.path.join(home_dir, 'Library', 'LaunchAgents')
            os.makedirs(launchagents_dir, exist_ok=True)
            
            plist_path = os.path.join(launchagents_dir, 'com.datenerfassung.app.plist')
            
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            
            print_success(f"macOS LaunchAgent erstellt: {plist_path}")
            print_warning("Führen Sie folgende Befehle aus:")
            print_info(f"  launchctl load {plist_path}")
            print_info(f"  launchctl start com.datenerfassung.app")
            
        except Exception as e:
            print_warning(f"macOS LaunchAgent konnte nicht erstellt werden: {e}")
    
    elif system_name == "windows":
        # Windows Task Scheduler
        print_warning("Windows Autostart:")
        print_info("Erstellen Sie manuell eine geplante Aufgabe in der Aufgabenplanung:")
        print_info(f"  Programm: {python_path}")
        print_info(f"  Argumente: {current_dir}\\main.py")
        print_info(f"  Arbeitsverzeichnis: {current_dir}")
        print_info("  Trigger: Bei Systemstart")
    
    else:
        print_warning(f"Autostart für {system_name} nicht unterstützt")
    
    return True



def main():
    """Hauptfunktion des Installationsscripts"""
    print_header("EHEMALIGEN-DATENERFASSUNG INSTALLATION")
    
    print_info("Willkommen zur Installation der Ehemaligen-Datenerfassungsplattform!")
    print_info("Dieses Script installiert Abhängigkeiten, setzt die Datenbank auf")
    print_info("und erstellt einen Autostart-Task.\n")
    
    # Überprüfungen
    if not check_python_version():
        sys.exit(1)
    
    # Installation (nur die drei gewünschten Aufgaben)
    steps = [
        ("Python-Abhängigkeiten installieren", install_dependencies),
        ("Datenbank initialisieren", setup_database),
        ("Autostart-Task erstellen", create_autostart_task)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print_info(f"Führe aus: {step_name}")
        if not step_function():
            failed_steps.append(step_name)
    
    # Ergebnis
    print_header("INSTALLATION ABGESCHLOSSEN")
    
    if not failed_steps:
        print_success("✅ Installation erfolgreich abgeschlossen!")
        print("")
        print_info("🚀 Die Anwendung ist bereit:")
        print("   • Abhängigkeiten installiert")
        print("   • Datenbank eingerichtet")
        print("   • Autostart-Task erstellt")
        print("")
        print_info("Manuelle Schritte:")
        print("   1. Starten Sie die Anwendung: python3 main.py")
        print("   2. Öffnen Sie http://localhost:5000")
        print("   3. Admin-Login: http://localhost:5000/admin")
        print("   4. Standard-Anmeldung: admin / password")
        print("")
        print_warning("⚠️  WICHTIG: Ändern Sie das Admin-Passwort nach der ersten Anmeldung!")
    else:
        print_error("❌ Installation teilweise fehlgeschlagen!")
        print(f"   Fehlgeschlagene Schritte: {', '.join(failed_steps)}")
        print("")
        print_warning("Die Anwendung funktioniert möglicherweise trotzdem.")
        print_info("Überprüfen Sie die Fehlermeldungen und versuchen Sie es erneut.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n❌ Installation abgebrochen!")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n❌ Unerwarteter Fehler: {e}")
        sys.exit(1)