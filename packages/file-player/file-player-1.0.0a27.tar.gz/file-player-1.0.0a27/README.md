# File Player

Features:
* **Uses as structure the file system**, rather than audio tags
* Fade out of tracks when switching/stopping/pausing
* Stopping playing after current track
* Duplicate track

## Installation

Requirements:
* Python 3.8 (possibly working with earlier versions of Python)
  * you can see the python version by typing `python3 --version` (on Linux-based systems) or `python --version` (on Windows and MacOS)
  * Python 3.8 is included with Ubuntu 20.04
* (Other requirements will be installed when using `pip`/`pip3` to install)

Tested on:
* Xubuntu 20.04 LTS
* Windows 7 (might be a bit tricky to get this working)

### Ubuntu

`pip3 install file-player`

### Windows

1. Download and install Python 3.x (Windows 7 supports up to 3.8, but not higher, so if you are using Windows 7 please make sure to download the 3.8 version rather than the latest)
2. `pip install file-player`

### Starting

`file-player` from the command line

## Usage

### Quick start

The left side shows the file system and the right side shows the play list

To add play a track you can double-click on a file on the left side and it will be added and played

### Integration with file manager

On Ubuntu: Open with -> Open with other application -> custom command -> enter "file-player" in the text area

