# RPALite - An Open Source RPA (Robotic Process Automation) Programming Library for Python and Robot Framework

| [English](README.md) | [中文](README-zh.md) |

[![PyPI](https://img.shields.io/pypi/v/RPALite?color=blue&label=PyPI%20Package)](https://pypi.org/project/RPALite/)
[![License](https://img.shields.io/github/license/jieliu2000/RPALite)](https://github.com/jieliu2000/RPALite/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RPALite)](https://www.python.org/downloads/)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Platform Support](#platform-support)
- [OCR Engine Options](#ocr-engine-options)
- [Performance Optimization](#performance-optimization)
- [Documentation](#documentation)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [Python](#python)
  - [Robot Framework](#robot-framework)
- [Contribution Guidelines](#contribution-guidelines)

## Introduction

RPALite is an open-source RPA (Robotic Process Automation) library. You can use RPALite through Python or [Robot Framework](https://robotframework.org/) to achieve various automation tasks with minimal code.

RPALite provides powerful automation capabilities with a simple API, allowing you to automate UI interactions, data entry, and image-based operations across different applications.

RPALite currently only supports the Windows platform. Support for macOS and Linux is under active development.

## Features

RPALite supports the following operations:

- **Application Management**

  - Launching applications
  - Finding applications by name or class name
  - Closing applications (with force quit option)
  - Window management (maximize, minimize, show desktop)

- **Mouse Operations**

  - Clicking by coordinates, text or images
  - Support for left-click, right-click, and double-click operations
  - Mouse press/release for drag and drop operations
  - Scrolling operations
  - Moving cursor to text elements

- **Keyboard Operations**

  - Text input at cursor position
  - Advanced keyboard input with special keys and combinations
  - Text field interaction based on labels

- **Visual Automation**

  - OCR-based text recognition (multiple language support)
  - Image-based location and verification
  - Finding all instances of an image on screen
  - Waiting for text or images to appear/disappear
  - Screen recording capabilities

- **UI Automation**

  - Finding controls by label, text vicinity, or automated IDs
  - Flexible UI element locator system
  - Control interaction based on element properties

- **Utility Features**
  - Clipboard operations (get/set)
  - Screenshot capabilities
  - Synchronization mechanisms (waits and sleeps)

## Platform Support

### Windows

- Full automation support including UI controls
- Windows-specific features like UI Automation
- Administrative privileges may be required for some features

### macOS (Under Development)

- macOS support is currently under development
- The code is not yet stable, so macOS-related features have been temporarily disabled
- We are working to provide full macOS support in future releases

### Linux (Planned)

- Linux support is planned for future releases
- Currently in early design phase

## OCR Engine Options

RPALite supports two OCR engines for text recognition:

- **EasyOCR** (Default)

  - Better multi-language support
  - Suitable for general-purpose OCR tasks
  - Larger model size

- **PaddleOCR**
  - Better performance for Chinese text
  - Smaller model size
  - Faster inference speed

You can specify which engine to use during initialization:

```python
# Using the default (EasyOCR)
rpa = RPALite()

# Using PaddleOCR
rpa = RPALite(ocr_engine="paddleocr")
```

### Language Configuration

#### Automatic Language Detection

RPALite automatically detects your operating system's display language and adds appropriate language support for OCR engines. For example, if your system is set to Chinese, Chinese language support will be automatically added to improve text recognition accuracy. This feature works with both EasyOCR and PaddleOCR engines.

#### Manual Language Configuration

You can also manually specify languages for OCR recognition:

```python
# For EasyOCR
rpa = RPALite(ocr_engine="easyocr", languages=["en", "ch_sim", "fr"])

# For PaddleOCR
rpa = RPALite(ocr_engine="paddleocr", languages=["en", "ch", "fr"])
```

**Language Code References:**

- **EasyOCR**: [Supported Languages](https://github.com/JaidedAI/EasyOCR#supported-languages)
- **PaddleOCR**: [Language Support](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/multi_languages_en.md)

## Performance Optimization

The most time-consuming operations in RPALite are image recognition and OCR. Both OCR engines run more efficiently on computers with dedicated GPUs and CUDA support. If you find RPALite running slowly, consider running it on a computer with a dedicated GPU and CUDA support and installing the appropriate version of PyTorch.

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

#### Basic Example

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

#### Advanced Features Example

```python
from RPALite import RPALite
rpalite = RPALite()

# Wait for text to appear with timeout
position = rpalite.wait_until_text_shown("Login", timeout=10)

# Click on a button identified by text
rpalite.click_by_text("Sign In")

# Work with form fields
rpalite.enter_in_field("Username", "my_user")
rpalite.enter_in_field("Password", "my_password")

# Wait for an image to appear
rpalite.wait_until_image_shown("dashboard_icon.png", timeout=15)

# Start screen recording
recording_path = rpalite.start_screen_recording(fps=15)

# Perform some operations...

# Stop recording
rpalite.stop_screen_recording()
```

#### Advanced Keyboard Input Examples

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

#### Basic Example

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

#### Advanced Features Example

```robotframework
*** Settings ***
Library    RPALite
Library    OperatingSystem

*** Test Cases ***
Login Form Automation
    # Wait for text to appear with timeout
    ${position} =    Wait Until Text Shown    Login    timeout=10

    # Click on UI elements
    Click By Text    Sign In

    # Fill in form fields
    Enter In Field    Username    my_user
    Enter In Field    Password    my_password

    # Take screenshot for verification
    ${screenshot} =    Take Screenshot    filename=login_screen.png

    # Wait for an image to appear on screen
    Wait Until Image Shown    dashboard_icon.png    timeout=15

    # Start screen recording
    ${recording_path} =    Start Screen Recording    fps=15

    # Perform test operations
    Click By Text    Dashboard
    Sleep    2

    # Validate text exists on screen
    Validate Text Exists    Welcome, my_user

    # Stop recording
    ${final_path} =    Stop Screen Recording
    Log    Recording saved to: ${final_path}
```

#### Advanced Keyboard Input Example

```robotframework
*** Settings ***
Library    RPALite

*** Test Cases ***
Keyboard Operations
    # Simple text input
    Input Text    Hello from Robot Framework!

    # Special keys and combinations
    Send Keys    {ENTER}
    Send Keys    ^a    # Select all
    Send Keys    ^c    # Copy
    Send Keys    {TAB}
    Send Keys    ^v    # Paste

    # Function keys and modifiers
    Send Keys    {F5}
    Send Keys    %{F4}    # Alt+F4

    # Get clipboard content
    ${clipboard_text} =    Get Clipboard Text
    Log    Clipboard contains: ${clipboard_text}
```

## Contribution Guidelines

If you wish to contribute code to RPALite, feel free to submit a Pull Request. Ensure your code style is consistent with the existing codebase and passes all tests in the tests directory. Additionally, make sure to update unit tests for any new or modified code.

- GitHub Repository: https://github.com/jieliu2000/RPALite
- Gitee Repository: https://gitee.com/jieliu2000/rpalite
- Gitcode Repository: https://gitcode.com/jieliu2000/rpalite
