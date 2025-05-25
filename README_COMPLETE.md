# 🎵 OrpheusDL Interactive Album Selector Suite

A comprehensive collection of tools for discovering, organizing, and downloading music albums with OrpheusDL. Choose between a simple CLI interface or a beautiful TUI experience.

## 📦 What's Included

### 🖥️ **Applications**
1. **`interactive_album_selector.py`** - Simple CLI version
2. **`tui_album_selector.py`** - Full TUI version with rich graphics
3. **`download_links.sh`** - Enhanced batch downloader

### 📚 **Documentation**
- **`README_INTERACTIVE.md`** - CLI version guide
- **`README_TUI.md`** - TUI version guide
- **`README_COMPLETE.md`** - This overview document

## 🎯 Quick Start

### 🚀 **For Immediate Use (CLI)**
```bash
# Simple, fast, and lightweight
./interactive_album_selector.py
```

### 🎨 **For Best Experience (TUI)**
```bash
# Beautiful interface with rich graphics
pip install "rich>=13.0.0"
./tui_album_selector.py
```

### 📥 **For Batch Downloads**
```bash
# Use generated files with the batch downloader
./download_links.sh my_albums.txt
```

## 🔄 Complete Workflow

### 1. **Discovery & Selection**
Choose your preferred interface:

**CLI Version** (Simple & Fast):
- Text-based menus
- Keyboard-driven navigation
- Minimal resource usage
- Perfect for automation

**TUI Version** (Beautiful & Intuitive):
- Rich graphics and colors
- Visual progress indicators
- Professional app-like feel
- Enhanced user experience

### 2. **Search & Browse**
Both versions offer:
- Multi-service support (Qobuz, Tidal, etc.)
- Artist search with detailed results
- Complete discography browsing
- Quality and metadata display

### 3. **Collection Management**
- Select specific albums or choose all
- View and edit your collection
- Remove unwanted items
- Save to files for later use

### 4. **Download Execution**
- Generate service-specific URLs
- Use with the enhanced batch downloader
- Monitor download progress
- Handle errors gracefully

## 📊 Version Comparison

| Feature | CLI Version | TUI Version |
|---------|-------------|-------------|
| **Setup** | No extra dependencies | Requires `rich` library |
| **Interface** | Simple text menus | Rich graphics & colors |
| **Performance** | Minimal overhead | Slightly higher resource use |
| **User Experience** | Functional | Professional & intuitive |
| **Learning Curve** | Immediate | Immediate with visual cues |
| **Automation** | Script-friendly | Interactive-focused |
| **Terminal Support** | Any terminal | Modern terminals preferred |
| **File Size** | Smaller | Larger due to rich features |

## 🛠️ Installation & Setup

### **Prerequisites**
```bash
# Ensure OrpheusDL is properly configured
# with at least one music service module installed
ls modules/  # Should show qobuz, tidal, etc.
```

### **Basic Setup (CLI Version)**
```bash
# Make executable
chmod +x interactive_album_selector.py

# Run immediately
./interactive_album_selector.py
```

### **Enhanced Setup (TUI Version)**
```bash
# Install rich library
pip install "rich>=13.0.0"

# Make executable
chmod +x tui_album_selector.py

# Launch TUI
./tui_album_selector.py
```

### **Batch Downloader Setup**
```bash
# Make executable
chmod +x download_links.sh

# Test with existing links
./download_links.sh links.txt

# Use with custom files
./download_links.sh my_collection.txt
```

## 🎯 Use Cases & Recommendations

### **Choose CLI Version When:**
- ✅ You prefer simple, fast interfaces
- ✅ Working on older or limited terminals
- ✅ Automating with scripts
- ✅ Minimal resource usage is important
- ✅ You're comfortable with text-based tools

### **Choose TUI Version When:**
- ✅ You want the best visual experience
- ✅ Working with large collections
- ✅ You prefer app-like interfaces
- ✅ Terminal supports rich graphics
- ✅ You value visual feedback and progress

### **Use Both When:**
- ✅ Different scenarios require different tools
- ✅ Multiple users with different preferences
- ✅ Testing and comparing workflows
- ✅ Learning the system capabilities

