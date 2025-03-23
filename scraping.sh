#!/bin/bash
# Scrape le prix du Bitcoin depuis CoinDesk

URL="https://www.coindesk.com/price/bitcoin"
echo "Scraping $URL ..."

# Récupérer le HTML en simulant un navigateur
HTML=$(curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" "$URL")

# Sauvegarder le HTML
echo "$HTML" > debug_coindesk.html
echo "Le contenu HTML a été sauvegardé dans debug_coindesk.html"

# Extraction du prix
PRICE=$(echo "$HTML" | grep -oE '\$[0-9,]+\.[0-9]{2}' | head -n 1)

if [ -z "$PRICE" ]; then
    echo "Erreur : Prix non trouvé. Vérification de la regex ou la structure du HTML."
    exit 1
fi

echo "Prix actuel du Bitcoin : $PRICE"

# Nettoyage du symbole $ et des virgules
PRICE_CLEAN=$(echo "$PRICE" | tr -d '$' | tr -d ',')

# Enregistrer dans un fichier CSV
CSV_FILE="prices.csv"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

#  on crée l'entête
if [ ! -f "$CSV_FILE" ]; then
  echo "timestamp,price" > "$CSV_FILE"
fi

# On ajoute la nouvelle ligne
echo "$TIMESTAMP,$PRICE_CLEAN" >> "$CSV_FILE"
echo "Données enregistrées dans $CSV_FILE"
