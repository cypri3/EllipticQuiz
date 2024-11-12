# Quiz Question Extractor and Revision Quiz Application

This is a Python-based tool designed for two main purposes:

1. **Quiz Question Extractor**: Extracts questions and answers from a PDF document, saving them as images for use in a quiz application.
2. **Revision Quiz Application**: A quiz application that presents questions from extracted images, allowing users to answer, check results, and track scores.

## Important Note

The data used in this project is derived from the course taught by Niels FELD, which itself is based on *Elliptic Curves, Number Theory and Cryptography* by Lawrence C. Washington (2008). The original course material is in English; however, the questions in this quiz project are presented in French.

## Features

### Quiz Question Extractor
- Extracts questions and answers from a PDF document.
- Detects comments associated with questions and saves these as images.
- Saves extracted questions, answers, and comments as PNG images in designated folders for easy access.

### Revision Quiz Application
- Presents random questions from images stored in folders.
- Supports both True/False and numeric-answer questions.
- Tracks the score and provides feedback on incorrect answers when needed.
- Automatically hides the "cheat" button for numeric questions and displays it for True/False questions.
- Allows manual input for numeric answers and buttons for True/False responses.

## Requirements

- Python 3.x
- Libraries:
  - PyMuPDF (`fitz`)
  - OpenCV (`cv2`)
  - Pillow (`PIL`)
  - Tkinter (for the GUI)

You can install the necessary libraries using `pip`:

```bash
pip install PyMuPDF opencv-python Pillow
```

### Tkinter installation (if not already installed):
For some Python versions, Tkinter might not come pre-installed. Install it via your package manager:
- On Debian-based systems (e.g., Ubuntu):
  ```bash
  sudo apt-get install python3-tk
  ```
- On macOS, Tkinter should be installed by default.

## Usage

1. **Quiz Question Extractor**:
   - Run the script to extract questions and answers from your PDF document.
   - Extracted questions and answers will be saved as PNG images in specified folders for use in the quiz application.

2. **Revision Quiz Application**:
   - Place the extracted question images in the `question` folder and answer images in the `reponse` folder.
   - Run the application to display a random question from the folder.
   - Use True/False buttons for corresponding questions and numeric entry for numeric questions.
   - Track your score as you progress through questions.
   - The cheat button allows you to view correct answers, but is automatically hidden for numeric questions.

## Planned Features

- **Improved UI**: Enhance the user interface, particularly for displaying feedback when answers are incorrect.
- **Confidence-based Answer Options**: Add an option to select True/False answers with a confidence indicator.