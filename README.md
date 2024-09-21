# RPALite - Open Source RPA (Robotic Process Automation) Library for Python and Robot Framework

| [English](README.md) | [中文](README-zh.md) |

## Introduction

RPALite is an open source RPA (Robotic Process Automation) library. You can use RPALite via Python or [Robot Framework](https://robotframework.org/) to process various automation tasks.

_In the current version , RPALite only supports Windows platform , we plan to add support for mac and Linux in the future version , but currently rpalite only supports Windows platform._

## Features

Currently RPALite supports the following operations on Windows platform:

- Start an application
- Find an application by its name or ClassName.
- Close an application
- Mouse clicks on specific text
- Locating textboxes, controls, windows based on its labels or the text inside the control
- Text input
- Support coordinate-based mouse click
- Left, right mouse button clicks, with single click or double click mode
- Supports finding the coordinates of a Windows control based on the control's name, class, or Automation ID.
- Support for image-based positioning. You can pass RPALite a picture of a part of the screen to return the coordinates of the part of the screen that corresponds to the picture.

## Documentation

We currently provide a copy of the Robot Framework documentation in English, which you can access [online documentation](https://jieliu2000.github.io/RPALite/docs/robot/RPALite.html). If you want to open it locally, you can open the [Robot Framework help documentation under the project folder](docs/robot/RPALite.html) directly

## Performance Optimization

The most time-consuming operations in RPALite is OCR, for which we utilize [EasyOCR](https://github.com/JaidedAI/EasyOCR). EasyOCR runs more efficiently on computers with a dedicated GPU and CUDA support, so if you find that RPALite is running slowly, consider switching to a computer with a dedicated GPU and CUDA support and installing the corresponding PyTorch version.

## Quick Start

### Installation

You can install RPALite via pip:

```bash
pip install RPALite
```

You can also install RPALite from source following the instructions below.

#### Installation from source

Since we are still in the early stages of the project, you need to clone the project and install it after build. First clone the project to you computer:

```
git clone https://github.com/jieliu2000/RPALite.git
```

After that, go into the rpalite directory and build and install it

```
cd RPALite
```

Install the libraries needed for build:

```
pip install -r requirements.txt
```

Perform a project build:

```
python -m build
```

After that use pip to install. Below command line is an example. Please make sure to replace the xxx to the actual version number:

```
cd dist
pip install rpalite-xxx.tar.gz
```

### Usage Examples

You can use RPALite with Python or Robot Framework, the following section shows some examples:

#### Python example

This is an example for using RPALite in Python to open Notepad and input some text:

```python
from RPALite import RPALite
rpalite = RPALite()

# Press Windows + D to show the desktop
rpalite.send_keys("{VK_LWIN down}D{VK_LWIN up}")

# Open Notepad and type a text
rpalite.run_command("notepad.exe")
rpalite.input_text("This is a demo using RPALite.\n")

# Find the notepad application and close it
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)

```

#### Robot Framework example

This is an example for using RPALite in Robot Framework script to open Notepad and input some text:

```robotframework
*** Settings ***
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

## Programming Guide

As mentioned earlier, you can use RPALite with Python or Robot Framework. In the following sections, we will introduce how to use RPALite in Python and Robot Framework. Since Robot Framework is built upon Python at its core, the content of these two sections is essentially the same.

### Python

### Creating an RPALite Object

You can create an RPALite object with the following code:

```python
from RPALite import RPALite
rpalite = RPALite()
```

The RPALite constructor includes several optional parameters:

- `debug_mode`: A boolean value, defaulting to False. If set to True, RPALite outputs debug information and displays markings of elements within images during recognition.
- `step_pause_interval`: An integer representing the duration to wait after each simulated action. The default value is 3 seconds. This value cannot be set to 0 because both Windows and the program being controlled need some time to respond after mouse or keyboard actions; otherwise, the likelihood of issues increases.
- `languages`: A list of strings indicating which languages RPALite should use for OCR recognition. The default value is `["en"]`, meaning English. You can specify other languages by passing their respective language codes.

### Application Operations

#### Launching an Application

You can launch an application with the following code:

```python
rpalite.run_command("notepad.exe")
```

The `run_command` function has two parameters:

- `command`: A string representing the command to start the application.
- `noblock`: An optional boolean value, defaulting to True, meaning RPALite will not wait for the application to finish launching before returning. If set to False, RPALite waits until the application is fully launched.

#### Finding an Application

You can find an application with the following code:

```python
app = rpalite.find_application(".*Notepad")
```

`find_application` supports finding an application through the following parameters:

- `title`: A string representing the regular expression for matching the application's title.
- `classname`: A string representing the application's class name. To find an application's class name, you can use the [Accessibility Insights for Windows tool](https://accessibilityinsights.io/).

#### Closing an Application

After obtaining an application instance using the `find_application` function, you can close an application with the following code:

```python
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```

#### Maximizing a Window

You can maximize an application window with the following code:

```python
app = rpalite.find_application(".*Notepad")
rpalite.maximize_window(app)
```

### Simulating Mouse Actions

RPALite supports various mouse simulation operations, such as clicking text, images, and coordinates.

#### Clicking by Coordinates

You can click a coordinate with the following code:

```python
rpalite.click_by_position(10, 20)
```

The first parameter is the X-axis coordinate, and the second is the Y-axis coordinate. The top-left corner of the screen is (0, 0).

#### Clicking Text

You can click text with the following code:

```python
rpalite.click_by_text("Text to click")
```

#### Clicking an Image

You can click an image with the following code:

```python
rpalite.click_by_image("path/to/image.png")
```

RPALite uses OpenCV to search for the corresponding image on the screen and clicks the top-left corner of the image if found.

### Simulating Keyboard Actions

#### Typing Text

You can type a piece of text with the following code:

```python
rpalite.input_text("This is a demo using RPALite.\n")
```

#### Sending Keys

You can simulate pressing a key on the keyboard with the following code:

```python
rpalite.send_keys("{VK_LWIN down}D{VK_LWIN up}")
```

### Robot Framework

Refer to our [Robot Framework Help Documentation](docs/robot/RPALite.html) for a list and descriptions of the operations supported by RPALite.

### Importing the RPALite Library

You can import the RPALite library with the following code:

```robotframework
Library    RPALite
```

### Application Operations

#### Launching an Application

You can launch an application with the following code:

```robotframework
Run Command    notepad.exe
```

#### Finding an Application

You can find an application with the following code:

```robotframework
${app} =    Find Application    .*Notepad
```

#### Closing an Application

You can close an application with the following code:

```robotframework
${app} =    Find Application    .*Notepad
Close App
```

### Simulating Mouse Actions

RPALite supports various mouse simulation operations, such as clicking text, images, and coordinates.

#### Clicking by Coordinates

You can click a coordinate with the following code:

```robotframework
Click By Position    10    20
```

#### Clicking Text

```robotframework
Click By Text    Text to click
```

#### Clicking an Image

You can click an image with the following code:

```robotframework
Click By Image    path/to/image.png
```

### Simulating Keyboard Actions

#### Typing Text

You can input a piece of text with the following code:

```robotframework
Input Text    This is a demo using RPALite.
```

#### Sending Keys

You can simulate pressing a key on the keyboard with the following code:

```robotframework
Send Keys    {VK_LWIN down}D{VK_LWIN up}
```

## Contributor Guidelines

If you wish to contribute code to RPALite, you can directly create a Pull Request. Please ensure that your coding style is consistent with the existing codebase and that your changes pass all tests in the tests directory. Additionally, make sure to update unit tests for any new or modified code.

- GitHub Repository: https://github.com/jieliu2000/RPALite
- GitCode Repository: https://gitcode.com/jieliu2000/rpalite
