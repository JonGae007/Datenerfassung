# 📦 Ehemaligen-Datenerfassung

Eine sichere, DSGVO-konforme Webanwendung zur Erfassung von Abiturjahrgang-Daten mit administrativem Management-Panel.

## ✨ Features

- 🎓 **Jahrgangswahl** - Dynamische Auswahl der Abiturjahrgänge
- 👤 **Datenerfassung** - Name, Vorname, E-Mail mit Validierung
- 🔒 **DSGVO-konform** - Datenschutzerklärung und Einwilligungsverwaltung
- 🛡️ **Admin-Panel** - Sicherer Zugang zur Datenverwaltung
- 📊 **CSV-Export** - Einfacher Datenexport für weitere Verarbeitung
- 👥 **Benutzerverwaltung** - Admin-Accounts verwalten
- 🌙 **Dark/Light Mode** - Automatische Systemanpassung
- 📱 **Responsive Design** - Optimiert für alle Geräte
- 🔄 **Sortierbare Tabellen** - Interaktive Datenansicht

## 🚀 Schnellstart

### 1. Repository klonen
```bash
git clone https://github.com/JonGae007/Datenerfassung.git
cd Datenerfassung
```

### 2. Automatische Installation
```bash
python3 install.py
```

### 3. Anwendung starten
```bash
python3 main.py
```

### 4. Zugriff
- **Anwendung:** http://localhost:5000
- **Admin-Panel:** http://localhost:5000/admin
- **Standard-Login:** admin / password

## 📋 Systemanforderungen

- Python 3.7 oder höher
- Flask Framework
- SQLite3 (bereits in Python enthalten)

## 🔧 Installation

### Automatisch (empfohlen)
```bash
python3 install.py
```

### Manuell
```bash
# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install flask

# Anwendung starten
python3 main.py
```

## 📁 Projektstruktur

```
Datenerfassung/
├── main.py              # Haupt-Flask-Anwendung
├── database.db          # SQLite-Datenbank (wird erstellt)
├── install.py           # Installations-Script
├── .gitignore          # Git-Ausschlüsse
├── templates/          # HTML-Templates
│   ├── index.html      # Registrierungsformular
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── admin_jahrgaenge.html
│   ├── admin_benutzer.html
│   └── datenschutz.html
├── static/
│   ├── style.css       # Responsive CSS mit Theme-Support
│   └── script.js       # JavaScript-Funktionen
└── docs/
    ├── README.md       # Diese Datei
    └── UBUNTU.md       # Ubuntu-Installation
```

## 🗄️ Datenbank-Schema

### Tabelle: abitur_jahrgaenge
- `id` - Eindeutige ID
- `jahrgang` - Jahrgang (z.B. 2024)
- `aktiv` - Status (1=aktiv, 0=inaktiv)

### Tabelle: schueler_daten
- `id` - Eindeutige ID
- `jahrgang` - Gewählter Jahrgang
- `vorname` - Vorname
- `name` - Nachname
- `email` - E-Mail-Adresse
- `datenschutz_akzeptiert` - DSGVO-Einwilligung
- `zeitstempel` - Erfassungszeit

### Tabelle: admins
- `id` - Eindeutige ID
- `username` - Benutzername
- `password` - Gehashtes Passwort (SHA256)
- `erstellt_am` - Erstellungszeit

## 🔐 Sicherheit

- **Passwort-Hashing:** SHA256 mit Salt
- **Session-Management:** Flask-Sessions
- **Input-Validierung:** Server- und clientseitig
- **DSGVO-Compliance:** Einwilligung und Datenschutzerklärung
- **SQL-Injection-Schutz:** Parametrisierte Queries

## 💾 Backup

### Automatisches Backup (Linux/Mac)
```bash
# Backup-Script erstellen
echo '#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp database.db "backup_database_$DATE.db"
echo "Backup erstellt: backup_database_$DATE.db"' > backup.sh

chmod +x backup.sh
./backup.sh
```

### Manuelles Backup
```bash
cp database.db backup_database_$(date +%Y%m%d).db
```

## 📊 CSV-Export

Der CSV-Export ist im Admin-Panel verfügbar und enthält:
- Jahrgang
- Vorname
- Nachname
- E-Mail
- Datenschutz-Status
- Zeitstempel

Format: UTF-8 mit Komma-Trennung

## 🎨 Design-System

### CSS Custom Properties
```css
:root {
  --bg-color: light-dark(#ffffff, #1a1a1a);
  --text-color: light-dark(#333333, #ffffff);
  --primary-color: light-dark(#2c3e50, #3498db);
}
```

