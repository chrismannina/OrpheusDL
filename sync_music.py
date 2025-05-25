#!/usr/bin/env python3

import os
import shutil
import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.panel import Panel
    from rich.prompt import Confirm
    from rich.table import Table
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better visual output: pip install rich")

class MusicSyncer:
    def __init__(self):
        self.source_dir = Path("/Users/chrismannina/Music/downloads")
        self.dest_dir = Path("/Users/chrismannina/Library/CloudStorage/SynologyDrive-Sync/Music")
        
        if RICH_AVAILABLE:
            self.console = Console()
        
    def print_info(self, message):
        if RICH_AVAILABLE:
            self.console.print(f"[blue][INFO][/blue] {message}")
        else:
            print(f"[INFO] {message}")
    
    def print_success(self, message):
        if RICH_AVAILABLE:
            self.console.print(f"[green][SUCCESS][/green] {message}")
        else:
            print(f"[SUCCESS] {message}")
    
    def print_warning(self, message):
        if RICH_AVAILABLE:
            self.console.print(f"[yellow][WARNING][/yellow] {message}")
        else:
            print(f"[WARNING] {message}")
    
    def print_error(self, message):
        if RICH_AVAILABLE:
            self.console.print(f"[red][ERROR][/red] {message}")
        else:
            print(f"[ERROR] {message}")

    def get_directory_size(self, directory):
        """Calculate total size of directory"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass
        return total_size

    def format_size(self, size_bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def get_all_files(self, directory):
        """Get list of all files in directory recursively"""
        files = []
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files

    def copy_file_with_structure(self, src_file, src_base, dest_base, dry_run=False):
        """Copy file maintaining directory structure"""
        # Calculate relative path from source base
        rel_path = os.path.relpath(src_file, src_base)
        dest_file = os.path.join(dest_base, rel_path)
        
        # Create destination directory if needed
        dest_dir = os.path.dirname(dest_file)
        if not dry_run:
            os.makedirs(dest_dir, exist_ok=True)
        
        # Copy file if it doesn't exist or is newer
        should_copy = True
        if os.path.exists(dest_file):
            src_mtime = os.path.getmtime(src_file)
            dest_mtime = os.path.getmtime(dest_file)
            src_size = os.path.getsize(src_file)
            dest_size = os.path.getsize(dest_file)
            
            # Skip if destination is newer and same size
            if dest_mtime >= src_mtime and src_size == dest_size:
                should_copy = False
        
        if should_copy:
            if not dry_run:
                shutil.copy2(src_file, dest_file)
            return True, rel_path
        else:
            return False, rel_path

    def sync_music(self, dry_run=False, delete_extra=False):
        """Main sync function"""
        
        # Validate directories
        if not self.source_dir.exists():
            self.print_error(f"Source directory does not exist: {self.source_dir}")
            return False
        
        if not self.dest_dir.exists():
            self.print_warning(f"Creating destination directory: {self.dest_dir}")
            if not dry_run:
                self.dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Show header
        if RICH_AVAILABLE:
            header = Panel(
                f"🎵 Music Sync\n"
                f"Source: {self.source_dir}\n"
                f"Destination: {self.dest_dir}\n"
                f"Mode: {'DRY RUN' if dry_run else 'SYNC'}",
                title="Music Sync Script",
                box=box.ROUNDED
            )
            self.console.print(header)
        else:
            print("🎵 Music Sync Script")
            print("=" * 50)
            print(f"Source: {self.source_dir}")
            print(f"Destination: {self.dest_dir}")
            if dry_run:
                print("Mode: DRY RUN")
            print()
        
        # Get file lists
        self.print_info("Scanning directories...")
        source_files = self.get_all_files(self.source_dir)
        
        if not source_files:
            self.print_warning("No files found in source directory")
            return True
        
        # Calculate sizes
        source_size = self.get_directory_size(self.source_dir)
        
        # Show statistics
        if RICH_AVAILABLE:
            stats_table = Table(box=box.SIMPLE)
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="white")
            stats_table.add_row("Source files", str(len(source_files)))
            stats_table.add_row("Source size", self.format_size(source_size))
            self.console.print(stats_table)
        else:
            print(f"Source files: {len(source_files)}")
            print(f"Source size: {self.format_size(source_size)}")
        
        # Confirm if not dry run
        if not dry_run:
            if RICH_AVAILABLE:
                proceed = Confirm.ask("Proceed with sync?")
            else:
                proceed = input("Proceed with sync? (y/N): ").lower().startswith('y')
            
            if not proceed:
                self.print_warning("Sync cancelled by user")
                return False
        
        # Perform sync
        copied_files = 0
        skipped_files = 0
        
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task("Syncing files...", total=len(source_files))
                
                for src_file in source_files:
                    was_copied, rel_path = self.copy_file_with_structure(
                        src_file, self.source_dir, self.dest_dir, dry_run
                    )
                    
                    if was_copied:
                        copied_files += 1
                        progress.update(task, description=f"Copied: {rel_path}")
                    else:
                        skipped_files += 1
                        progress.update(task, description=f"Skipped: {rel_path}")
                    
                    progress.advance(task)
        else:
            for i, src_file in enumerate(source_files, 1):
                was_copied, rel_path = self.copy_file_with_structure(
                    src_file, self.source_dir, self.dest_dir, dry_run
                )
                
                if was_copied:
                    copied_files += 1
                    print(f"[{i}/{len(source_files)}] Copied: {rel_path}")
                else:
                    skipped_files += 1
                    print(f"[{i}/{len(source_files)}] Skipped: {rel_path}")
        
        # Handle deletion of extra files
        if delete_extra and not dry_run:
            self.print_info("Checking for extra files to delete...")
            dest_files = self.get_all_files(self.dest_dir)
            deleted_files = 0
            
            for dest_file in dest_files:
                rel_path = os.path.relpath(dest_file, self.dest_dir)
                src_equivalent = os.path.join(self.source_dir, rel_path)
                
                if not os.path.exists(src_equivalent):
                    if not dry_run:
                        os.remove(dest_file)
                    deleted_files += 1
                    self.print_info(f"Deleted: {rel_path}")
            
            if deleted_files > 0:
                self.print_info(f"Deleted {deleted_files} extra files")
        
        # Show results
        if RICH_AVAILABLE:
            results_table = Table(title="Sync Results", box=box.ROUNDED)
            results_table.add_column("Operation", style="cyan")
            results_table.add_column("Count", style="white")
            results_table.add_row("Files copied", str(copied_files))
            results_table.add_row("Files skipped", str(skipped_files))
            self.console.print(results_table)
        else:
            print("\nSync Results:")
            print(f"Files copied: {copied_files}")
            print(f"Files skipped: {skipped_files}")
        
        if dry_run:
            self.print_success("Dry run completed successfully")
        else:
            self.print_success("Music sync completed successfully!")
        
        return True

def main():
    parser = argparse.ArgumentParser(description="Sync music from downloads to Synology Drive")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be copied without actually copying")
    parser.add_argument("--delete", action="store_true",
                       help="Delete files in destination that don't exist in source")
    
    args = parser.parse_args()
    
    syncer = MusicSyncer()
    
    try:
        success = syncer.sync_music(dry_run=args.dry_run, delete_extra=args.delete)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        syncer.print_warning("Sync interrupted by user")
        sys.exit(1)
    except Exception as e:
        syncer.print_error(f"Sync failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 