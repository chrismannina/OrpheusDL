# 🎵 OrpheusDL TUI Album Selector

A beautiful, full-featured Terminal User Interface (TUI) for searching, browsing, and collecting music albums for download with OrpheusDL.

## ✨ Features

### 🎨 **Professional TUI Interface**
- **Rich Terminal Graphics**: Beautiful panels, tables, and progress bars
- **Responsive Layout**: Adapts to your terminal size
- **Color-Coded Interface**: Intuitive color scheme for easy navigation
- **Real-time Status**: Live status bar showing current module and selection count
- **Loading Animations**: Smooth spinners and progress indicators

### 🔍 **Advanced Search & Browse**
- **Multi-Service Support**: Search across Qobuz, Tidal, Spotify, and more
- **Artist Discovery**: Find artists with detailed search results
- **Album Browsing**: View complete discographies with rich metadata
- **Quality Information**: See audio quality, duration, and format details
- **Smart Filtering**: Automatic handling of explicit content flags

### 📋 **Collection Management**
- **Interactive Selection**: Choose specific albums or select all
- **Visual Collection**: Beautiful table view of selected albums
- **Bulk Operations**: Add, remove, or clear multiple albums at once
- **Persistent Storage**: Save and load collections from files
- **URL Generation**: Automatic creation of service-specific URLs

### 🚀 **Workflow Integration**
- **Batch Download Ready**: Generate files for use with download scripts
- **Multiple Formats**: Export to various file formats
- **Error Handling**: Graceful handling of network and API issues
- **Session Management**: Save work automatically on exit

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Ensure you have OrpheusDL properly configured
# with at least one music service module installed
```

### Install Dependencies
```bash
# Install the rich library for TUI functionality
pip install "rich>=13.0.0"

# Or install from requirements.txt
pip install -r requirements.txt
```

### Make Executable
```bash
chmod +x tui_album_selector.py
```

## 🎯 Quick Start

### Launch the Application
```bash
# Run the TUI application
./tui_album_selector.py

# Or with Python directly
python3 tui_album_selector.py
```

### Basic Workflow
1. **Select Music Service** - Choose from available modules (Qobuz, Tidal, etc.)
2. **Search Artists** - Enter artist names to find matches
3. **Browse Albums** - View complete discographies with details
4. **Select Albums** - Choose specific albums or select all
5. **Manage Collection** - Review, edit, and organize your selections
6. **Save & Export** - Generate download-ready files

## 📖 User Guide

### 🏠 **Main Menu**
The main menu provides access to all application features:

- **🔍 Search & Select Albums** - Start the search workflow
- **📋 View Selected Albums** - Manage your current collection
- **💾 Save Album List** - Export your selections to files
- **📂 Load Existing File** - Import previously saved collections
- **🚪 Quit Application** - Exit with optional save prompt

### 🔍 **Search Workflow**

#### 1. **Module Selection**
- Choose your preferred music service
- See available modules with status indicators
- Automatic selection if only one module is available

#### 2. **Artist Search**
- Enter full or partial artist names
- View search results in a formatted table
- See additional information like years and quality indicators

#### 3. **Album Browsing**
- Browse complete artist discographies
- View detailed album information:
  - **Album Name** with version information
  - **Release Year** for chronological context
  - **Duration** in human-readable format
  - **Quality** information (sample rate, bit depth)
  - **Flags** for explicit content (🔞)

#### 4. **Album Selection**
Multiple selection methods available:
```
1 3 5        # Select specific albums by number
all          # Select all albums
none         # Select no albums
back         # Return to search
quit         # Exit application
```

### 📋 **Collection Management**

#### **View Selected Albums**
- See all selected albums in a formatted table
- Information includes artist, album, year, and source module
- Real-time count of selected items

#### **Remove Albums**
```bash
remove 1 3 5    # Remove specific albums by number
clear           # Remove all albums
back            # Return to main menu
```

#### **Bulk Operations**
- Select multiple albums at once
- Remove multiple albums simultaneously
- Clear entire collection with confirmation

### 💾 **File Operations**

#### **Save Collections**
- Export to `.txt` files for use with download scripts
- Automatic URL generation for each service
- Overwrite protection with confirmation prompts
- Progress indication during save operations

#### **Load Existing Files**
- Import URLs from existing files
- Merge with current selection
- Skip duplicates automatically
- Support for comment lines (starting with #)

### 🎨 **Interface Elements**

#### **Status Bar**
Real-time information display:
- **Current Module**: Active music service
- **Selected Albums**: Count of items in collection
- **Available Modules**: Total modules installed

#### **Progress Indicators**
- **Search Progress**: Animated spinner during searches
- **Album Loading**: Progress bar for large discographies
- **File Operations**: Progress indication for save/load

#### **Color Coding**
- **Cyan**: Headers and titles
- **Green**: Success messages and confirmations
- **Yellow**: Warnings and informational messages
- **Red**: Errors and critical actions
- **Blue**: Metadata and secondary information
- **Magenta**: Highlights and emphasis

## 🔧 Advanced Features

### **Smart URL Generation**
- Automatic detection of service URL patterns
- Proper album ID extraction and formatting
- Fallback to comment format for problematic albums
- Support for multiple URL schemes per service

### **Error Handling**
- Graceful handling of network timeouts
- API error recovery with user feedback
- Invalid input validation with helpful messages
- Automatic retry mechanisms where appropriate

### **Session Management**
- Automatic save prompts on exit
- Preservation of work during unexpected exits
- Resume capability for interrupted sessions
- Backup creation for important collections

### **Performance Optimization**
- Lazy loading of album information
- Efficient caching of search results
- Minimal memory footprint for large collections
- Responsive interface during heavy operations

## 🔗 Integration

### **With Batch Downloader**
```bash
# Generate collection file
./tui_album_selector.py
# (Select albums and save to 'my_collection.txt')

