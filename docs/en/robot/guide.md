# Using the RPALite Library in Robot Framework

## Table of Contents

- [Introduction](#introduction)
- [Platform Support](#platform-support)
- [OCR Engine Configuration](#ocr-engine-configuration)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Application Operations](#application-operations)
  - [Finding an Application](#finding-an-application)
  - [Launching an Application](#launching-an-application)
  - [Closing an Application](#closing-an-application)
  - [Maximizing a Window](#maximizing-a-window)
- [Mouse Operations](#mouse-operations)
  - [Getting Cursor Position](#getting-cursor-position)
  - [Moving Mouse](#moving-mouse)
  - [Clicking by Coordinates](#clicking-by-coordinates)
  - [Clicking by Text](#clicking-by-text)
  - [Clicking by Image](#clicking-by-image)
- [Keyboard Operations](#keyboard-operations)
  - [Typing Text](#typing-text)
  - [Sending Keys](#sending-keys)
  - [Validating Text](#validating-text)
  - [Finding Text Positions](#finding-text-positions)
- [Clipboard Operations](#clipboard-operations)
  - [Getting Clipboard Text](#getting-clipboard-text)
  - [Setting Clipboard Text](#setting-clipboard-text)
- [Global Operations](#global-operations)
  - [Sleep](#sleep)
  - [Show Desktop](#show-desktop)
  - [Get Screen Size](#get-screen-size)
  - [Take Screenshot](#take-screenshot)

## Introduction

This guide provides detailed information on how to use RPALite with Robot Framework. RPALite is an open-source RPA (Robotic Process Automation) library that allows you to automate various tasks through Robot Framework.

### Platform Support

RPALite currently supports the following platforms:

- **Windows**: Full automation support including UI controls
- **macOS (Under Development)**: Basic automation support is under development

### OCR Engine Configuration

RPALite supports two OCR engines:

- **EasyOCR** (Default)
  - Supports more languages out of the box
  - Better for general purpose OCR
  - Larger model size
- **PaddleOCR**
  - Better performance for Chinese text recognition
  - Smaller model size
  - Faster inference speed

You can configure the OCR engine when initializing RPALite:

```robotframework
*** Settings ***
Library    RPALite    ocr_engine=easyocr    # Use EasyOCR (default)

*** Settings ***
Library    RPALite    ocr_engine=paddleocr  # Use PaddleOCR
```

### Installation

To install RPALite, use pip:

```bash
pip install RPALite
```

### Basic Usage

Here's a simple example of using RPALite with Robot Framework:

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

### Advanced Features

RPALite provides many advanced features including:

- Image recognition
- OCR (Optical Character Recognition) with support for multiple engines
- Window management
- Clipboard operations
- Keyboard and mouse control

### Troubleshooting

If you encounter any issues:

1. Ensure you have the required permissions
2. Check the log files for error messages
3. Verify that all dependencies are properly installed
4. For Windows, ensure you have administrative privileges if required

## Application Operations

### Launching an Application

You can use the following code to launch an application:

```robotframework
Run Command    notepad.exe
```

### Finding an Application

You can find an application with the following code:

```robotframework
${app} =    Find Application    .*Notepad
```

The `Find Application` keyword supports finding an application through the following parameters:

- `title`: A string representing the regular expression that the application's title must match,
- `classname`: A string representing the class name of the application. To find the class name of an application, you can use the [Accessibility Insights for Windows tool](https://accessibilityinsights.io/) to view it.

### Closing an Application

You can close an application with the following code:

```robotframework
${app} =    Find Application    .*Notepad
Close App
```

### Maximizing a Window

To maximize a program, you first need to locate the program (refer to [Finding an Application](#finding-an-application)), then call the `Maximize Window` method:

```robotframework
${app} =     Find Application    .*Notepad
Maximize Window    ${app}
```

## Mouse Operations

### Getting Cursor Position

```robotframework
${position} =    Get Cursor Position
Log    Cursor position: ${position}
```

### Moving Mouse

```robotframework
Move Mouse    100    200    # Move to absolute position
```

### Clicking by Text

```robotframework
Click By Text    Click me    # Clicks on text that matches "Click me"
```

## Keyboard Operations

### Typing Text

```robotframework
Input Text    Hello World    # Types "Hello World" at current cursor position
```

### Sending Keys

```robotframework
Send Keys    {ENTER}    # Sends Enter key
Send Keys    ^c         # Sends Ctrl+C
Send Keys    %{F4}      # Sends Alt+F4
```

### Finding Text Positions

```robotframework
${positions} =    Find Text Positions    Text to find
Log    Text positions: ${positions}
```

## Clipboard Operations

### Getting Clipboard Text

```robotframework
${text} =    Get Clipboard Text
Log    Clipboard content: ${text}
```

### Setting Clipboard Text

```robotframework
Copy Text To Clipboard    This is a test
```

## Global Operations

### Sleep

```robotframework
Sleep    5    # Sleep for 5 seconds
```

### Show Desktop

```robotframework
Show Desktop
```

### Get Screen Size

```robotframework
${size} =    Get Screen Size
Log    Screen size: ${size}
```

### Take Screenshot

```robotframework
${image} =    Take Screenshot
Take Screenshot    filename=screenshot.png    # Save to file
```
