#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define the path to the links file relative to the script directory
LINKS_FILE="$SCRIPT_DIR/links.txt"
# Define the path to the orpheus script relative to the script directory
ORPHEUS_SCRIPT="$SCRIPT_DIR/orpheus.py"

# Check if links.txt exists
if [ ! -f "$LINKS_FILE" ]; then
  echo "Error: links.txt not found in the script directory ($SCRIPT_DIR)"
  exit 1
fi

# Check if orpheus.py exists
if [ ! -f "$ORPHEUS_SCRIPT" ]; then
  echo "Error: orpheus.py not found in the script directory ($SCRIPT_DIR)"
  exit 1
fi

echo "Starting download process..."

# Read the file line by line
while IFS= read -r link || [[ -n "$link" ]]; do
  # Skip empty lines or lines that might be just whitespace
  if [[ -z "$link" || "$link" =~ ^[[:space:]]*$ ]]; then
    continue
  fi

  echo "----------------------------------------"
  echo "Processing link: $link"
  echo "----------------------------------------"

  # Run the orpheus command with the link
  # Ensure you're using the correct python interpreter (python or python3)
  echo "python "$ORPHEUS_SCRIPT" "$link""

  # Optional: Add a small delay between downloads if needed
  sleep 2

done < "$LINKS_FILE"

echo "----------------------------------------"
echo "Finished processing all links in $LINKS_FILE"
echo "----------------------------------------"

exit 0