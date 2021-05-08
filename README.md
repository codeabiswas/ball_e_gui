# Ball-E Graphical User Interface (GUI) Repository

This repository contains all code pertaining to Ball-E's GUI.

This document will describe the branch, folder, and file structures for the repo. It will also list any pre-requisites for running this project.

## Pre-requisites

- Python 3.8.2
- OpenCV Python
- PyQt5
- NumPy

### Setting up a Python virtual environment

If you do not know how, follow this [tutorial](https://docs.python.org/3/library/venv.html). Also, **make sure that you add this folder into the `.gitignore` file.**

**Note:** The project on the Jetson Nano does not use virtual environments to run this code since OpenCV and PyQt packages have been installed from source. However, it is recommended to set up a virtual environment on a machine other than the Nano when developing for this project.

## Branch Structure

### main

Contains 'production-level', 100% working code.

### develop

Contains beta code. This will the primary branch for For system-wide testing.

### feature branches

Feature branches are development branches. It will follow the following naming convention:

`feature/<feature-name>`

Ensure this branch is always updated with `develop`'s code.

## Folder Structure

### `docs/`

Contains folders and their respective `.md` (Markdown) files pertaining to each Help section.

### `src/`

Contains the source code for the GUI.

### `src/components/`

Contains all the visual objects that are leveraged by other screens. This is done to reduce repetitiveness and follow a decent visual similarity across the UI for ease-of-use.

### `src/helpers/`

Contains all the helper code that helps in parsing/creating objects in the disk or constants that are used throughout the project.

### `src/images/`

Contains `.png` images that are used in the project or taken by the user for goal calibration steps.

### `src/screens/`

Contains all the screens (technically `QWidget` objects) for Ball-E. These screens widgets are shown using the `QMainWindow` objects, which is described below.

### `src/windows/`

Contains the window objects, which are used to instantiate all the widgets in `src/screens/`.

## File Structure

Based on which folder a file pertains to, the filename should preface with its name for ease of accessbility.

**Example**: If the file is in the `component` folder, its name should be `component_<filename>.py`.

### `requirements.txt`

Since this project is primarily in Python, this file will be constantly updated with the packages required to compile and run this project.

To install this project's required packages:
`pip install -r requirements.txt`

To update this project's required packages
`pip freeze > requirements.txt`

## Acknowledgements and Usage Agreement
This code is written for the P21390 Project for Rochester Institute of Technology's, Kate Gleason College of Engineering's, Multidisciplinary Senior Design class. You may use and edit the contents of this code freely in your own projects as long as the following is mentioned in your source code/documentation at least once:
* This [Confluence page's URL](https://wiki.rit.edu/display/MSDShowcase/P21390+Bi-Axial+Autonomous+Lacrosse+Learning+Evaluator) which talks about the project

