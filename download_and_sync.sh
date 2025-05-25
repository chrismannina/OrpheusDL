#!/bin/bash

# Combined Download and Sync Script
# Downloads albums and automatically syncs to Synology Drive

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "🎵 Download and Sync Workflow"
echo "============================="

# Check if links file is provided
LINKS_FILE="${1:-links.txt}"

if [ ! -f "$LINKS_FILE" ]; then
    echo "Error: Links file '$LINKS_FILE' not found"
    echo "Usage: $0 [links_file.txt]"
    exit 1
fi

echo "📥 Step 1: Downloading albums from $LINKS_FILE"
echo "----------------------------------------------"

# Run the download script
"$SCRIPT_DIR/download_links.sh" "$LINKS_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "📤 Step 2: Syncing to Synology Drive"
    echo "------------------------------------"
    
    # Run the sync script
    "$SCRIPT_DIR/sync_music.sh"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Complete workflow finished successfully!"
        echo "   - Albums downloaded to local storage"
        echo "   - Files synced to Synology Drive"
    else
        echo "❌ Sync failed, but downloads completed"
        exit 1
    fi
else
    echo "❌ Download failed, skipping sync"
    exit 1
fi 