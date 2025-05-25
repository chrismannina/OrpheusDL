# Interactive Album Selector for OrpheusDL

This script provides an interactive way to search for artists, browse their albums, and build a collection of album URLs that can be used with OrpheusDL.

## Features

- 🔍 **Search for Artists**: Search across different music services (Qobuz, Tidal, etc.)
- 📀 **Browse Albums**: View all albums by an artist with detailed information
- ✅ **Selective Downloads**: Choose specific albums or select all
- 💾 **Save to File**: Export your selections as URLs for use with the batch downloader
- 📋 **Manage Collection**: View, edit, and remove albums from your selection
- 🔄 **Continuous Operation**: Keep searching and adding until you're done

## Usage

### Quick Start

1. **Run the script**:
   ```bash
   python3 interactive_album_selector.py
   # or
   ./interactive_album_selector.py
   ```

2. **Follow the interactive menu**:
   - Choose "Search for artists and select albums"
   - Select your music service module (e.g., Qobuz)
   - Search for artists by name
   - Browse their albums and select the ones you want
   - Save your selections to a file

### Menu Options

1. **Search for artists and select albums**
   - Select which music service to use
   - Search for artists by name
   - Browse all albums by the selected artist
   - Choose specific albums or select all

2. **View selected albums**
   - See your current selection
   - Remove specific albums if needed
   - Clear all selections

3. **Save album list to file**
   - Export your selections as URLs
   - Default filename: `album_links.txt`
   - Can be used with `download_links.sh`

4. **Load existing links file**
   - Import URLs from an existing file
   - Add to your current selection

### Album Selection Commands

When viewing albums for an artist, you can:
- Enter numbers: `1 3 5` (select albums 1, 3, and 5)
- `all` - select all albums
- `none` - select no albums
- `back` - return to artist search
- `quit` - exit the program

### Managing Your Collection

In the "View selected albums" menu:
- `remove 1 3 5` - remove specific albums by number
- `clear` - remove all albums
- `back` - return to main menu

## Output

The script generates URLs that are compatible with OrpheusDL. For example:
```
https://play.qobuz.com/album/0093624932154
https://play.qobuz.com/album/0093624920137
https://play.qobuz.com/album/d7rchuzba48lc
```

These URLs can be:
1. **Used directly** with `orpheus.py [URL]`
2. **Saved to a file** and used with `download_links.sh`
3. **Added to your existing** `links.txt` file

## Integration with Batch Downloader

The generated file can be used with the existing `download_links.sh` script:

1. **Save your selections** to `links.txt` (or any filename)
2. **Run the batch downloader**:
   ```bash
   ./download_links.sh
   ```

## Requirements

- OrpheusDL properly configured
- At least one music service module installed (e.g., Qobuz)
- Python 3.6+

## Tips

- **Search Tips**: Use partial artist names for broader results
- **Quality Info**: Albums show quality information when available (e.g., `[96kHz/24bit]`)
- **Explicit Content**: Albums marked with `[E]` contain explicit content
- **Duration**: Album durations are shown when available
- **Backup**: The script offers to save your work when quitting

## Troubleshooting

- **No modules found**: Make sure you have music service modules installed in the `modules/` directory
- **Search errors**: Ensure your modules are properly configured with valid credentials
- **URL generation issues**: The script will fall back to comment placeholders if URL generation fails

## Example Workflow

1. Start the script: `./interactive_album_selector.py`
2. Choose "1. Search for artists and select albums"
3. Select "qobuz" as your module
4. Search for "Miles Davis"
5. Select the artist from results
6. Choose albums: `1 3 7 12` (select specific albums)
7. Continue searching for more artists or return to main menu
8. Choose "3. Save album list to file"
9. Save as "jazz_albums.txt"
10. Use with batch downloader: modify `download_links.sh` to use your file

Enjoy building your music collection! 🎵 