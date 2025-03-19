#!/bin/bash

# (Bitcoin sur Coinlore) 
URL="https://www.coinlore.com/coin/bitcoin"

echo "Scraping $URL ..."

# On recupere l'HTML en suivant les redirections et en imitant un navigateur
HTML=$(curl -s -L -A "Mozilla/5.0" "$URL")

# On supprime les retours à la ligne pour metre tout le HTML sur une seule ligne
HTML_ONELINE=$(echo "$HTML" | tr -d '\n' | tr -d '\r')

# Sauvegarde du HTML dans un fichier debug pour voir le contenu
echo "$HTML_ONELINE" > debug.html
echo "The HTML content has been saved in debug.html"

# Vérifier que le HTML est bien récupéré (affiche les 300 premiers caractères)
echo "$HTML_ONELINE" | cut -c1-300

# Extraction du prix avec awk pour compatibilité macOS
PRICE=$(echo "$HTML_ONELINE" | awk -F'id="hprice"' '{print $2}' | awk -F'>' '{print $2}' | awk -F'<' '{print $1}' | tr -d '$' | tr -d ' ')

if [ -z "$PRICE" ]; then
    echo "Error: Price not found."
    exit 1
fi

echo "Current Bitcoin price: \$$PRICE"

# On supprime la virgule des milliers pour éviter d'avoir une colonne en trop
PRICE_CLEAN=$(echo "$PRICE" | tr -d ',')

# Récupérer la date et l'heure actuelles
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
CSV_FILE="prices.csv"

# Si le fichier n'existe pas ou est vide, on ajoute l'en-tête
if [ ! -f "$CSV_FILE" ] || [ ! -s "$CSV_FILE" ]; then
    echo "timestamp,price" > "$CSV_FILE"
fi

# Ajouter la nouvelle ligne avec timestamp et prix
echo "$TIMESTAMP,$PRICE_CLEAN" >> "$CSV_FILE"
echo "Data saved in $CSV_FILE"
