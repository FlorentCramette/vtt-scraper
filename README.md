# VTT Scraper

## Description
VTT Scraper est un script automatisé permettant de surveiller les annonces de VTT sur plusieurs sites web :
- **Upway**
- **Rebike**
- **Le Bon Coin**

Le script extrait les annonces contenant un modèle précis de VTT (**Cube Stereo Hybrid 140 HPC**), stocke les résultats dans un fichier CSV et envoie des notifications par e-mail lorsqu'une nouvelle annonce est détectée.

## Fonctionnalités
- **Scraping des annonces** via **Selenium**.
- **Stockage des annonces** dans `data/vtt_annonces.csv`.
- **Comparaison des nouvelles annonces** avec celles déjà enregistrées.
- **Envoi d'un email** lorsque de nouvelles annonces sont trouvées.
- **Gestion des logs** dans `scraper.log`.

## Prérequis
### 📌 Environnement Python
Assurez-vous d'avoir **Python 3.x** installé sur votre machine.

### 📌 Dépendances Python
Installez les packages nécessaires en exécutant :
```bash
pip install -r requirements.txt
```

### 📌 Variables d'environnement
Définissez vos informations d'envoi d'e-mail dans un fichier `.env` ou via les variables d'environnement :
```bash
export EMAIL_SENDER="votre_email@gmail.com"
export EMAIL_PASSWORD="votre_mot_de_passe"
export EMAIL_RECEIVER="destinataire_email@gmail.com"
```

## Installation et Utilisation
### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/VOTRE_USER/vtt-scraper.git
cd vtt-scraper
```

### 2️⃣ Lancer le scraper
```bash
python src/vtt_scraper.py
```

Le script affichera dans les logs les annonces trouvées et enregistrera les résultats dans `data/vtt_annonces.csv`.

### 3️⃣ Programmer l'exécution automatique avec GitHub Actions
Le projet est configuré pour s'exécuter **deux fois par jour** grâce à GitHub Actions. Assurez-vous que votre repository contient un workflow dans `.github/workflows/scraper.yml`.

## Structure du Projet
```
📂 vtt-scraper/
 ├── 📂 data/                  # Stockage du fichier CSV des annonces
 ├── 📂 logs/                  # Fichiers logs
 ├── 📂 src/                   # Code source du scraper
 │   ├── vtt_scraper.py        # Script principal
 ├── .github/workflows/        # Configuration GitHub Actions
 ├── requirements.txt          # Dépendances Python
 ├── README.md                 # Documentation du projet
```

## Logs et Debugging
Toutes les exécutions du script sont enregistrées dans `scraper.log`. Pour voir les logs en temps réel :
```bash
tail -f scraper.log
```

## Contributions
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une **issue** ou une **pull request** si vous souhaitez améliorer le projet.

## Licence
Ce projet est sous licence MIT.

🚀 **Bon scraping !**

