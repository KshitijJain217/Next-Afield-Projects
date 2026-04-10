"""
File Organizer Automation Tool
==============================
Automatically organizes files in a directory into categorized folders
based on their file extensions.

Features:
    - Move files by type (images, documents, videos, audio, archives, code)
    - Create destination folders if they don't exist
    - Scan directories recursively or non-recursively
    - CLI arguments for flexible usage
    - Detailed logging of all operations

Concepts Used:
    - Context Manager  → logging file operations
    - OOP              → FileOrganizer class
    - Exception Handling → missing files, permission errors, invalid paths

Usage:
usage: File Organizer Automation Tool.py [-h] [--dry-run] [--recursive] [--undo] directory
    python "File Organizer Automation Tool.py" <source_directory>
    python "File Organizer Automation Tool.py" <source_directory> --dry-run
    python "File Organizer Automation Tool.py" <source_directory> --recursive
    python "File Organizer Automation Tool.py" <source_directory> --undo
"""

import os
import sys
import shutil
import argparse
import json
from datetime import datetime

# Prevent crash on Windows Command Prompt when printing emojis
if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


# ──────────────────────────────────────────────────────────────
# File Category Mappings
# ──────────────────────────────────────────────────────────────

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".odt"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".ts", ".json", ".xml"],
    "Executables": [".exe", ".msi", ".bat", ".sh", ".app"],
}


# ──────────────────────────────────────────────────────────────
# Context Manager for Logging
# ──────────────────────────────────────────────────────────────