### Responsive Breakpoints
- **Mobile:** < 768px
- **Tablet:** 768px - 1024px
- **Desktop:** > 1024px

## 🔧 Konfiguration

### Hauptkonfiguration (main.py)
```python
# Port ändern
app.run(port=5000, debug=False, host='127.0.0.1')

# Debug-Modus aktivieren
app.run(debug=True)
```

### Datenschutzerklärung anpassen
Bearbeiten Sie `templates/datenschutz.html` und ersetzen Sie:
- `[Ihre Schule/Organisation]`
- `[Kontaktdaten]`
- `[Weitere Details]`

## 🚀 Produktions-Deployment

### Ubuntu Server
Siehe [UBUNTU.md](UBUNTU.md) für detaillierte Anleitung.

### Docker (optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 5000
CMD ["python3", "main.py"]
```

### nginx-Konfiguration
```nginx
server {
    listen 80;
    server_name ihre-domain.de;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🛠️ Entwicklung

### Lokale Entwicklung starten
```bash
git clone https://github.com/JonGae007/Datenerfassung.git
cd Datenerfassung
python3 -m venv venv
source venv/bin/activate
pip install flask
python3 main.py
```

### Debug-Modus
```python
# In main.py
app.run(debug=True)
```

### Logs aktivieren
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 API-Endpunkte

### Öffentlich
- `GET /` - Registrierungsformular
- `POST /` - Datenerfassung
- `GET /datenschutz` - Datenschutzerklärung

### Admin (Authentifizierung erforderlich)
- `GET /admin` - Dashboard
- `GET /admin/jahrgaenge` - Jahrgangsverwaltung
- `GET /admin/benutzer` - Benutzerverwaltung
- `POST /admin/export` - CSV-Export

## 🧪 Testing

### Manuelle Tests
1. Registrierung mit verschiedenen Jahrgängen
2. Admin-Login und Dashboard-Zugriff
3. CSV-Export Funktionalität
4. Responsive Design auf verschiedenen Geräten
5. Dark/Light Mode Wechsel

### Datenbank-Tests
```bash
# SQLite-Konsole öffnen
sqlite3 database.db

# Tabellen anzeigen
.tables

# Daten prüfen
SELECT * FROM schueler_daten LIMIT 5;
```

## 🔍 Troubleshooting

### Häufige Probleme

#### Port bereits belegt
```bash
# Port-Nutzung prüfen
lsof -i :5000

# Anderen Port verwenden
python3 main.py --port 8080
```

#### Datenbankfehler
```bash
# Datenbank neu erstellen
rm database.db
python3 main.py
```

#### CSS/JS nicht geladen
- Browser-Cache leeren
- Entwicklertools prüfen (F12)
- Pfade in Templates überprüfen

### Logs analysieren
```python
# Debug-Ausgabe aktivieren
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
```

## 📈 Performance-Optimierung

### Datenbankoptimierung
```sql
-- Indizes erstellen
CREATE INDEX idx_jahrgang ON schueler_daten(jahrgang);
CREATE INDEX idx_zeitstempel ON schueler_daten(zeitstempel);
```

### Flask-Optimierung
```python
# Produktions-Setup
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['TESTING'] = False
```

## 📞 Support

### Fehler melden
1. Issue auf GitHub erstellen
2. Logs und Fehlermeldungen anhängen
3. System-Informationen bereitstellen:
   ```bash
   python3 --version
   pip list
   uname -a  # Linux/Mac
   ```

### Beitragen
1. Fork des Repositories
2. Feature-Branch erstellen
3. Changes committen
4. Pull Request erstellen

## 📄 Lizenz

MIT License - siehe LICENSE-Datei für Details.

## 🏆 Credits

Entwickelt für die sichere Erfassung von Ehemaligen-Daten mit Fokus auf:
- Datenschutz-Compliance (DSGVO)
- Benutzerfreundlichkeit
- Responsive Design
- Sicherheit

---

## 📱 Screenshots

### Registrierungsformular
- Sauberes, modernes Design
- Jahrgangswahl-Dropdown
- DSGVO-Einwilligung
- Mobile-optimiert

### Admin-Dashboard
- Übersichtliche Datentabelle
- Sortier- und Filterfunktionen
- CSV-Export-Button
- Responsive Layout

### Benutzerverwaltung
- Admin-Accounts verwalten
- Passwörter sicher ändern
- Benutzer hinzufügen/entfernen

---

*Für technischen Support oder Feature-Anfragen bitte GitHub Issues verwenden.*