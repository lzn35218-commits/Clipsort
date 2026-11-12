# ClipSort

A small, transparent command-line utility that helps video editors organize media files into folders by file type.

**Project status:** Early-stage / experimental. This repository is a starting point for testing and community feedback. It does not claim an existing user base, download numbers, or external contributors.

## What it does

- Scans one folder for media files.
- Sorts supported files into `Videos`, `Audio`, and `Images` folders.
- Supports a dry-run preview before moving anything.
- Avoids overwriting files by adding a numbered suffix when a filename already exists.
- Can scan subfolders when `--recursive` is used.

Supported extensions are listed in `clipsort.py` and can be extended.

## Requirements

- Python 3.9 or newer
- No third-party Python packages

## Usage

Preview what would happen (recommended first):

```bash
python clipsort.py "/path/to/media" --dry-run
```

Organize files:

```bash
python clipsort.py "/path/to/media"
```

Include nested folders:

```bash
python clipsort.py "/path/to/media" --recursive --dry-run
```

Apply the recursive organization after reviewing the preview:

```bash
python clipsort.py "/path/to/media" --recursive
```

By default, the tool does not scan hidden files or move files already inside its output folders.

## Safety notes

- Start with a copy of important footage.
- Run `--dry-run` first and inspect the proposed moves.
- ClipSort moves files; it does not edit, compress, or delete media.
- Do not run it on system folders or folders you do not own or have permission to manage.

## Development

Run the tests:

```bash
python -m unittest discover -s tests -v
```

## Contributing

Bug reports, documentation improvements, and tested feature suggestions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Roadmap

See [ROADMAP.md](ROADMAP.md). Roadmap items are plans, not implemented features.

## License

MIT. See [LICENSE](LICENSE).
