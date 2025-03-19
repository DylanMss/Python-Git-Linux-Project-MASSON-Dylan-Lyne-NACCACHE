#!/bin/bash

# (Bitcoin sur Coinlore) 
URL="https://www.coinlore.com/coin/bitcoin"

echo "Scraping $URL ..."

# On recupere l'HTML en suivant les redirections
HTML=$(curl -s -L -A "Mozilla/5.0" "$URL")

# On supprime les retours à la ligne pour metre tout le HTML sur une ligne
HTML_ONELINE=$(echo "$HTML" | sed ':a;N;$!ba;s/\n//g')