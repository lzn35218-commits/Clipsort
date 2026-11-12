#!/usr/bin/env python3
"""Organize media files into Videos, Audio, and Images folders.

This utility moves files. Use --dry-run to preview changes before applying them.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

VIDEO_EXTENSIONS = {
    ".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".mpeg", ".mpg",
}
AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".aiff",
}
IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".tif", ".tiff", ".bmp",
}

CATEGORIES = {
    "Videos": VIDEO_EXTENSIONS,
    "Audio": AUDIO_EXTENSIONS,
    "Images": IMAGE_EXTENSIONS,
}


def category_for(path: Path) -> str | None:
    """Return the destination category for a supported media file."""
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return None


def unique_destination(destination: Path) -> Path:
    """Return a non-existing destination path without overwriting files."""
    if not destination.exists():
        return destination
    stem, suffix = destination.stem, destination.suffix
    counter = 1
    while True:
        candidate = destination.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def collect_files(source: Path, recursive: bool) -> list[Path]:
    iterator = source.rglob("*") if recursive else source.iterdir()
    output_dirs = {source / name for name in CATEGORIES}
    found = []
    for item in iterator:
        if not item.is_file() or item.name.startswith("."):
            continue
        # Never re-process files already in ClipSort's destination folders.
        if any(parent in output_dirs for parent in item.parents):
            continue
        if category_for(item):
            found.append(item)
    return sorted(found)


def organize(source: Path, recursive: bool = False, dry_run: bool = False) -> list[tuple[Path, Path]]:
    """Plan and optionally perform moves. Returns (source, destination) pairs."""
    source = source.expanduser().resolve()
    if not source.exists() or not source.is_dir():
        raise ValueError(f"Source folder does not exist or is not a directory: {source}")

    moves = []
    for item in collect_files(source, recursive):
        category = category_for(item)
        assert category is not None
        target_dir = source / category
        target = unique_destination(target_dir / item.name)
        moves.append((item, target))

    for original, target in moves:
        print(f"{'[DRY RUN] ' if dry_run else ''}{original} -> {target}")
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(original), str(target))
    return moves


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sort video, audio, and image files into folders."
    )
    parser.add_argument("folder", help="Folder containing media files")
    parser.add_argument("--recursive", action="store_true",
                        help="Also scan subfolders")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview moves without changing files")
    args = parser.parse_args()

    try:
        moves = organize(Path(args.folder), args.recursive, args.dry_run)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Found {len(moves)} supported media file(s).")
    if args.dry_run:
        print("Preview only: no files were moved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
