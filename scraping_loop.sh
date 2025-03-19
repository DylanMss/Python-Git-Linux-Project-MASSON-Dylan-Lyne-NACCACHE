#!/bin/bash

while true; do
    /bin/bash /Users/lynenaccache/Desktop/scrappingProject/scraping.sh >> /Users/lynenaccache/Desktop/scrappingProject/logfile.log 2>&1
    sleep 10  # Attendre 10 secondes avant de relancer
done

