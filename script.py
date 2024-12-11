import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Werte aus Umgebungsvariablen lesen
PROXY_CHOICE = int(os.getenv("PROXY_CHOICE", 1))  # Standardwert: 1
TWITCH_USERNAME = os.getenv("TWITCH_USERNAME", "default")  # Standardwert: "default"
PROXY_COUNT = int(os.getenv("PROXY_COUNT", 50))  # Standardwert: 50

PROXY_SERVERS = [
    "https://www.blockaway.net",
    "https://www.croxyproxy.com",
    "https://www.croxyproxy.rocks",
    "https://www.croxy.network",
    "https://www.croxy.org",
    "https://www.youtubeunblocked.live",
    "https://www.croxyproxy.net",
]

def log(message):
    """
    Einfacher Logger für Docker-Logs.
    """
    print(f"[LOG] {message}", flush=True)

def remove_overlays(driver):
    """
    Entferne störende Overlays wie Dialoge und Consent-Banner vollständig aus dem DOM.
    """
    overlay_selectors = [
        ".fc-dialog-overlay",  # Overlay
        ".fc-consent-root",    # Consent-Banner
    ]
    for selector in overlay_selectors:
        try:
            overlay = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            if overlay:
                driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", overlay)
        except Exception:
            pass  # Kein Overlay gefunden oder bereits entfernt

def open_new_connection(driver, proxy_url, active_connections):
    """
    Öffnet eine neue Verbindung zum Proxy-Server und interagiert mit Twitch.
    """
    try:
        driver.execute_script(f"window.open('{proxy_url}')")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(proxy_url)
        remove_overlays(driver)
        text_box = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, 'url'))  # Stelle sicher, dass das Element vorhanden ist
        )
        driver.execute_script("arguments[0].focus();", text_box)
        driver.execute_script(f"arguments[0].value = 'www.twitch.tv/{TWITCH_USERNAME}';", text_box)
        text_box.send_keys(Keys.RETURN)
        active_connections += 1
        log(f"Active connections: {active_connections}")
    except Exception as e:
        log(f"Error opening new connection: {e}")
    return active_connections

def main():
    log("Starting script execution.")

    proxy_url = PROXY_SERVERS[PROXY_CHOICE - 1]
    log(f"Using proxy: {proxy_url}")
    log(f"Twitch username: {TWITCH_USERNAME}")
    log(f"Proxy count: {PROXY_COUNT}")

    # Chrome-Optionen konfigurieren
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--headless')  # Headless-Modus für Docker
    chrome_options.add_argument('--disable-dev-shm-usage')  # Optimierung für Container
    chrome_options.add_argument('--no-sandbox')

    # ChromeDriver-Service explizit konfigurieren
    driver_service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    active_connections = 0

    try:
        driver.get(proxy_url)

        # Initiale Verbindungen aufbauen
        for _ in range(PROXY_COUNT):
            active_connections = open_new_connection(driver, proxy_url, active_connections)

        while True:
            log(f"Active connections: {active_connections}")

            # Überprüfe auf blockierte Verbindungen
            for handle in driver.window_handles[:]:
                driver.switch_to.window(handle)
                try:
                    if "blocked" in driver.page_source:  # Dummy-Bedingung ersetzen
                        log(f"Connection blocked, closing tab: {handle}")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])  # Zurück zum ersten Tab
                        active_connections -= 1
                        log(f"Active connections: {active_connections}")
                        active_connections = open_new_connection(driver, proxy_url, active_connections)
                except Exception:
                    continue

#            time.sleep(2)

    except KeyboardInterrupt:
        log("Received KeyboardInterrupt. Shutting down...")
    except Exception as e:
        log(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()
        log("All headless browsers have been closed.")
        log("Twitch Viewer Bot has stopped.")

if __name__ == '__main__':
    main()