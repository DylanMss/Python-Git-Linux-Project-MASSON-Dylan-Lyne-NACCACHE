#!/bin/bash
# Scrape the Bitcoin price from CoinDesk

URL="https://www.coindesk.com/price/bitcoin"
echo "Scraping $URL ..."

# Fetch the HTML while simulating a browser
HTML=$(curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" "$URL")

# Save the HTML for debugging
echo "$HTML" > debug_coindesk.html
echo "HTML content saved to debug_coindesk.html"

# Extract the price from the HTML
PRICE=$(echo "$HTML" | grep -oE '\$[0-9,]+\.[0-9]{2}' | head -n 1)

if [ -z "$PRICE" ]; then
    echo "Error: Price not found. Check the regex or HTML structure."
    exit 1
fi

echo "Current Bitcoin price: $PRICE"

# Clean up the dollar sign and commas
PRICE_CLEAN=$(echo "$PRICE" | tr -d '$' | tr -d ',')

# Save data to CSV file
CSV_FILE="prices.csv"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Create header
if [ ! -f "$CSV_FILE" ]; then
  echo "timestamp,price" > "$CSV_FILE"
fi

# Append the new line to the CSV
echo "$TIMESTAMP,$PRICE_CLEAN" >> "$CSV_FILE"
echo "Data saved to $CSV_FILE"
