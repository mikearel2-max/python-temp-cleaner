# Python Temp Cleaner

A Windows TEMP folder cleaner written in Python.

## Features
- Safe **dry-run mode** (no deletion)
- CLI and GUI interfaces
- Background threading so the GUI doesn’t freeze
- Cleanup statistics and optional log file

## Files
- `cleaner_engine.py` – core cleanup logic
- `pc_tools_cli.py` – command-line interface
- `pc_tools_gui.py` – Tkinter-based GUI

## Usage

### GUI
```bash
python pc_tools_gui.py


python pc_tools_cli.py --dry-run


Notes

This project is for learning and experimentation.