class OrganizeLogger:
    """
    Context manager that logs all file-move operations to a log file.

    Usage:
        with OrganizeLogger("path/to/logfile.log") as logger:
            logger.log("Moved file.txt → Documents/")
    """

    def __init__(self, log_path):
        self.log_path = log_path
        self._file = None

    def __enter__(self):
        try:
            self._file = open(self.log_path, "a", encoding="utf-8")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._file.write(f"\n{'=' * 60}\n")
            self._file.write(f"  File Organizer Session — {timestamp}\n")
            self._file.write(f"{'=' * 60}\n")
        except PermissionError:
            print(f"⚠  Warning: Cannot write to log file '{self.log_path}' (permission denied).")
            self._file = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            if exc_type:
                self._file.write(f"\n❌ Session ended with error: {exc_val}\n")
            else:
                self._file.write(f"\n✅ Session completed successfully.\n")
            self._file.close()
        # Don't suppress exceptions
        return False

    def log(self, message):
        """Write a timestamped message to the log file and print it."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"  [{timestamp}] {message}"
        print(formatted)
        if self._file:
            self._file.write(formatted + "\n")


# ──────────────────────────────────────────────────────────────
# FileOrganizer Class (OOP)
# ──────────────────────────────────────────────────────────────

class FileOrganizer:
    """
    Organizes files in a source directory into categorized subfolders.

    Attributes:
        source_dir (str): The directory to organize.
        dry_run (bool): If True, only preview moves without executing them.
        recursive (bool): If True, scan subdirectories as well.
    """

    def __init__(self, source_dir, dry_run=False, recursive=False):
        self.source_dir = os.path.abspath(source_dir)
        self.dry_run = dry_run
        self.recursive = recursive
        self.history_file = os.path.join(self.source_dir, ".organize_history.json")

        # Stats
        self.files_moved = 0
        self.files_skipped = 0
        self.errors = 0

    # ── Directory Validation ──────────────────────────────────

    def validate_source(self):
        """
        Validate that the source directory exists and is accessible.

        Raises:
            FileNotFoundError: If the directory does not exist.
            NotADirectoryError: If the path is not a directory.
            PermissionError: If the directory is not readable.
        """
        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(f"Directory not found: '{self.source_dir}'")

        if not os.path.isdir(self.source_dir):
            raise NotADirectoryError(f"Path is not a directory: '{self.source_dir}'")

        if not os.access(self.source_dir, os.R_OK):
            raise PermissionError(f"No read permission for: '{self.source_dir}'")

    # ── Category Detection ────────────────────────────────────

    @staticmethod
    def get_category(filename):
        """
        Determine which category a file belongs to based on its extension.

        Args:
            filename (str): The name of the file.

        Returns:
            str: The category name (e.g., 'Images', 'Documents'), or 'Others'.
        """
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        for category, extensions in FILE_CATEGORIES.items():
            if ext in extensions:
                return category

        return "Others"

    # ── Folder Creation ───────────────────────────────────────

    def create_folder(self, folder_name, logger):
        """
        Create a category folder inside the source directory if it doesn't exist.

        Args:
            folder_name (str): Name of the folder to create.
            logger (OrganizeLogger): Logger instance for recording actions.

        Returns:
            str: The full path of the (created or existing) folder.
        """
        folder_path = os.path.join(self.source_dir, folder_name)

        if not os.path.exists(folder_path):
            if not self.dry_run:
                try:
                    os.makedirs(folder_path, exist_ok=True)
                    logger.log(f"📁 Created folder: {folder_name}/")
                except PermissionError:
                    logger.log(f"❌ Permission denied: cannot create '{folder_name}/'")
                    raise
            else:
                logger.log(f"📁 [DRY RUN] Would create folder: {folder_name}/")

        return folder_path

    # ── File Scanning ─────────────────────────────────────────

    def scan_files(self):
        """
        Scan the source directory for files to organize.

        Returns:
            list[str]: A list of absolute file paths found.
        """
        files = []

        if self.recursive:
            for root, dirs, filenames in os.walk(self.source_dir):
                # Skip already-organized category folders
                dirs[:] = [d for d in dirs if d not in FILE_CATEGORIES and d != "Others"]
                for fname in filenames:
                    filepath = os.path.join(root, fname)
                    files.append(filepath)
        else:
            for item in os.listdir(self.source_dir):
                filepath = os.path.join(self.source_dir, item)
                if os.path.isfile(filepath):
                    files.append(filepath)

        # Filter out hidden files and the organizer's own files
        files = [
            f for f in files
            if not os.path.basename(f).startswith(".")
            and os.path.basename(f) != os.path.basename(__file__)
        ]

        return files

    # ── File Moving ───────────────────────────────────────────

    def move_file(self, filepath, dest_folder, logger):
        """
        Move a single file to the destination folder.

        Handles filename conflicts by appending a counter suffix.

        Args:
            filepath (str): Path of the file to move.
            dest_folder (str): Path of the destination folder.
            logger (OrganizeLogger): Logger instance.

        Returns:
            tuple: (original_path, new_path) if moved, or None if skipped.
        """
        filename = os.path.basename(filepath)
        dest_path = os.path.join(dest_folder, filename)

        # Handle filename conflicts
        if os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                counter += 1

        try:
            if not self.dry_run:
                shutil.move(filepath, dest_path)
                logger.log(f"📄 Moved: {filename} → {os.path.basename(dest_folder)}/")
                self.files_moved += 1
                return (filepath, dest_path)
            else:
                logger.log(f"📄 [DRY RUN] Would move: {filename} → {os.path.basename(dest_folder)}/")
                self.files_moved += 1
                return None

        except PermissionError:
            logger.log(f"⚠  Skipped (permission denied): {filename}")
            self.errors += 1
            return None
        except OSError as e:
            logger.log(f"⚠  Error moving {filename}: {e}")
            self.errors += 1
            return None

    # ── Undo Support ──────────────────────────────────────────

    def save_history(self, move_records):
        """Save move history to a JSON file for undo support."""
        history = {
            "timestamp": datetime.now().isoformat(),
            "moves": [{"from": src, "to": dst} for src, dst in move_records],
        }
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except OSError:
            pass  # Non-critical — silently skip if we can't write history

    def undo(self, logger):
        """
        Undo the last organize operation by reading the history file
        and moving files back to their original locations.
        """
        if not os.path.exists(self.history_file):
            logger.log("❌ No history file found. Nothing to undo.")
            return

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.log(f"❌ Failed to read history: {e}")
            return

        moves = history.get("moves", [])
        if not moves:
            logger.log("ℹ  History is empty. Nothing to undo.")
            return

        logger.log(f"⏪ Undoing {len(moves)} move(s)...\n")
        undo_count = 0

        for record in moves:
            src = record["to"]    # current location
            dst = record["from"]  # original location

            if not os.path.exists(src):
                logger.log(f"⚠  File not found (already moved?): {src}")
                continue

            try:
                shutil.move(src, dst)
                logger.log(f"↩  Restored: {os.path.basename(src)} → {os.path.dirname(dst)}")
                undo_count += 1
            except OSError as e:
                logger.log(f"⚠  Failed to restore {os.path.basename(src)}: {e}")

        # Clean up empty category folders
        for category in list(FILE_CATEGORIES.keys()) + ["Others"]:
            folder = os.path.join(self.source_dir, category)
            if os.path.isdir(folder) and not os.listdir(folder):
                os.rmdir(folder)
                logger.log(f"🗑  Removed empty folder: {category}/")

        # Remove history file after undo
        try:
            os.remove(self.history_file)
        except OSError:
            pass

        logger.log(f"\n✅ Undo complete. Restored {undo_count}/{len(moves)} file(s).")

    # ── Main Organize Method ─────────────────────────────────

    def organize(self):
        """
        Main method: validate, scan, categorize, and move files.
        """
        # Validate source directory
        self.validate_source()

        log_path = os.path.join(self.source_dir, ".organize_log.txt")

        with OrganizeLogger(log_path) as logger:
            mode = "DRY RUN" if self.dry_run else "LIVE"
            scan = "recursive" if self.recursive else "top-level"
            logger.log(f"Source: {self.source_dir}")
            logger.log(f"Mode: {mode} | Scan: {scan}\n")

            # Scan for files
            files = self.scan_files()

            if not files:
                logger.log("ℹ  No files found to organize.")
                return

            logger.log(f"Found {len(files)} file(s) to organize.\n")

            # Organize each file
            move_records = []

            for filepath in files:
                filename = os.path.basename(filepath)
                category = self.get_category(filename)

                # Create the destination folder
                dest_folder = self.create_folder(category, logger)

                # Move the file
                result = self.move_file(filepath, dest_folder, logger)
                if result:
                    move_records.append(result)

            # Save history for undo
            if move_records and not self.dry_run:
                self.save_history(move_records)

            # Print summary
            logger.log(f"\n{'─' * 40}")
            logger.log(f"📊 Summary:")
            logger.log(f"   Files moved:   {self.files_moved}")
            logger.log(f"   Files skipped: {self.files_skipped}")
            logger.log(f"   Errors:        {self.errors}")
            logger.log(f"{'─' * 40}")


# ──────────────────────────────────────────────────────────────
# CLI Entry Point
# ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="📂 File Organizer — Automatically sort files into categorized folders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organizer.py ~/Downloads
  python organizer.py ~/Downloads --dry-run
  python organizer.py ~/Downloads --recursive
  python organizer.py ~/Downloads --undo
        """,
    )

    parser.add_argument(
        "directory",
        help="Path to the directory to organize.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving any files.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories recursively.",
    )
    parser.add_argument(
        "--undo",
        action="store_true",
        help="Undo the last organize operation.",
    )

    args = parser.parse_args()

    # Create the organizer
    organizer = FileOrganizer(
        source_dir=args.directory,
        dry_run=args.dry_run,
        recursive=args.recursive,
    )

    try:
        if args.undo:
            # Undo mode
            log_path = os.path.join(organizer.source_dir, ".organize_log.txt")
            with OrganizeLogger(log_path) as logger:
                logger.log("🔄 Starting UNDO operation...\n")
                organizer.undo(logger)
        else:
            # Normal organize mode
            organizer.organize()

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("   Please check that the directory path is correct.")
    except NotADirectoryError as e:
        print(f"\n❌ Error: {e}")
        print("   The path must point to a directory, not a file.")
    except PermissionError as e:
        print(f"\n❌ Error: {e}")
        print("   Try running with elevated permissions.")
    except KeyboardInterrupt:
        print("\n\n⚠  Operation cancelled by user.")


if __name__ == "__main__":
    main()
