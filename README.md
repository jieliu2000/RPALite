# RPALite - Open Source RPA (Robotic Process Automation) Library for Python and Robot Framework

| [English](README.md) | [中文](README-zh.md) |

## Introduction

RPALite is an open source RPA (Robotic Process Automation) library. You can use RPALite via Python or [Robot Framework](https://robotframework.org/) to process various automation tasks.

_In the current version , RPALite only supports Windows platform , we plan to add support for mac and Linux in the future version , but currently rpalite only supports Windows platform._

## Features

Currently RPALite supports the following operations on Windows platform:

* Start an application
* Find an application by its name or ClassName.
* Close an application
* Mouse clicks on specific text
* Locating textboxes, controls, windows based on its labels or the text inside the control
* Text input
* Support coordinate-based mouse click
* Left, right mouse button clicks, with single click or double click mode
* Supports finding the coordinates of a Windows control based on the control's name, class, or Automation ID.
* Support for image-based positioning. You can pass RPALite a picture of a part of the screen to return the coordinates of the part of the screen that corresponds to the picture.

## Documentation

We currently provide a copy of the Robot Framework documentation in English, which you can access [online documentation](https://jieliu2000.github.io/RPALite/docs/robot/RPALite.html). If you want to open it locally, you can open the [Robot Framework help documentation under the project folder](docs/robot/RPALite.html) directly

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
Library    RPALite

*** Test Cases ***
Notepad Test
    Send Keys    {VK_LWIN down}D{VK_LWIN up}
    Run Command    notepad.exe
    Input Text    This is a demo using RPALite.
    ${app} = Find Application    .*Notepad
    Close App    ${app}
```