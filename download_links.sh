#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Allow specifying the links file as an argument, default to links.txt
LINKS_FILE_NAME="${1:-links.txt}"

# Define the path to the links file relative to the script directory
LINKS_FILE="$SCRIPT_DIR/$LINKS_FILE_NAME"
# Define the path to the orpheus script relative to the script directory
ORPHEUS_SCRIPT="$SCRIPT_DIR/orpheus.py"

# Check if links file exists
if [ ! -f "$LINKS_FILE" ]; then
  echo "Error: $LINKS_FILE_NAME not found in the script directory ($SCRIPT_DIR)"
  echo "Usage: $0 [filename.txt]"
  echo "  If no filename is provided, 'links.txt' will be used"
  exit 1
fi

# Check if orpheus.py exists
if [ ! -f "$ORPHEUS_SCRIPT" ]; then
  echo "Error: orpheus.py not found in the script directory ($SCRIPT_DIR)"
  exit 1
fi

echo "Starting download process for $LINKS_FILE_NAME..."
echo "Found $(grep -c '^[^#[:space:]]' "$LINKS_FILE" 2>/dev/null || echo "0") links to process"

# Read the file line by line
while IFS= read -r link || [[ -n "$link" ]]; do
  # Skip empty lines or lines that might be just whitespace
  if [[ -z "$link" || "$link" =~ ^[[:space:]]*$ ]]; then
    continue
  fi

  # Skip comment lines (starting with #)
  if [[ "$link" =~ ^[[:space:]]*# ]]; then
    echo "Skipping comment: $link"
    continue
  fi

  echo "----------------------------------------"
  echo "Processing link: $link"
  echo "----------------------------------------"

  # Run the orpheus command with the link
  # Use relative path to virtual environment
  "$SCRIPT_DIR/venv/bin/python3" "$ORPHEUS_SCRIPT" "$link"

  # Check if the download was successful
  if [ $? -eq 0 ]; then
    echo "✓ Successfully processed: $link"
  else
    echo "✗ Failed to process: $link"
  fi

  # Optional: Add a small delay between downloads if needed
  sleep 2

done < "$LINKS_FILE"

echo "----------------------------------------"
echo "Finished processing all links in $LINKS_FILE_NAME"
echo "----------------------------------------"

exit 0