# Use with batch downloader
./download_links.sh my_collection.txt
```

### **With OrpheusDL Direct**
```bash
# Use generated URLs directly
python3 orpheus.py "https://play.qobuz.com/album/123456"
```

### **With Custom Scripts**
The generated files are plain text with one URL per line:
```
https://play.qobuz.com/album/123456
https://play.qobuz.com/album/789012
# Comment lines are supported
https://play.qobuz.com/album/345678
```

## 🎛️ Keyboard Shortcuts

### **Global Shortcuts**
- **Ctrl+C**: Graceful exit with save prompt
- **Enter**: Confirm selections and continue
- **Escape**: Cancel current operation (where supported)

### **Navigation**
- **Numbers**: Select menu options or items
- **Letters**: Quick commands (s=search, b=back, q=quit)
- **Space**: Separate multiple selections

## 🐛 Troubleshooting

### **Common Issues**

#### **"No modules found"**
```bash
# Ensure you have music service modules installed
ls modules/
# Should show directories like 'qobuz', 'tidal', etc.
```

#### **"Rich library not found"**
```bash
# Install the rich library
pip install "rich>=13.0.0"
```

#### **"Search errors"**
- Check your module configuration
- Verify internet connection
- Ensure valid credentials for music services

#### **"Terminal display issues"**
- Use a modern terminal with Unicode support
- Ensure terminal width is at least 80 characters
- Update your terminal application if needed

### **Performance Tips**
- Use specific artist names for faster searches
- Limit album selections for large discographies
- Save collections regularly to prevent data loss
- Close other terminal applications for better performance

## 🎨 Customization

### **Terminal Compatibility**
The TUI automatically adapts to:
- **Terminal Size**: Responsive layout for different screen sizes
- **Color Support**: Graceful degradation for limited color terminals
- **Unicode Support**: Fallback characters for limited character sets

### **Configuration**
The application respects OrpheusDL configuration:
- Module settings from `config/settings.json`
- Quality preferences and download paths
- Service-specific authentication credentials

## 📊 Comparison: TUI vs CLI

| Feature | TUI Version | CLI Version |
|---------|-------------|-------------|
| **Interface** | Rich graphics, panels, tables | Simple text output |
| **Navigation** | Menu-driven, intuitive | Command-based |
| **Progress** | Visual progress bars | Text indicators |
| **Error Handling** | Colored, contextual | Plain text |
| **User Experience** | App-like feel | Script-like feel |
| **Learning Curve** | Immediate, visual | Requires command knowledge |
| **Performance** | Slightly higher overhead | Minimal overhead |
| **Accessibility** | Better visual organization | Better for automation |

## 🚀 Tips for Best Experience

### **Terminal Setup**
- Use a terminal with good Unicode support (iTerm2, Windows Terminal, etc.)
- Set terminal to at least 100x30 characters for optimal layout
- Enable true color support if available

### **Workflow Tips**
- Start with broad artist searches, then narrow down
- Use the "View Selected Albums" feature to review before saving
- Save collections with descriptive filenames
- Use the load feature to build upon previous collections

### **Performance Tips**
- Search for specific artists rather than generic terms
- Select albums in batches rather than one by one
- Save your work frequently during long sessions
- Use the quit confirmation to avoid losing work

## 🎵 Happy Music Collecting!

The TUI Album Selector transforms the process of building music collections from a tedious task into an enjoyable, visual experience. With its intuitive interface and powerful features, you can efficiently discover, organize, and prepare music for download.

Enjoy exploring new artists and building your perfect music collection! 🎶 