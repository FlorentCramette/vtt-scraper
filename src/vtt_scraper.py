import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

# Configuration
SEARCH_QUERY = "Cube Stereo Hybrid 160 HPC"
CSV_FILE = "data/vtt_annonces.csv"
LOG_FILE = "logs/scraper.log"
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Vérifier et créer le dossier logs/ s'il n'existe pas
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "scraper.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Vérifier et créer le dossier data/ s'il n'existe pas
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "vtt_annonces.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Configuration du logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URLs des sites à scraper
URLS = {
    "Upway": "https://upway.fr/search?q=Cube+Stereo+Hybrid+160+HPC",
    "Rebike": "https://rebike.com/fr/search?q=Cube+Stereo+Hybrid+160+HPC",
    "Le Bon Coin": "https://www.leboncoin.fr/recherche?category=57&text=Cube+Stereo+Hybrid+160+HPC"
}


# Fonction de scraping
def scrape_annonces():
    logging.info("Démarrage du scraping")
    nouvelles_annonces = []
    for site, url in URLS.items():
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f"Succès : Scraping de {site}")
            soup = BeautifulSoup(response.text, "html.parser")
            
            if site == "Upway":
                annonces = soup.find_all("div", class_="product-tile")
                for annonce in annonces:
                    titre = annonce.find("h2").text.strip()
                    prix = annonce.find("span", class_="price").text.strip()
                    lien = annonce.find("a")["href"]
                    nouvelles_annonces.append((site, titre, prix, f"https://upway.fr{lien}"))
            
            elif site == "Rebike":
                annonces = soup.find_all("div", class_="rebike-product-card")
                for annonce in annonces:
                    titre = annonce.find("h2").text.strip()
                    prix = annonce.find("span", class_="rebike-product-card-price").text.strip()
                    lien = annonce.find("a")["href"]
                    nouvelles_annonces.append((site, titre, prix, f"https://rebike.com{lien}"))
        else:
            logging.error(f"Échec : Impossible de scraper {site}, Code HTTP {response.status_code}")
    
    return nouvelles_annonces

# Fonction de stockage et de comparaison
def check_and_save_annonces(nouvelles_annonces):
    try:
        df_old = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        logging.warning("Fichier CSV non trouvé, création d'un nouveau fichier.")
        df_old = pd.DataFrame(columns=["Site", "Titre", "Prix", "Lien"])
    
    df_new = pd.DataFrame(nouvelles_annonces, columns=["Site", "Titre", "Prix", "Lien"])
    df_merged = pd.concat([df_old, df_new]).drop_duplicates(subset=["Lien"], keep=False)
    df_new.to_csv(CSV_FILE, index=False)
    logging.info(f"{len(df_merged)} nouvelles annonces détectées.")
    
    return df_merged

# Fonction d'envoi d'email
def send_email(new_entries):
    if new_entries.empty:
        logging.info("Aucune nouvelle annonce trouvée.")
        return
    
    subject = "Nouvelles annonces VTT Cube Stereo Hybrid 160 HPC"
    body = "\n".join([f"{row['Titre']} - {row['Prix']} ({row['Site']})\n{row['Lien']}" for _, row in new_entries.iterrows()])
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        logging.info("Email envoyé avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de l'envoi de l'email : {e}")

# Exécution du script
if __name__ == "__main__":
    logging.info("Lancement du script")
    annonces = scrape_annonces()
    nouvelles = check_and_save_annonces(annonces)
    send_email(nouvelles)
    logging.info("Fin du script")
