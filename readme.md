# Verzeichnisstuktur
## DjangoSettings
Im **DjangoSettings** Verzeichnis befinden sich ausschliesslich Dateien die von Django 
selbst generiert wurden und beinhalten Einstellungen und Konfigurationen.

## Dashboard
Im **Dashboard** Verzeichnis befinden sich alle für die Phase3 relevanten Dateien,
die für das Projekt umgesetzt wurden.

Dummy data is added for hans mustermann weeks KW30-KW32. New entries can be created in demand.

# Installationsanleitung
## 1. Anforderungen
1. Python muss mindestens in Version 3.13 installiert sein. Diese Version findet sich auf der Py-thon Website: https://www.python.org/downloads/release/python-3130/
2. Der Python Package Manager «Pip» muss installiert sein. Herunterladen des Installers get-pip.py von https://bootstrap.pypa.io/get-pip.py
   (Falls der Download nicht startet, den Anzeigequelltext in eine Datei namens get-pip.py speichern)
3. Öffnen eines Terminals und Ausführen des Installers mit Befehl «py get-pip.py» 
4. Sicherstellen Powershell Execution Policy ist aktiv mit folgendem Befehl im Terminal «Set-ExecutionPolicy -ExecutionPolicy Unrestricted”. 

## 2. Vorbereitung
1. Öffnen des Quellcode-Verzeichnisses und Herunterladen der Abhängigkeiten. Dazu sind folgende Schritte in einem Terminal notwendig. Diese müssen für jedes Phasen Verzeichnis wiederholt werden:
2. Erstellen eines virtuellen Environments mit dem Befehl «py -m venv .venv»
3. Aktivieren des virtuellen Environments mit dem Befehl «.venv/Scripts/activate» 
4. Installation der Abhängigkeiten mit dem Befehl «pip install -r requirements.txt»

## 3. Ausführung
Um den Django Server zu starten, muss im Hauptverzeichnis der entsprechenden Phase mit einem Terminal zunächst das virtuale Environment von Schritt 2.1 gestartet werden «.venv/Scripts/activate». Danach sollte folgender Befehl aufgeführt werden: «py manage.py runserver»
Die Applikation ist im Browser unter folgender URL aufrufbar:
-	http://localhost:8000/

Anmerkung: Anstelle des Internet Explorer sollte auf Windows immer Microsoft Edge verwendet wer-den.
