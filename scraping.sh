#!/bin/bash

# (Bitcoin sur Coinlore) 
URL="https://www.coinlore.com/coin/bitcoin"

echo "Scraping $URL ..."

# On recupere l'HTML en suivant les redirections
HTML=$(curl -s -L -A "Mozilla/5.0" "$URL")

# On supprime les retours à la ligne pour metre tout le HTML sur une ligne
HTML_ONELINE=$(echo "$HTML" | sed ':a;N;$!ba;s/\n//g')


echo "$HTML_ONELINE" > debug.html
echo "Le contenu HTML a ete sauvegarde dans debug.html"

# voir si ca commence bien
echo "$HTML_ONELINE" | head -n 1 | cut -c1-300

# extraire le prix dans la balise span avec id hprice

PRICE=$(echo "$HTML_ONELINE" | grep -oP '(?<=\$)[0-9,\.]+' | head -n 1)

if [ -z "$PRICE" ]; then
    echo "Erreur : Prix non trouvé."
    exit 1
fi

echo "Prix actuel du Bitcoin : \$$PRICE"

# On supprime la virgule des milliers pour que le CSV ait deux colonnes seulement
PRICE_CLEAN=$(echo "$PRICE" | tr -d ',')

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
CSV_FILE="prices.csv"
# Si le fichier n'existe pas ou est vide, on ajoute l'entête
if [ ! -f "$CSV_FILE" ] || [ ! -s "$CSV_FILE" ]; then
    echo "timestamp,price" > "$CSV_FILE"
fi

echo "$TIMESTAMP,$PRICE_CLEAN" >> "$CSV_FILE"
echo "Donnee sauvegardee dans $CSV_FILE"