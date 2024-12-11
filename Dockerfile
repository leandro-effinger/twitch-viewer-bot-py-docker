# Basis-Image mit vorinstalliertem Chrome und ChromeDriver
FROM selenium/standalone-chrome:latest

# Wechsle zum Arbeitsverzeichnis im Container
WORKDIR /app

# Python-Pakete installieren (pip und venv)
USER root
RUN apt-get update && apt-get install -y python3-pip python3-venv && rm -rf /var/lib/apt/lists/*

# Erstelle eine virtuelle Umgebung und installiere Abhängigkeiten
COPY requirements.txt .
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Kopiere den Anwendungscode in den Container
COPY . .

# Setze die virtuelle Umgebung als Standard
ENV PATH="/app/venv/bin:$PATH"

# Pfad zu ChromeDriver festlegen
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

# Skript ausführen
CMD ["/app/venv/bin/python", "script.py"]
