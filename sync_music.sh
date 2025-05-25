#!/bin/bash

# Music Sync Script - Copy from downloads to Synology Drive
# Usage: ./sync_music.sh [--dry-run] [--delete]

SOURCE_DIR="/Users/chrismannina/Music/downloads"
DEST_DIR="/Users/chrismannina/Library/CloudStorage/SynologyDrive-Sync/Music"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse command line arguments
DRY_RUN=false
DELETE_EXTRA=false

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --delete)
            DELETE_EXTRA=true
            shift
            ;;
        --help|-h)
            echo "Music Sync Script"
            echo "Usage: $0 [--dry-run] [--delete]"
            echo ""
            echo "Options:"
            echo "  --dry-run    Show what would be copied without actually copying"
            echo "  --delete     Delete files in destination that don't exist in source"
            echo "  --help       Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $arg"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    print_error "Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# Create destination directory if it doesn't exist
if [ ! -d "$DEST_DIR" ]; then
    print_warning "Destination directory does not exist. Creating: $DEST_DIR"
    mkdir -p "$DEST_DIR"
fi

# Display sync information
echo "🎵 Music Sync Script"
echo "===================="
print_status "Source: $SOURCE_DIR"
print_status "Destination: $DEST_DIR"

if [ "$DRY_RUN" = true ]; then
    print_warning "DRY RUN MODE - No files will be copied"
fi

if [ "$DELETE_EXTRA" = true ]; then
    print_warning "DELETE MODE - Extra files in destination will be removed"
fi

echo ""

# Check available space
SOURCE_SIZE=$(du -sh "$SOURCE_DIR" | cut -f1)
print_status "Source directory size: $SOURCE_SIZE"

# Count files to be processed
TOTAL_FILES=$(find "$SOURCE_DIR" -type f | wc -l | tr -d ' ')
print_status "Total files to process: $TOTAL_FILES"

echo ""

# Confirm before proceeding (unless dry run)
if [ "$DRY_RUN" = false ]; then
    read -p "Proceed with sync? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Sync cancelled by user"
        exit 0
    fi
fi

# Build rsync command
RSYNC_CMD="rsync -avh --progress"

if [ "$DRY_RUN" = true ]; then
    RSYNC_CMD="$RSYNC_CMD --dry-run"
fi

if [ "$DELETE_EXTRA" = true ]; then
    RSYNC_CMD="$RSYNC_CMD --delete"
fi

# Add source and destination
RSYNC_CMD="$RSYNC_CMD \"$SOURCE_DIR/\" \"$DEST_DIR/\""

print_status "Running: $RSYNC_CMD"
echo ""

# Execute the sync
eval $RSYNC_CMD

# Check exit status
if [ $? -eq 0 ]; then
    if [ "$DRY_RUN" = true ]; then
        print_success "Dry run completed successfully"
    else
        print_success "Music sync completed successfully!"
        
        # Show final statistics
        DEST_SIZE=$(du -sh "$DEST_DIR" | cut -f1)
        DEST_FILES=$(find "$DEST_DIR" -type f | wc -l | tr -d ' ')
        
        echo ""
        print_status "Final destination size: $DEST_SIZE"
        print_status "Total files in destination: $DEST_FILES"
    fi
else
    print_error "Sync failed with exit code $?"
    exit 1
fi 