## 🔧 Advanced Features

### **Smart URL Generation**
Both versions automatically generate proper URLs:
```
https://play.qobuz.com/album/123456789
https://tidal.com/album/987654321
# Fallback comments for problematic albums
```

### **Enhanced Batch Downloader**
Improved `download_links.sh` features:
- ✅ Custom filename support: `./download_links.sh my_file.txt`
- ✅ Comment line support (lines starting with #)
- ✅ Progress indicators and success/failure tracking
- ✅ Portable paths (no hardcoded directories)
- ✅ Error handling and recovery

### **Collection Management**
- ✅ Save/load collections from files
- ✅ Merge multiple collections
- ✅ Remove duplicates automatically
- ✅ Bulk operations for efficiency

### **Error Handling**
- ✅ Network timeout recovery
- ✅ API error handling
- ✅ Invalid input validation
- ✅ Graceful degradation

## 🔗 Integration Examples

### **With Existing Workflows**
```bash
# Generate collection with TUI
./tui_album_selector.py
# Save as "jazz_collection.txt"

# Download with batch script
./download_links.sh jazz_collection.txt

# Or use individual URLs
python3 orpheus.py "https://play.qobuz.com/album/123456"
```

### **With Custom Scripts**
```python
# Read generated files in your own scripts
with open('album_links.txt', 'r') as f:
    urls = [line.strip() for line in f 
            if line.strip() and not line.startswith('#')]

for url in urls:
    # Process each URL
    download_album(url)
```

### **With Automation**
```bash
#!/bin/bash
# Automated collection building
echo "Miles Davis" | ./interactive_album_selector.py --auto
./download_links.sh auto_generated.txt
```

## 🎨 Customization

### **Terminal Optimization**
For the best TUI experience:
- Use modern terminals (iTerm2, Windows Terminal, etc.)
- Enable Unicode and color support
- Set terminal size to at least 100x30 characters
- Use monospace fonts with good Unicode coverage

### **OrpheusDL Integration**
Both versions respect your OrpheusDL configuration:
- Module settings from `config/settings.json`
- Quality preferences and download paths
- Service authentication credentials
- Custom module configurations

## 🐛 Troubleshooting

### **Common Issues**

#### **"No modules found"**
```bash
# Check module installation
ls modules/
# Install modules if missing
```

#### **"Rich library not found" (TUI only)**
```bash
# Install rich library
pip install "rich>=13.0.0"
```

#### **"Permission denied"**
```bash
# Make scripts executable
chmod +x *.py *.sh
```

#### **"Search/API errors"**
- Verify internet connection
- Check module credentials
- Ensure service availability

### **Performance Tips**
- Use specific search terms for faster results
- Save work frequently during long sessions
- Close unnecessary applications for better performance
- Use CLI version for automation and scripting

## 📈 Future Enhancements

### **Planned Features**
- 🔄 Playlist support and management
- 🎵 Track-level selection within albums
- 📊 Statistics and collection analytics
- 🔍 Advanced search filters and sorting
- 💾 Multiple export formats (JSON, CSV, etc.)
- 🌐 Web interface for remote access

### **Community Contributions**
- 🐛 Bug reports and feature requests
- 🔧 Module compatibility improvements
- 🎨 UI/UX enhancements
- 📚 Documentation improvements

## 🎵 Getting Started

### **First Time Users**
1. **Start with the TUI version** for the best experience
2. **Search for a favorite artist** to test functionality
3. **Select a few albums** to understand the workflow
4. **Save your collection** and test the batch downloader
5. **Explore advanced features** as you become comfortable

### **Power Users**
1. **Use CLI version** for automation and scripting
2. **Combine both versions** for different scenarios
3. **Customize the batch downloader** for your workflow
4. **Build large collections** efficiently
5. **Integrate with existing tools** and scripts

## 🎉 Conclusion

The OrpheusDL Interactive Album Selector Suite provides a complete solution for music discovery and collection management. Whether you prefer the simplicity of the CLI version or the beauty of the TUI version, you have powerful tools to build and manage your music library efficiently.

Choose the version that fits your style, and enjoy discovering new music! 🎶

---

**Happy music collecting!** 🎵✨ 