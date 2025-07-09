# Self-Checkout System Using YOLOv10

This repository contains a simple self‑checkout prototype that relies on YOLOv10 for object detection. The application is written with Tkinter and can be packaged as a Windows executable using PyInstaller.

## Building the executable

Install the dependencies from `requirements.txt` inside a virtual environment and run PyInstaller from the project root:

```powershell
pyinstaller Main.py --name SelfCheckout --noconsole --onefile \
    --add-data "runs\datasets;runs\datasets" \
    --hidden-import mediapipe
```

If you want the executable to start with a fresh database, also pass:

```powershell
--add-data "sales.db;."
```

`SelfCheckout.exe` will be created inside the `dist/` folder.

## Preparing runtime files

The application expects all data files in the same directory as the executable. After building, copy the following into `dist/` next to `SelfCheckout.exe`:

- the `runs/` folder containing `datasets/`, weights (`*.pt`) and YAML files
- `sales.db`
- `train_model.py` (for on‑device re‑training)

With these files present, the program can run entirely from inside `dist/` because every path is resolved relative to the executable.

## Running

Double‑click `SelfCheckout.exe` (or run it from the command line) from inside `dist/`. The login screen should appear and all features—including scanning, training and database updates—will operate using the files located within `dist/`.

## Confidence threshold

When scanning items, the application only accepts predictions whose confidence score is at least `0.6`. If no high-confidence object is detected, the user is asked to rescan the item.

