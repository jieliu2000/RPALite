# RPALite - An Open Source RPA (Robotic Process Automation) Programming Library for Python and Robot Framework

| [English](README.md) | [中文](README-zh.md) |

[![PyPI](https://img.shields.io/pypi/v/RPALite?color=blue&label=PyPI%20Package)](https://pypi.org/project/RPALite/)
[![License](https://img.shields.io/github/license/jieliu2000/RPALite)](https://github.com/jieliu2000/RPALite/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RPALite)](https://www.python.org/downloads/)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Platform Support](#platform-support)
- [Performance Optimization](#performance-optimization)
- [Documentation](#documentation)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [Python](#python)
  - [Robot Framework](#robot-framework)
- [Contribution Guidelines](#contribution-guidelines)

## Introduction

RPALite is an open-source RPA (Robotic Process Automation) library. You can use RPALite through Python or [Robot Framework](https://robotframework.org/) to achieve various automation tasks.

RPALite now supports Windows platform. Supporting for macOS and Linux is under development.

## Features

RPALite supports the following operations:

- Launching applications
- Finding applications by name or ClassName
- Closing applications
- Mouse clicking on specific text
- Locating and inputting into text boxes based on placeholders or labels
- Mouse clicking based on coordinates
- Support for left-click, right-click, and double-click operations
- Locating controls based on control names, classes, or Automation IDs (Windows) and getting their coordinates
- Image-based location. You can pass a partial screenshot to RPALite to return the coordinates of the corresponding part on the screen.
- Screen recording capabilities
- Clipboard operations
- Advanced keyboard input support with special keys and combinations
- Window management (maximize, minimize, show desktop)

## Platform Support

### Windows

- Full automation support including UI controls
- Windows-specific features like UI Automation
- Administrative privileges may be required for some features

### macOS (Under Development)

- Basic macOS automation support is now available
- Key features supported:
  - Application launching and window management
  - Keyboard and mouse input
  - Screen capture and OCR text detection
  - Clipboard operations
- System dependencies:
  - pyobjc-core: Core Objective-C bindings
  - pyobjc-framework-Cocoa: AppKit and Foundation frameworks
  - pyobjc-framework-Quartz: Screen capture and image processing
  - pyobjc-framework-ApplicationServices: Accessibility and user input
  - macOS 10.14 or later recommended
- Installation of system dependencies:
  ```bash
  # Install required macOS dependencies
  pip install pyobjc-core pyobjc-framework-Cocoa pyobjc-framework-Quartz pyobjc-framework-ApplicationServices
  ```
- Known limitations:
  - No UI element identification through accessibility frameworks yet
  - Limited support for application-specific automation
  - Some features may require additional permissions in System Settings > Privacy & Security

#### macOS System Permission Setup

To use RPALite on macOS, you need to grant the necessary permissions in System Settings:

1. **Screen Recording Permission**:

   - Go to System Settings > Privacy & Security > Screen Recording
   - Click the "+" button to add applications
   - For Terminal:
     - Navigate to `/Applications/Utilities/Terminal.app`
     - Select Terminal and click "Open"
   - For VSCode:
     - Navigate to `/Applications/Visual Studio Code.app` (or your custom installation location)
     - Select VSCode and click "Open"
   - Restart Terminal or VSCode after adding them
   - This permission is required for taking screenshots and OCR functionality

2. **Accessibility Permission**:

   - Go to System Settings > Privacy & Security > Accessibility
   - Click the "+" button to add applications
   - For Terminal:
     - Navigate to `/Applications/Utilities/Terminal.app`
     - Select Terminal and click "Open"
   - For VSCode:
     - Navigate to `/Applications/Visual Studio Code.app`
     - Select VSCode and click "Open"
   - Make sure the checkboxes next to Terminal and VSCode are checked
   - This permission is required for mouse and keyboard simulation

3. **Automation Permission**:

   - These permissions are requested dynamically when your script attempts to control an application
   - When prompted, click "OK" to allow your script to control the target application
   - To pre-approve applications (optional):
     - Go to System Settings > Privacy & Security > Automation
     - You'll see a list of applications that can control other apps
     - Check the boxes for the apps you want to allow Terminal or VSCode to control

4. **Adding Python Directly (Alternative Method)**:
   - If running scripts directly with Python and not through Terminal/VSCode:
     - Find your Python installation (usually in `/usr/local/bin/python3` or within a virtual environment)
     - Add this Python executable to both Screen Recording and Accessibility permissions
   - If using Homebrew Python:
     - Add `/opt/homebrew/bin/python3` (for Apple Silicon) or `/usr/local/bin/python3` (for Intel Macs)

Note: The exact path to these settings may vary slightly depending on your macOS version. In older macOS versions, these settings are in System Preferences > Security & Privacy > Privacy.

#### macOS Troubleshooting Tips

If you encounter issues when running RPALite on macOS:

1. **Permission Errors**:

   - Ensure your terminal/IDE has the required permissions (see macOS System Permission Setup)
   - Try running your script with administrator privileges using `sudo python your_script.py`
   - If prompted for application control, always click "OK"

2. **OCR or Screenshot Issues**:

   - Verify Screen Recording permission is granted for your terminal/IDE
   - Try using a different OCR engine: `rpalite = RPALite(ocr_engine="paddleocr")`
   - For poor text recognition, adjust screen resolution or increase font size

3. **Mouse/Keyboard Control Issues**:

   - Verify Accessibility permission is granted
   - Use absolute coordinates for clicking if text-based clicking fails
   - For keyboard input issues, try using `send_keys()` method instead of `input_text()`

4. **Application Launch Problems**:
   - Specify the full path to the application if `run_command()` fails
   - For some apps, use the full name with `.app` extension: `"Calculator.app"`
   - Check if the application bundle name is correct

### Linux

- Full automation support for X11-based desktop environments
- Requires X Window System (X11) and a graphical desktop environment
- System dependencies:
  - xdotool: For keyboard and mouse simulation
  - wmctrl: For window management
  - python-xlib: For X11 interaction
- Installation of system dependencies:

  ```bash
  # Ubuntu/Debian
  sudo apt-get install xdotool wmctrl python3-xlib

  # CentOS/RHEL
  sudo yum install xdotool wmctrl python3-xlib

  # Arch Linux
  sudo pacman -S xdotool wmctrl python-xlib
  ```

## Performance Optimization

The most time-consuming operations in RPALite are image recognition and OCR. For OCR, users could choose to use [EasyOCR](https://github.com/JaidedAI/EasyOCR) or [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR). Both OCR engines run more efficiently on computers with dedicated GPUs and CUDA support. If you find RPALite running slowly, consider running it on a computer with a dedicated GPU and CUDA support and installing the appropriate version of PyTorch.

## Documentation

In the following sections, we provide a [Quick Start Guide](#quick-start) to give you a basic understanding of RPALite.

Here are links to more detailed documentation:

- [Programming Guide for Using RPALite in Python](docs/en/python/guide.md)
- [Programming Guide for Using RPALite in Robot Framework](docs/en/robot/guide.md)

In addition to the above documents, we provide an English version of the Robot Framework Library documentation, which you can access through the [Online Robot Framework Documentation](https://jieliu2000.github.io/RPALite/docs/en/robot/RPALite.html). If you prefer to view it locally, you can open the [Robot Framework Library documentation in the project directory](docs/en/robot/RPALite.html).

## Installation

You can install RPALite via pip:

```bash
pip install RPALite
```

Platform-specific dependencies will be automatically installed based on your operating system.

## Quick Start

As mentioned earlier, you can use RPALite with Python or Robot Framework. Here are some examples:

### Python

#### Windows Example

Below is an example of using RPALite to operate Windows Notepad:

```python
from RPALite import RPALite
rpalite = RPALite()

# Show the desktop
rpalite.show_desktop()

# Run Notepad and input some text
rpalite.run_command("notepad.exe")
rpalite.input_text("This is a demo using RPALite.\n")

# Find the Notepad app and close it
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```

#### Linux Example

Below is an example of using RPALite to operate Linux Calculator:

```python
from RPALite import RPALite
rpalite = RPALite()

# Launch Calculator
rpalite.launch_application("gnome-calculator")  # For GNOME
# or
rpalite.launch_application("kcalc")  # For KDE

# Click on number 5
rpalite.click_text("5")

# Click on plus button
rpalite.click_text("+")

# Click on number 3
rpalite.click_text("3")

# Click on equals button
rpalite.click_text("=")

# Verify result
result = rpalite.get_text_from_coordinates(100, 100)  # Adjust coordinates based on your calculator
assert result == "8"
```

#### macOS Example

Below is an example of using RPALite to operate macOS Calculator:

```python
from RPALite import RPALite
rpalite = RPALite()

# Launch Calculator
rpalite.run_command("Calculator")

# Click on number 5
rpalite.click_text("5")

# Click on plus button
rpalite.click_text("+")

# Click on number 3
rpalite.click_text("3")

# Click on equals button
rpalite.click_text("=")

# Get the result (using clipboard since element detection is limited)
rpalite.click_text("Edit")
rpalite.click_text("Copy")
result = rpalite.get_clipboard_text()
assert result.strip() == "8"
```

### Advanced Keyboard Input Examples

```python
# Simple text input
rpalite.send_keys("Hello World")

# Special keys
rpalite.send_keys("{ENTER}")
rpalite.send_keys("{ESC}")

# Key combinations
rpalite.send_keys("^c")          # Control+C
rpalite.send_keys("%{F4}")       # Alt+F4
rpalite.send_keys("+(abc)")      # Shift+ABC (uppercase)
```

### Robot Framework

#### Windows Example

Below is an example of using RPALite to operate Windows Notepad:

```robotframework
*** Settings ***
Library    RPALite

*** Test Cases ***
Test Notepad
    Send Keys    {VK_LWIN down}D{VK_LWIN up}
    Run Command    notepad.exe
    ${app} =     Find Application    .*Notepad
    Maximize Window    ${app}
    Input Text    This is a demo using RPALite.
    Close App    ${app}
```

## Contribution Guidelines

If you wish to contribute code to RPALite, feel free to submit a Pull Request. Ensure your code style is consistent with the existing codebase and passes all tests in the tests directory. Additionally, make sure to update unit tests for any new or modified code.

- GitHub Repository: https://github.com/jieliu2000/RPALite
- Gitee Repository: https://gitee.com/jieliu2000/rpalite
- Gitcode Repository: https://gitcode.com/jieliu2000/rpalite
