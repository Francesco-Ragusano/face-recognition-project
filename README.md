# Real-Time Face Recognition

A simple Python script that recognizes known faces from your webcam in real time, using [OpenCV](https://opencv.org/) and [face_recognition](https://github.com/ageitgey/face_recognition).

Each detected face gets a bounding box, a name label and a crosshair at its center: **green** for known people and **red** for unknown ones.

## Features

- Loads several reference photos per person for better accuracy
- Live webcam recognition with an adjustable matching tolerance
- Different colors for known and unknown faces
- Crosshair pointer centered on each detected face
- On-screen warning when the reference folder is missing, is empty, or has no usable faces

## Requirements

- Python 3.8+
- A webcam
- [CMake](https://cmake.org/), which `dlib` (a dependency of `face_recognition`) needs to build

### Installation

```bash
pip install opencv-python face_recognition
```

On macOS you can install CMake with Homebrew first:

```bash
brew install cmake
```

## Project structure

```
.
├── riconoscimento_volti.py
└── volti-fr/
    ├── P1_1.jpg
    ├── P1_2.jpg
    ├── P2_1.jpg
    └── P3_1.jpeg
```

## Setting up reference images

1. Create a folder called `volti-fr` next to the script.
2. Add `.jpg` or `.jpeg` photos of each person you want to recognize.
3. Start each file name with the person's label (`P1`, `P2`, `P3`). The label is the name shown on screen.
4. Use clear, front-facing photos with one face per image. Images where no face is detected are skipped.

To add more people or rename them, edit this list in the script:

```python
for nome in ['P1', 'P2', 'P3']:
```

## Usage

```bash
python riconoscimento_volti.py
```

- The number of loaded encodings is printed to the terminal.
- A window called **Camera** opens with the live feed.
- Press **`q`** to quit.

If no reference faces are loaded, the program still runs: every face is labeled *Sconosciuto* (unknown), and a warning banner appears at the top of the window.

## Configuration

| Setting | Where | Default | Notes |
|---|---|---|---|
| Reference folder | `cartella` | `'volti-fr'` | Path to the reference images |
| People | `['P1', 'P2', 'P3']` | 3 labels | File name prefixes |
| Tolerance | `compare_faces(..., tolerance=0.5)` | `0.5` | Lower is stricter (fewer false matches) |
| Camera | `cv2.VideoCapture(0)` | `0` | Change the index to use another camera |

## Notes

- Recognition runs on every full-resolution frame, so it can be slow on older hardware. Shrinking the frame before detection makes it much faster.
- When a face matches more than one reference, the first match in the list wins.

## Privacy

Only use photos of people who have agreed to it. Face data counts as personal data under GDPR. Keep the `volti-fr/` folder out of public repositories by adding it to `.gitignore`:

```
volti-fr/
```
