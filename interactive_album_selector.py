#!/usr/bin/env python3

import argparse
import os
import sys
from urllib.parse import urlparse

from orpheus.core import Orpheus
from orpheus.music_downloader import beauty_format_seconds
from utils.models import DownloadTypeEnum, SearchResult, AlbumInfo, ArtistInfo


class InteractiveAlbumSelector:
    def __init__(self):
        self.orpheus = Orpheus()
        self.selected_albums = []
        self.album_urls = []
        
        # Get available modules (excluding hidden ones)
        self.available_modules = [
            module for module in self.orpheus.module_list 
            if module in self.orpheus.module_settings and 
            hasattr(self.orpheus.module_settings[module], 'flags') and
            'hidden' not in str(self.orpheus.module_settings[module].flags)
        ]
        
        if not self.available_modules:
            self.available_modules = list(self.orpheus.module_list)
        
        print("🎵 Interactive Album Selector")
        print("=" * 50)
        print(f"Available modules: {', '.join(self.available_modules)}")
        print()

    def select_module(self):
        """Let user select which music service module to use"""
        if len(self.available_modules) == 1:
            print(f"Using module: {self.available_modules[0]}")
            return self.available_modules[0]
        
        print("Available modules:")
        for i, module in enumerate(self.available_modules, 1):
            service_name = self.orpheus.module_settings[module].service_name
            print(f"{i}. {service_name} ({module})")
        
        while True:
            try:
                choice = input("\nSelect module (number or name): ").strip().lower()
                
                # Try as number first
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(self.available_modules):
                        return self.available_modules[idx]
                
                # Try as module name
                if choice in self.available_modules:
                    return choice
                
                # Try as service name (case insensitive)
                for module in self.available_modules:
                    service_name = self.orpheus.module_settings[module].service_name.lower()
                    if choice == service_name:
                        return module
                
                print("Invalid selection. Try again.")
                
            except (ValueError, KeyboardInterrupt):
                print("\nExiting...")
                sys.exit(0)

    def search_artists(self, module_name, query):
        """Search for artists using the selected module"""
        try:
            module = self.orpheus.load_module(module_name)
            results = module.search(DownloadTypeEnum.artist, query, limit=10)
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def get_artist_albums(self, module_name, artist_id):
        """Get albums for a specific artist"""
        try:
            module = self.orpheus.load_module(module_name)
            artist_info = module.get_artist_info(artist_id, get_credited_albums=True)
            
            albums = []
            for album_id in artist_info.albums:
                try:
                    album_info = module.get_album_info(album_id)
                    # Store the album ID in the album_info object for URL generation
                    album_info.album_id = album_id
                    albums.append(album_info)
                except Exception as e:
                    print(f"Warning: Could not get info for album {album_id}: {e}")
            
            return albums
        except Exception as e:
            print(f"Error getting artist albums: {e}")
            return []

    def display_search_results(self, results):
        """Display search results for user selection"""
        if not results:
            print("No results found.")
            return None
        
        print("\nSearch Results:")
        print("-" * 40)
        for i, result in enumerate(results, 1):
            additional_info = ""
            if result.year:
                additional_info += f" ({result.year})"
            if result.additional:
                additional_info += f" {', '.join(result.additional)}"
            
            print(f"{i}. {result.name}{additional_info}")
        
        print(f"{len(results) + 1}. Search again")
        print(f"{len(results) + 2}. Back to main menu")
        
        while True:
            try:
                choice = input(f"\nSelect artist (1-{len(results) + 2}): ").strip()
                
                if choice.lower() in ['q', 'quit', 'exit']:
                    return 'quit'
                elif choice == str(len(results) + 1):
                    return 'search_again'
                elif choice == str(len(results) + 2):
                    return 'back'
                
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    return results[idx]
                else:
                    print("Invalid selection.")
                    
            except ValueError:
                print("Please enter a valid number.")

    def display_albums(self, albums, artist_name):
        """Display albums for user selection"""
        if not albums:
            print(f"No albums found for {artist_name}.")
            return []
        
        print(f"\nAlbums by {artist_name}:")
        print("-" * 50)
        
        for i, album in enumerate(albums, 1):
            duration_str = f" [{beauty_format_seconds(album.duration)}]" if album.duration else ""
            explicit_str = " [E]" if album.explicit else ""
            quality_str = f" [{album.quality}]" if album.quality else ""
            
            print(f"{i}. {album.name} ({album.release_year}){explicit_str}{duration_str}{quality_str}")
        
        print("\nCommands:")
        print("- Enter album numbers separated by spaces (e.g., '1 3 5')")
        print("- 'all' to select all albums")
        print("- 'none' to select no albums")
        print("- 'back' to go back")
        print("- 'quit' to exit")
        
        while True:
            try:
                choice = input(f"\nSelect albums: ").strip().lower()
                
                if choice in ['q', 'quit', 'exit']:
                    return 'quit'
                elif choice == 'back':
                    return 'back'
                elif choice == 'all':
                    return albums
                elif choice == 'none':
                    return []
                
                # Parse individual album selections
                selected_albums = []
                try:
                    selections = choice.split()
                    for selection in selections:
                        idx = int(selection) - 1
                        if 0 <= idx < len(albums):
                            selected_albums.append(albums[idx])
                        else:
                            print(f"Invalid album number: {selection}")
                            break
                    else:
                        return selected_albums
                        
                except ValueError:
                    print("Please enter valid album numbers separated by spaces.")
                    
            except KeyboardInterrupt:
                return 'quit'

    def generate_album_url(self, module_name, album_info):
        """Generate URL for an album based on the module's URL constants"""
        try:
            module_settings = self.orpheus.module_settings[module_name]
            url_constants = module_settings.url_constants
            
            # Get the netlocation for this module
            netloc_constant = module_settings.netlocation_constant
            if isinstance(netloc_constant, list):
                netloc_constant = netloc_constant[0]
            
            # Common domain mappings for major services
            domain_mapping = {
                'qobuz': 'play.qobuz.com',
                'tidal': 'tidal.com',
                'spotify': 'open.spotify.com',
                'deezer': 'deezer.com',
                'apple': 'music.apple.com'
            }
            
            domain = domain_mapping.get(netloc_constant, f"{netloc_constant}.com")
            
            # Find album path from url_constants
            album_path = 'album'
            if url_constants:
                for path, download_type in url_constants.items():
                    if download_type == DownloadTypeEnum.album:
                        album_path = path
                        break
            
            # Get the album ID - try multiple approaches
            album_id = None
            
            # First try the album_id we stored
            if hasattr(album_info, 'album_id') and album_info.album_id:
                album_id = album_info.album_id
            # Try common attribute names
            elif hasattr(album_info, 'id'):
                album_id = album_info.id
            elif hasattr(album_info, '__dict__'):
                # Look for any attribute that might be an ID
                for attr_name in ['album_id', 'id', 'albumId', 'albumID']:
                    if attr_name in album_info.__dict__ and album_info.__dict__[attr_name]:
                        album_id = album_info.__dict__[attr_name]
                        break
            
            # Fallback to a hash of the album name if no ID found
            if not album_id:
                album_id = str(abs(hash(f"{album_info.name}_{album_info.artist}_{album_info.release_year}")))[:10]
            
            url = f"https://{domain}/{album_path}/{album_id}"
            return url
            
        except Exception as e:
            print(f"Warning: Could not generate URL for {album_info.name}: {e}")
            # Fallback: create a placeholder comment
            safe_name = "".join(c for c in album_info.name if c.isalnum() or c in (' ', '-', '_')).strip()
            return f"# {safe_name} ({album_info.release_year}) - {album_info.artist}"

    def add_selected_albums(self, module_name, albums, artist_name):
        """Add selected albums to the collection"""
        if not albums:
            return
        
        print(f"\nAdding {len(albums)} album(s) from {artist_name}:")
        
        for album in albums:
            self.selected_albums.append({
                'artist': artist_name,
                'album': album.name,
                'year': album.release_year,
                'module': module_name,
                'album_info': album
            })
            
            # Generate URL for the album
            url = self.generate_album_url(module_name, album)
            self.album_urls.append(url)
            
            duration_str = f" [{beauty_format_seconds(album.duration)}]" if album.duration else ""
            print(f"  ✓ {album.name} ({album.release_year}){duration_str}")
        
        print(f"\nTotal albums selected: {len(self.selected_albums)}")

    def show_selected_albums(self):
        """Display currently selected albums"""
        if not self.selected_albums:
            print("No albums selected yet.")
            return
        
        print(f"\nSelected Albums ({len(self.selected_albums)}):")
        print("=" * 60)
        
        for i, album in enumerate(self.selected_albums, 1):
            print(f"{i}. {album['artist']} - {album['album']} ({album['year']}) [{album['module']}]")
        
        print("\nCommands:")
        print("- 'remove [numbers]' to remove specific albums (e.g., 'remove 1 3 5')")
        print("- 'clear' to remove all albums")
        print("- 'back' to return to main menu")
        
        while True:
            choice = input("\nCommand: ").strip().lower()
            
            if choice == 'back':
                break
            elif choice == 'clear':
                self.selected_albums.clear()
                self.album_urls.clear()
                print("All albums removed.")
                break
            elif choice.startswith('remove '):
                try:
                    numbers = choice.split()[1:]
                    indices_to_remove = []
                    
                    for num in numbers:
                        idx = int(num) - 1
                        if 0 <= idx < len(self.selected_albums):
                            indices_to_remove.append(idx)
                        else:
                            print(f"Invalid album number: {num}")
                    
                    # Remove in reverse order to maintain indices
                    for idx in sorted(indices_to_remove, reverse=True):
                        removed = self.selected_albums.pop(idx)
                        self.album_urls.pop(idx)
                        print(f"  Removed: {removed['artist']} - {removed['album']}")
                    
                    print(f"Remaining albums: {len(self.selected_albums)}")
                    break
                    
                except (ValueError, IndexError):
                    print("Invalid format. Use 'remove [numbers]' (e.g., 'remove 1 3 5')")
            else:
                print("Invalid command.")

    def save_to_file(self, filename):
        """Save selected album URLs to a file"""
        if not self.album_urls:
            print("No albums to save.")
            return
        
        try:
            with open(filename, 'w') as f:
                for url in self.album_urls:
                    f.write(f"{url}\n")
            
            print(f"✓ Saved {len(self.album_urls)} album URLs to {filename}")
            
        except Exception as e:
            print(f"Error saving to file: {e}")

    def main_menu(self):
        """Display and handle main menu"""
        while True:
            print("\n" + "="*50)
            print("🎵 Interactive Album Selector - Main Menu")
            print("="*50)
            print("1. Search for artists and select albums")
            print("2. View selected albums")
            print("3. Save album list to file")
            print("4. Load existing links file")
            print("5. Quit")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            try:
                if choice == '1':
                    self.search_workflow()
                elif choice == '2':
                    self.show_selected_albums()
                elif choice == '3':
                    self.save_workflow()
                elif choice == '4':
                    self.load_existing_file()
                elif choice == '5' or choice.lower() in ['q', 'quit', 'exit']:
                    self.quit_application()
                else:
                    print("Invalid choice. Please enter 1-5.")
                    
            except KeyboardInterrupt:
                self.quit_application()

    def search_workflow(self):
        """Handle the search and selection workflow"""
        # Select module
        module_name = self.select_module()
        print(f"\nUsing {self.orpheus.module_settings[module_name].service_name}")
        
        while True:
            # Get search query
            print("\n" + "-"*40)
            query = input("Enter artist name to search (or 'back' to return): ").strip()
            
            if query.lower() in ['back', 'b']:
                break
            elif query.lower() in ['quit', 'q', 'exit']:
                self.quit_application()
            
            if not query:
                continue
            
            print(f"Searching for '{query}'...")
            
            # Search for artists
            results = self.search_artists(module_name, query)
            
            # Display results and get selection
            selected = self.display_search_results(results)
            
            if selected == 'quit':
                self.quit_application()
            elif selected == 'back':
                break
            elif selected == 'search_again':
                continue
            elif isinstance(selected, SearchResult):
                # Get albums for selected artist
                print(f"\nGetting albums for {selected.name}...")
                albums = self.get_artist_albums(module_name, selected.result_id)
                
                if albums:
                    selected_albums = self.display_albums(albums, selected.name)
                    
                    if selected_albums == 'quit':
                        self.quit_application()
                    elif selected_albums == 'back':
                        continue
                    elif isinstance(selected_albums, list):
                        self.add_selected_albums(module_name, selected_albums, selected.name)
                else:
                    print(f"No albums found for {selected.name}")
                    input("Press Enter to continue...")

    def save_workflow(self):
        """Handle saving albums to file"""
        if not self.album_urls:
            print("No albums selected to save.")
            input("Press Enter to continue...")
            return
        
        print(f"\nYou have {len(self.album_urls)} album(s) ready to save.")
        
        # Suggest filename
        default_filename = "album_links.txt"
        filename = input(f"Enter filename (default: {default_filename}): ").strip()
        
        if not filename:
            filename = default_filename
        
        # Ensure .txt extension
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Check if file exists
        if os.path.exists(filename):
            overwrite = input(f"File {filename} exists. Overwrite? (y/N): ").strip().lower()
            if overwrite not in ['y', 'yes']:
                print("Save cancelled.")
                return
        
        self.save_to_file(filename)
        input("Press Enter to continue...")

    def load_existing_file(self):
        """Load an existing links file to add to current selection"""
        filename = input("Enter filename to load: ").strip()
        
        if not filename:
            return
        
        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            input("Press Enter to continue...")
            return
        
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            loaded_count = 0
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and line.startswith('http'):
                    if line not in self.album_urls:
                        self.album_urls.append(line)
                        # Try to parse info from URL
                        try:
                            parsed = urlparse(line)
                            self.selected_albums.append({
                                'artist': 'Unknown',
                                'album': 'Unknown',
                                'year': 'Unknown',
                                'module': 'Unknown',
                                'url': line
                            })
                            loaded_count += 1
                        except:
                            pass
            
            print(f"✓ Loaded {loaded_count} new album URLs from {filename}")
            print(f"Total albums now: {len(self.album_urls)}")
            
        except Exception as e:
            print(f"Error loading file: {e}")
        
        input("Press Enter to continue...")

    def quit_application(self):
        """Handle application exit"""
        if self.selected_albums:
            print(f"\nYou have {len(self.selected_albums)} album(s) selected.")
            save = input("Save before quitting? (Y/n): ").strip().lower()
            
            if save not in ['n', 'no']:
                filename = input("Enter filename (default: album_links.txt): ").strip()
                if not filename:
                    filename = "album_links.txt"
                if not filename.endswith('.txt'):
                    filename += '.txt'
                
                self.save_to_file(filename)
        
        print("\nGoodbye! 🎵")
        sys.exit(0)


def main():
    print("Initializing Orpheus...")
    
    try:
        selector = InteractiveAlbumSelector()
        selector.main_menu()
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye! 🎵")
        sys.exit(0)
    except Exception as e:
        print(f"\nError initializing: {e}")
        print("Make sure you have modules installed and configured.")
        sys.exit(1)


if __name__ == "__main__":
    main() 