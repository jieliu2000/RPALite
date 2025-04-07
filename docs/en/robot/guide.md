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
  - [Launching an Application](#launching-an-application)
  - [Finding an Application](#finding-an-application)
  - [Closing an Application](#closing-an-application)
  - [Maximizing a Window](#maximizing-a-window)
- [Mouse Operations](#mouse-operations)
  - [Getting Cursor Position](#getting-cursor-position)
  - [Moving Mouse](#moving-mouse)
  - [Moving Mouse to Text](#moving-mouse-to-text)
  - [Clicking by Coordinates](#clicking-by-coordinates)
  - [Clicking by Text](#clicking-by-text)
  - [Clicking by Image](#clicking-by-image)
  - [Mouse Press and Release](#mouse-press-and-release)
  - [Scrolling](#scrolling)
- [Keyboard Operations](#keyboard-operations)
  - [Typing Text](#typing-text)
  - [Sending Keys](#sending-keys)
  - [Entering Text in Fields](#entering-text-in-fields)
  - [Getting Field Value](#getting-field-value)
  - [Validating Text](#validating-text)
  - [Finding Text Positions](#finding-text-positions)
  - [Waiting for Text to Appear](#waiting-for-text-to-appear)
  - [Waiting for Text to Disappear](#waiting-for-text-to-disappear)
- [Clipboard Operations](#clipboard-operations)
  - [Getting Clipboard Text](#getting-clipboard-text)
  - [Setting Clipboard Text](#setting-clipboard-text)
- [Image Operations](#image-operations)
  - [Finding an Image](#finding-an-image)
  - [Finding All Image Instances](#finding-all-image-instances)
  - [Waiting for an Image](#waiting-for-an-image)
- [Control Operations](#control-operations)
  - [Finding Controls by Label](#finding-controls-by-label)
  - [Finding Controls Near Text](#finding-controls-near-text)
  - [Clicking Controls by Label](#clicking-controls-by-label)
  - [Finding Controls by Automation ID](#finding-controls-by-automation-id)
- [Window Operations](#window-operations)
  - [Finding Windows by Title](#finding-windows-by-title)
- [Screen Recording](#screen-recording)
  - [Starting Screen Recording](#starting-screen-recording)
  - [Stopping Screen Recording](#stopping-screen-recording)
- [Global Operations](#global-operations)
  - [Sleep](#sleep)
  - [Show Desktop](#show-desktop)
  - [Get Screen Size](#get-screen-size)
  - [Take Screenshot](#take-screenshot)
  - [Generic Locator](#generic-locator)

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
Library    RPALite

*** Settings ***
Library    RPALite    ocr_engine=paddleocr  # Use PaddleOCR
```

You can also configure other parameters like debug mode, languages, and step pause interval:

```robotframework
*** Settings ***
Library    RPALite    debug_mode=${TRUE}    languages=["en", "fr"]    step_pause_interval=5
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
- Screen recording
- Control finding and automation
- Waiting mechanisms for text and images

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

To wait for the application to fully launch before proceeding:

```robotframework
Run Command    notepad.exe    noblock=${FALSE}
```

### Finding an Application

You can find an application with the following code:

```robotframework
${app} =    Find Application    .*Notepad
```

The `Find Application` keyword supports finding an application through the following parameters:

- `title`: A string representing the regular expression that the application's title must match,
- `class_name`: A string representing the class name of the application. To find the class name of an application, you can use the [Accessibility Insights for Windows tool](https://accessibilityinsights.io/) to view it.

Example with class name:

```robotframework
${app} =    Find Application    title=${NONE}    class_name=Notepad
```

### Closing an Application

You can close an application with the following code:

```robotframework
${app} =    Find Application    .*Notepad
Close App    ${app}
```

You can also force quit an application:

```robotframework
Close App    ${app}    force_quit=${TRUE}
```

### Maximizing a Window

To maximize a program, you first need to locate the program, then call the `Maximize Window` method:

```robotframework
${app} =     Find Application    .*Notepad
Maximize Window    ${app}
```

You can also specify a window title pattern:

```robotframework
Maximize Window    ${app}    window_title_pattern=Document - Notepad
```

## Mouse Operations

### Getting Cursor Position

```robotframework
${position} =    Get Cursor Position
Log    Cursor position: ${position}
```

### Moving Mouse

```robotframework
Mouse Move    100    200    # Move to absolute position (x=100, y=200)
```

### Moving Mouse to Text

```robotframework
Move Mouse To The Middle Of Text    Text to move to
```

### Clicking by Coordinates

```robotframework
Click By Position    100    200    # Left click at position (100, 200)
```

You can also specify button and double-click parameters:

```robotframework
# Right click
Click By Position    100    200    button=right

# Double left click
Click By Position    100    200    double_click=${TRUE}
```

### Clicking by Text

```robotframework
Click By Text    Click me    # Clicks on text that matches "Click me"
```

With right-click or double-click:

```robotframework
# Right click on text
Click By Text    Click me    button=right

# Double left click on text
Click By Text    Click me    double_click=${TRUE}
```

### Clicking by Image

```robotframework
Click By Image    path/to/image.png    # Clicks on the image
```

With customized clicking:

```robotframework
# Right click on image
Click By Image    path/to/image.png    button=right

# Double left click on image
Click By Image    path/to/image.png    double_click=${TRUE}
```

### Mouse Press and Release

For drag and drop operations:

```robotframework
Mouse Press    button=left
Mouse Move    300    400    # Move while holding button
Mouse Release    button=left
```

### Scrolling

```robotframework
# Scroll up 3 times
Scroll    3

# Scroll down 2 times
Scroll    -2

# Scroll with custom sleep time after
Scroll    1    sleep=1
```

## Keyboard Operations

### Typing Text

```robotframework
Input Text    Hello World    # Types "Hello World" at current cursor position
```

You can also specify how long to wait after inputting text:

```robotframework
Input Text    Hello World    seconds=5
```

### Sending Keys

```robotframework
Send Keys    {ENTER}                 # Sends Enter key
Send Keys    ^c                      # Sends Ctrl+C
Send Keys    %{F4}                   # Sends Alt+F4
Send Keys    +(abc)                  # Sends Shift+ABC (uppercase)
Send Keys    {VK_LWIN down}D{VK_LWIN up}    # Show desktop
```

### Entering Text in Fields

```robotframework
Enter In Field    Username    john.doe
Enter In Field    Password    secret123
```

### Getting Field Value

```robotframework
${value} =    Get Text Field Value    Username
Log    The username is: ${value}
```

### Validating Text

```robotframework
Validate Text Exists    Welcome to RPALite
```

You can disable throwing exceptions:

```robotframework
${result} =    Validate Text Exists    Welcome to RPALite    throw_exception_when_failed=${FALSE}
```

### Finding Text Positions

```robotframework
${positions} =    Find Text Positions    Text to find
Log    Text positions: ${positions}
Log    First matched text position: ${positions}[0]
```

With exact matching:

```robotframework
${positions} =    Find Text Positions    Text to find    exact_match=${TRUE}
```

### Waiting for Text to Appear

```robotframework
${position} =    Wait Until Text Shown    Text to wait for    timeout=30
```

### Waiting for Text to Disappear

```robotframework
Wait Until Text Disappears    Text to wait for disappearing    timeout=30
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

## Image Operations

### Finding an Image

```robotframework
${location} =    Find Image Location    path/to/image.png
```

Searching within another image:

```robotframework
${location} =    Find Image Location    path/to/needle.png    path/to/haystack.png
```

### Finding All Image Instances

```robotframework
${locations} =    Find All Image Locations    path/to/image.png
FOR    ${loc}    IN    @{locations}
    Log    Found image at: ${loc}
END
```

Note: If no matches are found, this function will return an empty list, not None.

### Waiting for an Image

```robotframework
${location} =    Wait Until Image Shown    path/to/image.png    timeout=30
```

## Control Operations

### Finding Controls by Label

```robotframework
${control} =    Find Control By Label    Label text
Log    Control position: ${control}
```

### Finding Controls Near Text

```robotframework
${control} =    Find Control Near Text    Text near control
Log    Control position: ${control}
```

### Clicking Controls by Label

```robotframework
Click Control By Label    Button label
```

With right-click or double-click:

```robotframework
Click Control By Label    Button label    button=right    double_click=${TRUE}
```

### Finding Controls by Automation ID

For Windows applications:

```robotframework
${app} =    Find Application    Notepad
${control} =    Find Control    ${app}    class_name=Edit    title=Text Editor
```

Clicking a specific part of the control:

```robotframework
Click Control    ${app}    class_name=Edit    click_position=center
```

Click position options include 'center', 'center-left', 'center-right', 'left', and 'right'.

## Window Operations

### Finding Windows by Title

```robotframework
${windows} =    Find Windows By Title    Window Title
```

## Screen Recording

### Starting Screen Recording

```robotframework
${video_path} =    Start Screen Recording    output.avi
```

Without specifying a file path:

```robotframework
${video_path} =    Start Screen Recording
Log    Recording to: ${video_path}
```

With custom frame rate:

```robotframework
${video_path} =    Start Screen Recording    fps=30
```

### Stopping Screen Recording

```robotframework
${final_path} =    Stop Screen Recording
Log    Recording saved to: ${final_path}
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
```

With file saving and multi-monitor options:

```robotframework
# Take screenshot and save to file
Take Screenshot    filename=screenshot.png

# Capture all screens
${all_screens_image} =    Take Screenshot    all_screens=${TRUE}
```

### Generic Locator

RPALite provides a generic `Locate` function that can find objects in different ways:

```robotframework
# Locate by text
${position} =    Locate    OK Button

# Locate by image path
${position} =    Locate    image:path/to/image.png

# Locate by automation ID (Windows only)
${app} =    Find Application    Notepad
${position} =    Locate    automateId:EditControl    app=${app}
```

You can also use the general-purpose `Click` function that works with these locators:

```robotframework
# Click on text
Click    OK Button

# Click on image
Click    image:path/to/image.png

# Click by automation ID
${app} =    Find Application    Notepad
Click    automateId:EditControl    app=${app}
```
