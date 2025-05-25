#!/usr/bin/env python3

import os
import sys
import time
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.tree import Tree
from rich.rule import Rule
from rich.status import Status
from rich import box
from rich.markup import escape

from orpheus.core import Orpheus
from orpheus.music_downloader import beauty_format_seconds
from utils.models import DownloadTypeEnum, SearchResult, AlbumInfo, ArtistInfo


class TUIAlbumSelector:
    def __init__(self):
        self.console = Console()
        self.orpheus = None
        self.selected_albums = []
        self.album_urls = []
        self.available_modules = []
        self.current_module = None
        
        # Initialize Orpheus with loading animation
        self._initialize_orpheus()

    def _initialize_orpheus(self):
        """Initialize Orpheus with a loading animation"""
        with Status("🎵 Initializing OrpheusDL...", console=self.console, spinner="dots"):
            try:
                self.orpheus = Orpheus()
                
                # Get available modules (excluding hidden ones)
                self.available_modules = [
                    module for module in self.orpheus.module_list 
                    if module in self.orpheus.module_settings and 
                    hasattr(self.orpheus.module_settings[module], 'flags') and
                    'hidden' not in str(self.orpheus.module_settings[module].flags)
                ]
                
                if not self.available_modules:
                    self.available_modules = list(self.orpheus.module_list)
                
                time.sleep(0.5)  # Brief pause for visual effect
                
            except Exception as e:
                self.console.print(f"[red]Error initializing OrpheusDL: {e}[/red]")
                self.console.print("[yellow]Make sure you have modules installed and configured.[/yellow]")
                sys.exit(1)

    def show_header(self):
        """Display the application header"""
        header_text = Text()
        header_text.append("🎵 ", style="bold magenta")
        header_text.append("OrpheusDL ", style="bold cyan")
        header_text.append("Interactive Album Selector", style="bold white")
        
        header_panel = Panel(
            Align.center(header_text),
            box=box.DOUBLE,
            style="cyan",
            padding=(1, 2)
        )
        
        return header_panel

    def show_status_bar(self):
        """Display current status information"""
        status_items = []
        
        # Module status
        if self.current_module:
            module_name = self.orpheus.module_settings[self.current_module].service_name
            status_items.append(f"[green]Module:[/green] {module_name}")
        else:
            status_items.append("[yellow]Module:[/yellow] None selected")
        
        # Albums count
        status_items.append(f"[blue]Selected Albums:[/blue] {len(self.selected_albums)}")
        
        # Available modules
        status_items.append(f"[magenta]Available Modules:[/magenta] {len(self.available_modules)}")
        
        status_text = " | ".join(status_items)
        return Panel(status_text, box=box.ROUNDED, style="dim")

    def show_main_menu(self):
        """Display the main menu and handle selection"""
        while True:
            self.console.clear()
            
            # Create layout
            layout = Layout()
            layout.split_column(
                Layout(self.show_header(), size=5),
                Layout(self._create_main_menu_content(), name="main"),
                Layout(self.show_status_bar(), size=3)
            )
            
            self.console.print(layout)
            
            choice = Prompt.ask(
                "\n[bold cyan]Select an option[/bold cyan]",
                choices=["1", "2", "3", "4", "5", "q"],
                default="1"
            )
            
            if choice == "1":
                self.search_workflow()
            elif choice == "2":
                self.show_selected_albums()
            elif choice == "3":
                self.save_workflow()
            elif choice == "4":
                self.load_existing_file()
            elif choice == "5" or choice.lower() == "q":
                self.quit_application()

    def _create_main_menu_content(self):
        """Create the main menu content panel"""
        menu_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        menu_table.add_column("Option", style="bold cyan", width=8)
        menu_table.add_column("Description", style="white")
        menu_table.add_column("Status", style="dim", width=20)
        
        # Menu options with status indicators
        options = [
            ("1", "🔍 Search & Select Albums", f"{len(self.available_modules)} modules available"),
            ("2", "📋 View Selected Albums", f"{len(self.selected_albums)} albums selected"),
            ("3", "💾 Save Album List", "Export to file"),
            ("4", "📂 Load Existing File", "Import from file"),
            ("5", "🚪 Quit Application", "Exit program")
        ]
        
        for option, desc, status in options:
            menu_table.add_row(f"[{option}]", desc, status)
        
        return Panel(
            menu_table,
            title="[bold white]Main Menu[/bold white]",
            box=box.ROUNDED,
            padding=(1, 2)
        )

    def select_module(self) -> Optional[str]:
        """Let user select which music service module to use"""
        if len(self.available_modules) == 1:
            self.current_module = self.available_modules[0]
            service_name = self.orpheus.module_settings[self.current_module].service_name
            self.console.print(f"[green]Using module:[/green] {service_name}")
            return self.current_module
        
        self.console.clear()
        self.console.print(self.show_header())
        self.console.print()
        
        # Create module selection table
        module_table = Table(box=box.ROUNDED, title="[bold cyan]Available Music Services[/bold cyan]")
        module_table.add_column("Option", style="bold cyan", width=8)
        module_table.add_column("Service", style="bold white")
        module_table.add_column("Module", style="dim")
        module_table.add_column("Status", style="green")
        
        for i, module in enumerate(self.available_modules, 1):
            service_name = self.orpheus.module_settings[module].service_name
            module_table.add_row(
                f"[{i}]",
                service_name,
                module,
                "✓ Available"
            )
        
        self.console.print(module_table)
        self.console.print()
        
        while True:
            choice = Prompt.ask(
                "[bold cyan]Select music service[/bold cyan]",
                choices=[str(i) for i in range(1, len(self.available_modules) + 1)] + ["q"],
                default="1"
            )
            
            if choice.lower() == "q":
                return None
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.available_modules):
                    self.current_module = self.available_modules[idx]
                    return self.current_module
            except ValueError:
                self.console.print("[red]Invalid selection. Please try again.[/red]")

    def search_artists(self, module_name: str, query: str) -> List[SearchResult]:
        """Search for artists with progress indication"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task(f"Searching for '{query}'...", total=None)
            
            try:
                module = self.orpheus.load_module(module_name)
                results = module.search(DownloadTypeEnum.artist, query, limit=10)
                progress.update(task, completed=True)
                return results
            except Exception as e:
                progress.update(task, completed=True)
                self.console.print(f"[red]Search error: {e}[/red]")
                return []

    def get_artist_albums(self, module_name: str, artist_id: str) -> List[AlbumInfo]:
        """Get albums for an artist with progress indication"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
            transient=True
        ) as progress:
            
            try:
                module = self.orpheus.load_module(module_name)
                artist_info = module.get_artist_info(artist_id, get_credited_albums=True)
                
                total_albums = len(artist_info.albums)
                task = progress.add_task("Loading albums...", total=total_albums)
                
                albums = []
                for i, album_id in enumerate(artist_info.albums):
                    try:
                        album_info = module.get_album_info(album_id)
                        album_info.album_id = album_id
                        albums.append(album_info)
                        progress.update(task, advance=1)
                    except Exception as e:
                        progress.update(task, advance=1)
                        self.console.print(f"[yellow]Warning: Could not load album {album_id}: {e}[/yellow]")
                
                return albums
                
            except Exception as e:
                self.console.print(f"[red]Error getting artist albums: {e}[/red]")
                return []

    def display_search_results(self, results: List[SearchResult]) -> Optional[SearchResult]:
        """Display search results in a formatted table"""
        if not results:
            self.console.print("[yellow]No results found.[/yellow]")
            Prompt.ask("Press Enter to continue", default="")
            return None
        
        self.console.clear()
        self.console.print(self.show_header())
        self.console.print()
        
        # Create results table
        results_table = Table(box=box.ROUNDED, title="[bold cyan]Search Results[/bold cyan]")
        results_table.add_column("Option", style="bold cyan", width=8)
        results_table.add_column("Artist", style="bold white")
        results_table.add_column("Year", style="dim", width=10)
        results_table.add_column("Additional Info", style="green")
        
        for i, result in enumerate(results, 1):
            year = str(result.year) if result.year else "Unknown"
            additional = ", ".join(result.additional) if result.additional else ""
            
            results_table.add_row(
                f"[{i}]",
                escape(result.name),
                year,
                additional
            )
        
        # Add navigation options
        results_table.add_row("", "", "", "")
        results_table.add_row("[s]", "🔍 Search again", "", "")
        results_table.add_row("[b]", "⬅️  Back to main menu", "", "")
        
        self.console.print(results_table)
        self.console.print()
        
        choices = [str(i) for i in range(1, len(results) + 1)] + ["s", "b", "q"]
        choice = Prompt.ask(
            "[bold cyan]Select artist[/bold cyan]",
            choices=choices,
            default="1"
        )
        
        if choice.lower() == "q":
            self.quit_application()
        elif choice.lower() == "s":
            return "search_again"
        elif choice.lower() == "b":
            return "back"
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    return results[idx]
            except ValueError:
                pass
        
        return None

    def display_albums(self, albums: List[AlbumInfo], artist_name: str) -> List[AlbumInfo]:
        """Display albums in a formatted table with selection"""
        if not albums:
            self.console.print(f"[yellow]No albums found for {artist_name}.[/yellow]")
            Prompt.ask("Press Enter to continue", default="")
            return []
        
        self.console.clear()
        self.console.print(self.show_header())
        self.console.print()
        
        # Create albums table
        albums_table = Table(
            box=box.ROUNDED, 
            title=f"[bold cyan]Albums by {escape(artist_name)}[/bold cyan]",
            title_style="bold cyan"
        )
        albums_table.add_column("Option", style="bold cyan", width=8)
        albums_table.add_column("Album", style="bold white")
        albums_table.add_column("Year", style="dim", width=8)
        albums_table.add_column("Duration", style="blue", width=12)
        albums_table.add_column("Quality", style="green", width=15)
        albums_table.add_column("Flags", style="yellow", width=8)
        
        for i, album in enumerate(albums, 1):
            duration = beauty_format_seconds(album.duration) if album.duration else "Unknown"
            quality = album.quality if album.quality else "Standard"
            flags = "🔞" if album.explicit else ""
            
            albums_table.add_row(
                f"[{i}]",
                escape(album.name),
                str(album.release_year),
                duration,
                quality,
                flags
            )
        
        self.console.print(albums_table)
        self.console.print()
        
        # Show selection instructions
        instructions = Panel(
            "[bold white]Selection Commands:[/bold white]\n"
            "• Enter numbers separated by spaces (e.g., '1 3 5')\n"
            "• Type 'all' to select all albums\n"
            "• Type 'none' to select no albums\n"
            "• Type 'back' to return to search\n"
            "• Type 'quit' to exit",
            title="[bold cyan]Instructions[/bold cyan]",
            box=box.ROUNDED
        )
        self.console.print(instructions)
        
        while True:
            choice = Prompt.ask("[bold cyan]Select albums[/bold cyan]").strip().lower()
            
            if choice in ['q', 'quit']:
                self.quit_application()
            elif choice == 'back':
                return "back"
            elif choice == 'all':
                return albums
            elif choice == 'none':
                return []
            else:
                # Parse individual selections
                try:
                    selected_albums = []
                    selections = choice.split()
                    
                    for selection in selections:
                        idx = int(selection) - 1
                        if 0 <= idx < len(albums):
                            selected_albums.append(albums[idx])
                        else:
                            self.console.print(f"[red]Invalid album number: {selection}[/red]")
                            break
                    else:
                        return selected_albums
                        
                except ValueError:
                    self.console.print("[red]Please enter valid album numbers separated by spaces.[/red]")

    def generate_album_url(self, module_name: str, album_info: AlbumInfo) -> str:
        """Generate URL for an album"""
        try:
            module_settings = self.orpheus.module_settings[module_name]
            url_constants = module_settings.url_constants
            
            netloc_constant = module_settings.netlocation_constant
            if isinstance(netloc_constant, list):
                netloc_constant = netloc_constant[0]
            
            domain_mapping = {
                'qobuz': 'play.qobuz.com',
                'tidal': 'tidal.com',
                'spotify': 'open.spotify.com',
                'deezer': 'deezer.com',
                'apple': 'music.apple.com'
            }
            
            domain = domain_mapping.get(netloc_constant, f"{netloc_constant}.com")
            
            album_path = 'album'
            if url_constants:
                for path, download_type in url_constants.items():
                    if download_type == DownloadTypeEnum.album:
                        album_path = path
                        break
            
            # Get album ID
            album_id = None
            if hasattr(album_info, 'album_id') and album_info.album_id:
                album_id = album_info.album_id
            elif hasattr(album_info, 'id'):
                album_id = album_info.id
            
            if not album_id:
                album_id = str(abs(hash(f"{album_info.name}_{album_info.artist}_{album_info.release_year}")))[:10]
            
            return f"https://{domain}/{album_path}/{album_id}"
            
        except Exception as e:
            safe_name = "".join(c for c in album_info.name if c.isalnum() or c in (' ', '-', '_')).strip()
            return f"# {safe_name} ({album_info.release_year}) - {album_info.artist}"

    def add_selected_albums(self, module_name: str, albums: List[AlbumInfo], artist_name: str):
        """Add selected albums with progress indication"""
        if not albums:
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
            transient=True
        ) as progress:
            
            task = progress.add_task(f"Adding {len(albums)} albums...", total=len(albums))
            
            for album in albums:
                self.selected_albums.append({
                    'artist': artist_name,
                    'album': album.name,
                    'year': album.release_year,
                    'module': module_name,
                    'album_info': album
                })
                
                url = self.generate_album_url(module_name, album)
                self.album_urls.append(url)
                progress.update(task, advance=1)
        
        self.console.print(f"[green]✓ Added {len(albums)} albums from {artist_name}[/green]")
        self.console.print(f"[blue]Total albums selected: {len(self.selected_albums)}[/blue]")
        Prompt.ask("Press Enter to continue", default="")

    def show_selected_albums(self):
        """Display selected albums in a formatted view"""
        self.console.clear()
        self.console.print(self.show_header())
        self.console.print()
        
        if not self.selected_albums:
            no_albums_panel = Panel(
                "[yellow]No albums selected yet.[/yellow]\n\n"
                "Use option 1 from the main menu to search and select albums.",
                title="[bold cyan]Selected Albums[/bold cyan]",
                box=box.ROUNDED
            )
            self.console.print(no_albums_panel)
            Prompt.ask("Press Enter to continue", default="")
            return
        
        # Create selected albums table
        selected_table = Table(
            box=box.ROUNDED,
            title=f"[bold cyan]Selected Albums ({len(self.selected_albums)})[/bold cyan]"
        )
        selected_table.add_column("No.", style="bold cyan", width=6)
        selected_table.add_column("Artist", style="bold white")
        selected_table.add_column("Album", style="white")
        selected_table.add_column("Year", style="dim", width=8)
        selected_table.add_column("Module", style="green", width=12)
        
        for i, album in enumerate(self.selected_albums, 1):
            selected_table.add_row(
                str(i),
                escape(album['artist']),
                escape(album['album']),
                str(album['year']),
                album['module']
            )
        
        self.console.print(selected_table)
        self.console.print()
        
        # Management options
        management_panel = Panel(
            "[bold white]Management Commands:[/bold white]\n"
            "• 'remove [numbers]' - Remove specific albums (e.g., 'remove 1 3 5')\n"
            "• 'clear' - Remove all albums\n"
            "• 'back' - Return to main menu",
            title="[bold cyan]Album Management[/bold cyan]",
            box=box.ROUNDED
        )
        self.console.print(management_panel)
        
        while True:
            choice = Prompt.ask("[bold cyan]Command[/bold cyan]", default="back").strip().lower()
            
            if choice == 'back':
                break
            elif choice == 'clear':
                if Confirm.ask("[red]Remove all selected albums?[/red]"):
                    self.selected_albums.clear()
                    self.album_urls.clear()
                    self.console.print("[green]✓ All albums removed.[/green]")
                    break
            elif choice.startswith('remove '):
                self._remove_albums(choice)
                break
            else:
                self.console.print("[red]Invalid command.[/red]")

    def _remove_albums(self, command: str):
        """Remove specific albums by numbers"""
        try:
            numbers = command.split()[1:]
            indices_to_remove = []
            
            for num in numbers:
                idx = int(num) - 1
                if 0 <= idx < len(self.selected_albums):
                    indices_to_remove.append(idx)
                else:
                    self.console.print(f"[red]Invalid album number: {num}[/red]")
                    return
            
            # Remove in reverse order
            removed_count = 0
            for idx in sorted(indices_to_remove, reverse=True):
                removed = self.selected_albums.pop(idx)
                self.album_urls.pop(idx)
                removed_count += 1
            
            self.console.print(f"[green]✓ Removed {removed_count} albums.[/green]")
            self.console.print(f"[blue]Remaining albums: {len(self.selected_albums)}[/blue]")
            
        except (ValueError, IndexError):
            self.console.print("[red]Invalid format. Use 'remove [numbers]' (e.g., 'remove 1 3 5')[/red]")

    def search_workflow(self):
        """Handle the complete search workflow"""
        # Select module
        module_name = self.select_module()
        if not module_name:
            return
        
        service_name = self.orpheus.module_settings[module_name].service_name
        
        while True:
            self.console.clear()
            self.console.print(self.show_header())
            self.console.print(f"\n[green]Using service:[/green] {service_name}")
            self.console.print()
            
            query = Prompt.ask(
                "[bold cyan]Enter artist name to search[/bold cyan] (or 'back' to return)",
                default=""
            ).strip()
            
            if query.lower() in ['back', 'b', '']:
                break
            elif query.lower() in ['quit', 'q']:
                self.quit_application()
            
            # Search for artists
            results = self.search_artists(module_name, query)
            
            # Display results and get selection
            selected = self.display_search_results(results)
            
            if selected == "back":
                break
            elif selected == "search_again":
                continue
            elif isinstance(selected, SearchResult):
                # Get albums for selected artist
                with Status(f"Loading albums for {selected.name}...", console=self.console):
                    albums = self.get_artist_albums(module_name, selected.result_id)
                
                if albums:
                    selected_albums = self.display_albums(albums, selected.name)
                    
                    if selected_albums == "back":
                        continue
                    elif isinstance(selected_albums, list) and selected_albums:
                        self.add_selected_albums(module_name, selected_albums, selected.name)

    def save_workflow(self):
        """Handle saving albums to file"""
        if not self.album_urls:
            self.console.print("[yellow]No albums selected to save.[/yellow]")
            Prompt.ask("Press Enter to continue", default="")
            return
        
        self.console.clear()
        self.console.print(self.show_header())
        self.console.print()
        
        save_panel = Panel(
            f"[bold white]Ready to save {len(self.album_urls)} album URLs[/bold white]\n\n"
            "These URLs can be used with:\n"
            "• The batch downloader script\n"
            "• Direct orpheus.py commands\n"
            "• Manual organization and editing",
            title="[bold cyan]Save Album Collection[/bold cyan]",
            box=box.ROUNDED
        )
        self.console.print(save_panel)
        
        filename = Prompt.ask(
            "[bold cyan]Enter filename[/bold cyan]",
            default="album_links.txt"
        ).strip()
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Check if file exists
        if os.path.exists(filename):
            if not Confirm.ask(f"[yellow]File {filename} exists. Overwrite?[/yellow]"):
                self.console.print("[yellow]Save cancelled.[/yellow]")
                Prompt.ask("Press Enter to continue", default="")
                return
        
        # Save with progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task("Saving file...", total=None)
            
            try:
                with open(filename, 'w') as f:
                    for url in self.album_urls:
                        f.write(f"{url}\n")
                
                progress.update(task, completed=True)
                self.console.print(f"[green]✓ Saved {len(self.album_urls)} album URLs to {filename}[/green]")
                
            except Exception as e:
                progress.update(task, completed=True)
                self.console.print(f"[red]Error saving file: {e}[/red]")
        
        Prompt.ask("Press Enter to continue", default="")

    def load_existing_file(self):
        """Load an existing links file"""
        self.console.clear()
        self.console.print(self.show_header())
        self.console.print()
        
        filename = Prompt.ask(
            "[bold cyan]Enter filename to load[/bold cyan]",
            default=""
        ).strip()
        
        if not filename:
            return
        
        if not os.path.exists(filename):
            self.console.print(f"[red]File {filename} not found.[/red]")
            Prompt.ask("Press Enter to continue", default="")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task("Loading file...", total=None)
            
            try:
                with open(filename, 'r') as f:
                    lines = f.readlines()
                
                loaded_count = 0
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and line.startswith('http'):
                        if line not in self.album_urls:
                            self.album_urls.append(line)
                            self.selected_albums.append({
                                'artist': 'Unknown',
                                'album': 'Unknown',
                                'year': 'Unknown',
                                'module': 'Unknown',
                                'url': line
                            })
                            loaded_count += 1
                
                progress.update(task, completed=True)
                self.console.print(f"[green]✓ Loaded {loaded_count} new album URLs from {filename}[/green]")
                self.console.print(f"[blue]Total albums now: {len(self.album_urls)}[/blue]")
                
            except Exception as e:
                progress.update(task, completed=True)
                self.console.print(f"[red]Error loading file: {e}[/red]")
        
        Prompt.ask("Press Enter to continue", default="")

    def quit_application(self):
        """Handle application exit with save prompt"""
        if self.selected_albums:
            self.console.print(f"\n[yellow]You have {len(self.selected_albums)} album(s) selected.[/yellow]")
            
            if Confirm.ask("[bold cyan]Save before quitting?[/bold cyan]", default=True):
                filename = Prompt.ask(
                    "[bold cyan]Enter filename[/bold cyan]",
                    default="album_links.txt"
                )
                
                if not filename.endswith('.txt'):
                    filename += '.txt'
                
                try:
                    with open(filename, 'w') as f:
                        for url in self.album_urls:
                            f.write(f"{url}\n")
                    
                    self.console.print(f"[green]✓ Saved to {filename}[/green]")
                except Exception as e:
                    self.console.print(f"[red]Error saving: {e}[/red]")
        
        goodbye_panel = Panel(
            "[bold white]Thank you for using OrpheusDL Interactive Album Selector![/bold white]\n\n"
            "🎵 Happy listening! 🎵",
            title="[bold cyan]Goodbye[/bold cyan]",
            box=box.DOUBLE,
            style="cyan"
        )
        
        self.console.print("\n")
        self.console.print(Align.center(goodbye_panel))
        sys.exit(0)

    def run(self):
        """Main application entry point"""
        try:
            self.show_main_menu()
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Interrupted by user.[/yellow]")
            self.quit_application()
        except Exception as e:
            self.console.print(f"\n[red]Unexpected error: {e}[/red]")
            sys.exit(1)


def main():
    """Application entry point"""
    try:
        app = TUIAlbumSelector()
        app.run()
    except KeyboardInterrupt:
        print("\nGoodbye! 🎵")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 