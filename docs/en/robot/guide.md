# Using the RPALite Library in Robot Framework

## Table of Contents

- [Introduction](#introduction)
- [Platform Support](#platform-support)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Importing the RPALite Library](#importing-the-rpalite-library)
- [Application Operations](#application-operations)
  - [Finding an Application](#finding-an-application)
  - [Launching an Application](#launching-an-application)
  - [Closing an Application](#closing-an-application)
  - [Maximizing a Window](#maximizing-a-window)
  - [Sleeping](#sleeping)
- [Simulating Mouse Actions](#simulating-mouse-actions)
  - [Clicking by Coordinates](#clicking-by-coordinates)
  - [Clicking by Text](#clicking-by-text)
  - [Clicking by Image](#clicking-by-image)
- [Simulating Keyboard Actions](#simulating-keyboard-actions)
  - [Typing Text at the Current Cursor Position](#typing-text-at-the-current-cursor-position)
  - [Sending Key Strokes](#sending-key-strokes)
- [Global Operations](#global-operations)
  - [Sleeping](#sleeping)
  - [Getting Screen Dimensions](#getting-screen-dimensions)
  - [Taking a Screenshot](#taking-a-screenshot)
  - [Showing the Desktop](#showing-the-desktop)
  - [Screen Recording](#screen-recording)
    - [Starting a Screen Recording](#starting-a-screen-recording)
    - [Stopping a Screen Recording](#stopping-a-screen-recording)

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
Library    RPALite    ocr_engine=paddleocr    # Use PaddleOCR (default)

*** Settings ***
Library    RPALite    ocr_engine=easyocr     # Use EasyOCR
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

## Importing the RPALite Library

You can import the RPALite library with the following code:

```robotframework
Library    RPALite
```

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

## Simulating Mouse Actions

RPALite supports various mouse simulation actions, such as clicking on text, images, and coordinates.

### Clicking by Coordinates

You can use the following code to click at specific coordinates:

```robotframework
Click By Position    10    20
```

### Clicking by Text

```robotframework
Click By Text    Text to click
```

### Clicking by Image

You can use the following code to click an image:

```robotframework
Click By Image    path/to/image.png
```

## Simulating Keyboard Actions

### Typing Text at the Current Cursor Position

You can use the following code to input a piece of text:

```robotframework
Input Text    This is a demo using RPALite.
```

### Sending Key Strokes

You can simulate pressing a key on the keyboard with the following code:

```robotframework
Send Keys    {VK_LWIN down}D{VK_LWIN up}
```

## Global Operations

### Sleeping

You can simulate a program sleep with the following code:

```robotframework
Sleep    1
```

The `Sleep` function accepts an integer parameter indicating how many seconds RPALite should sleep. This parameter is optional, and the default value is the `step_pause_interval` attribute of the rpalite object.

As mentioned earlier, this value cannot be set to 0 because after simulating mouse or keyboard actions, Windows or the program being operated also needs some time to respond. Otherwise, the likelihood of issues occurring will greatly increase. If you set this parameter to 0, RPALite will directly use the value of `step_pause_interval`. If you set the `step_pause_interval`
