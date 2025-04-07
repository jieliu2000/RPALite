# Python Programming Guide

## Table of Contents

- [Introduction](#introduction)
- [Platform Support](#platform-support)
- [OCR Engine Configuration](#ocr-engine-configuration)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Creating an RPALite Object](#creating-an-rpalite-object)
- [Application Operations](#application-operations)
  - [Launching an Application](#launching-an-application)
  - [Finding an Application](#finding-an-application)
  - [Closing an Application](#closing-an-application)
  - [Maximizing a Window](#maximizing-a-window)
- [Simulating Mouse Actions](#simulating-mouse-actions)
  - [Getting Current Cursor Position](#getting-current-cursor-position)
  - [Moving Mouse to Specified Position](#moving-mouse-to-specified-position)
  - [Moving Mouse to Text](#moving-mouse-to-text)
  - [Clicking by Coordinates](#clicking-by-coordinates)
  - [Clicking Text](#clicking-text)
  - [Clicking an Image](#clicking-an-image)
  - [Mouse Press and Release](#mouse-press-and-release)
  - [Scrolling](#scrolling)
- [Keyboard/Text Operations](#keyboardtext-operations)
  - [Entering Text at Current Cursor Position](#entering-text-at-current-cursor-position)
  - [Retrieving Field Value](#retrieving-field-value)
  - [Inputting Text by Field Name](#inputting-text-by-field-name)
  - [Simulating Key Presses](#simulating-key-presses)
  - [Validating Text Existence](#validating-text-existence)
  - [Getting Coordinates of Text](#getting-coordinates-of-text)
  - [Waiting for Text to Appear](#waiting-for-text-to-appear)
  - [Waiting for Text to Disappear](#waiting-for-text-to-disappear)
- [Clipboard Operations](#clipboard-operations)
  - [Getting Clipboard Text](#getting-clipboard-text)
  - [Copying Text to Clipboard](#copying-text-to-clipboard)
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
  - [Sleeping](#sleeping)
  - [Getting Screen Size](#getting-screen-size)
  - [Taking Screenshot](#taking-screenshot)
  - [Show Desktop](#show-desktop)
  - [Generic Locator](#generic-locator)

## Introduction

This guide provides detailed information on how to use RPALite with Python. RPALite is an open-source RPA (Robotic Process Automation) library that allows you to automate various tasks through Python.

### Platform Support

RPALite currently supports the following platforms:

- **Windows**: Full automation support including UI controls
- **macOS (Under Development)**: Basic automation support is implemented with some limitations

## OCR Engine Configuration

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

```python
# Use EasyOCR (default)
rpalite = RPALite(ocr_engine="easyocr")

# Use PaddleOCR
rpalite = RPALite(ocr_engine="paddleocr")
```

### Installation

To install RPALite, use pip:

```bash
pip install RPALite
```

### Basic Usage

Here's a simple example of using RPALite with Python:

```python
from RPALite import RPALite

# Initialize RPALite
rpalite = RPALite()

# Show desktop
rpalite.show_desktop()

# Run Notepad and input text
rpalite.run_command("notepad.exe")
rpalite.input_text("Hello from RPALite!")

# Find and close Notepad
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
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

# Using RPALite in Python

You can directly navigate to each section via the following links in the Table of Contents.

## Creating an RPALite Object

Since RPALite is declared as a class, **you need to create an RPALite object before performing any operations**:

```python
from RPALite import RPALite
rpalite = RPALite()
```

The constructor of RPALite includes multiple optional parameters:

- `debug_mode`: Boolean, default value is False. If set to True, RPALite will output debug information and mark elements in images during operations that require image recognition.
- `ocr_engine`: String, default value is "easyocr". Specifies which OCR engine to use (either "easyocr" or "paddleocr").
- `step_pause_interval`: Integer. Represents the waiting time after each simulated action. Default value is **3** seconds. This value cannot be set to 0, mainly because the Windows system or the program being operated on also needs some time to respond after simulating mouse or keyboard actions; otherwise, there would be a high likelihood of issues occurring.
- `languages`: List of strings indicating which languages RPALite will use for OCR recognition. The default value is `["en"]` (English). You can specify other languages by passing in their language codes to enable input in those languages. For a list of supported languages, refer to the EasyOCR documentation's language list.

In subsequent examples in this document, assume that the rpalite object has already been created.

## Application Operations

### Launching an Application

You can launch an application using `run_command`:

```python
rpalite.run_command("notepad.exe")
```

The `run_command` function has two parameters:

- `command`: String representing the command to start the application, which could be the path to an executable file or a command that the operating system can execute.
- `noblock`: Optional boolean parameter, default value is True, meaning RPALite does not wait for the application to finish launching but returns immediately. If set to False, RPALite waits for the application to fully launch before returning from `run_command`.

### Finding an Application

You can find an application using the following code:

```python
app = rpalite.find_application(".*Notepad")
```

The `find_application` function supports finding applications through the following parameters:

- `title`: String representing the regular expression that the application title should match,
- `class_name`: String representing the class name of the application. To find the class name of an application, you can use the [Accessibility Insights for Windows tool](https://accessibilityinsights.io/).

### Closing an Application

After obtaining an application instance using the `find_application` function, you can close the application using the following code:

```python
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```

You can also force quit an application by setting the `force_quit` parameter to True:

```python
rpalite.close_app(app, force_quit=True)
```

### Maximizing a Window

You can maximize an application window using the following code:

```python
app = rpalite.find_application(".*Notepad")
rpalite.maximize_window(app)
```

If you want to maximize a specific window within the application, you can specify a window title pattern:

```python
rpalite.maximize_window(app, window_title_pattern="Document - Notepad")
```

## Simulating Mouse Actions

RPALite supports various mouse simulation operations, such as clicking on text, images, or coordinates.

### Getting Current Cursor Position

```python
position = rpalite.get_cursor_position()
print(f"Current mouse position: {position}")
```

The returned coordinates are in tuple form (x, y), for example (10, 20) represents an X-coordinate of 10 and a Y-coordinate of 20. Note that these coordinates are relative to the top-left corner of the screen.

### Moving Mouse to Specified Position

```python
rpalite.mouse_move(10, 20)
```

Parameters are the X-coordinate x and Y-coordinate y. The top-left corner of the screen is (0, 0).

### Moving Mouse to Text

```python
rpalite.move_mouse_to_the_middle_of_text("Text to move to")
```

This function will move the mouse cursor to the center of the specified text on screen.

### Clicking by Coordinates

```python
rpalite.click_by_position(10, 20)
```

The first parameter is the X-coordinate x, and the second parameter is the Y-coordinate y. The top-left corner of the screen is (0, 0).

You can also specify button and double click parameters:

```python
# Right click
rpalite.click_by_position(10, 20, button='right')

# Double left click
rpalite.click_by_position(10, 20, double_click=True)
```

### Clicking Text

You can click on text using the following code:

```python
rpalite.click_by_text("Text to click")
```

You can also specify the button (left or right) and whether to double-click:

```python
# Right click on text
rpalite.click_by_text("Text to click", button='right')

# Double left click on text
rpalite.click_by_text("Text to click", double_click=True)
```

### Clicking an Image

You can click an image using the following code:

```python
rpalite.click_by_image("path/to/image.png")
```

You can also specify the button (left or right) and whether to double-click:

```python
# Right click on image
rpalite.click_by_image("path/to/image.png", button='right')

# Double left click on image
rpalite.click_by_image("path/to/image.png", double_click=True)
```

RPALite uses OpenCV to locate the corresponding image on the screen, and if found, clicks at the center of the image.

### Mouse Press and Release

You can simulate pressing and releasing mouse buttons separately:

```python
# Press left mouse button
rpalite.mouse_press(button='left')

# Move mouse while button is pressed (for drag and drop)
rpalite.mouse_move(100, 200)

# Release left mouse button
rpalite.mouse_release(button='left')
```

### Scrolling

You can scroll the mouse wheel using the following code:

```python
# Scroll up 3 times
rpalite.scroll(3)

# Scroll down 2 times
rpalite.scroll(-2)

# Scroll with custom sleep time after
rpalite.scroll(1, sleep=1)
```

## Keyboard/Text Operations

### Entering Text at Current Cursor Position

You can enter a piece of text using the following code:

```python
rpalite.input_text("This is a demo using RPALite.\n")
```

As shown above, the `input_text` function does not automatically insert line breaks, so you need to add them yourself.
If you need to enter text at a specific location, first use the `mouse_move` function to move to the specified location, then enter the text.

You can also specify how long to wait after inputting text:

```python
rpalite.input_text("This is a demo using RPALite.\n", seconds=5)
```

### Retrieving Field Value

```python
value = rpalite.get_text_field_value("Field name")
print(f"Value of field: {value}")
```

RPALite uses OCR and AI image technology to recognize the corresponding fields and their values. Since this recognition is not always accurate, there may be errors or mistakes with this function. Adjustments based on actual usage are needed.

### Inputting Text by Field Name

```python
rpalite.enter_in_field("Field name", "New value")
```

The `enter_in_field` function has two parameters:

- `field_name`: String representing the name of the field,
- `text`: String representing the text to be entered.

RPALite uses OCR and AI image technology to recognize the position of the corresponding field and text box. Similarly, there is a possibility of errors or mistakes. Adjustments based on actual usage are needed.

### Simulating Key Presses

You can simulate pressing a key on the keyboard using the following code:

```python
rpalite.send_keys("{VK_LWIN down}D{VK_LWIN up}")
```

For Windows, it uses pywinauto's send_keys format. For macOS, it converts the keys to keyboard module format.

Examples of key formats:

- `"Hello World"` - types the text
- `"^c"` - Control+C
- `"%{F4}"` - Alt+F4
- `"{ENTER}"` - Press Enter key
- `"+(abc)"` - Shift+ABC (uppercase)

### Validating Text Existence

```python
rpalite.validate_text_exists("Text to check")
```

You may notice that the `validate_text_exists` function does not return a value. This is because if the text does not exist, the function will directly throw an AssertionError exception.

You can disable throwing exceptions by setting `throw_exception_when_failed` to False:

```python
result = rpalite.validate_text_exists("Text to check", throw_exception_when_failed=False)
```

RPALite uses OCR technology to identify text, which is not always accurate and only recognizes single-line text, so this function might sometimes produce errors or mistakes and cannot recognize multi-line text. Adjustments based on actual usage are needed.

### Getting Coordinates of Text

```python
positions = rpalite.find_text_positions("Text to find")
print(f"Text positions: {positions}")
print(f"First matched text position: {positions[0]}")
```

Note that the `find_text_positions` function returns a list representing the locations of the text on the screen. Each item in the list is a tuple structured as (x, y, width, height), indicating the position of the text on the screen. x and y represent the coordinates of the top-left corner of the text, while width and height represent the width and height of the recognized text.

You can use exact matching to improve accuracy:

```python
positions = rpalite.find_text_positions("Text to find", exact_match=True)
```

### Waiting for Text to Appear

You can wait for text to appear on the screen with a timeout:

```python
position = rpalite.wait_until_text_shown("Text to wait for", timeout=30)
```

This will wait for up to 30 seconds for the text to appear, and will return the position of the text if found, or raise an AssertionError if not found within the timeout.

### Waiting for Text to Disappear

Similarly, you can wait for text to disappear from the screen:

```python
rpalite.wait_until_text_disppears("Text to wait for disappearing", timeout=30)
```

## Clipboard Operations

### Getting Clipboard Text

```python
text = rpalite.get_clipboard_text()
print(f"Clipboard content: {text}")
```

### Copying Text to Clipboard

```python
rpalite.copy_text_to_clipboard("This is a demo using RPALite.")
```

## Image Operations

### Finding an Image

You can find an image on the screen:

```python
location = rpalite.find_image_location("path/to/image.png")
```

Or use a PIL Image object directly:

```python
from PIL import Image
img = Image.open("path/to/image.png")
location = rpalite.find_image_location(img)
```

You can also search within another image:

```python
location = rpalite.find_image_location("path/to/needle.png", "path/to/haystack.png")
```

### Finding All Image Instances

To find all instances of an image on screen:

```python
locations = rpalite.find_all_image_locations("path/to/image.png")
for loc in locations:
    print(f"Found image at: {loc}")
```

### Waiting for an Image

You can wait for an image to appear on screen:

```python
location = rpalite.wait_until_image_shown("path/to/image.png", timeout=30)
```

## Control Operations

### Finding Controls by Label

```python
control = rpalite.find_control_by_label("Label text")
print(f"Control position: {control}")
```

### Finding Controls Near Text

```python
control = rpalite.find_control_near_text("Text near control")
print(f"Control position: {control}")
```

### Clicking Controls by Label

```python
rpalite.click_control_by_label("Button label")
```

With right-click or double-click:

```python
rpalite.click_control_by_label("Button label", button="right", double_click=True)
```

### Finding Controls by Automation ID

For Windows applications, you can find controls using their automation properties:

```python
app = rpalite.find_application("Notepad")
control = rpalite.find_control(app, class_name="Edit", title="Text Editor")
```

You can then click on a specific part of the control:

```python
rpalite.click_control(app, class_name="Edit", click_position="center")
```

Click position options include 'center', 'center-left', 'center-right', 'left', and 'right'.

## Window Operations

### Finding Windows by Title

```python
windows = rpalite.find_windows_by_title("Window Title")
```

## Screen Recording

### Starting Screen Recording

You can record the screen to an AVI file:

```python
video_path = rpalite.start_screen_recording("output.avi")
```

If you don't specify a file path, RPALite will create a random file in a temporary directory:

```python
video_path = rpalite.start_screen_recording()
print(f"Recording to: {video_path}")
```

You can also specify the frames per second:

```python
video_path = rpalite.start_screen_recording(fps=30)
```

### Stopping Screen Recording

```python
final_path = rpalite.stop_screen_recording()
print(f"Recording saved to: {final_path}")
```

## Global Operations

### Sleeping

```python
rpalite.sleep(5)
```

The `sleep` function accepts an integer parameter indicating how many seconds RPALite should sleep. This parameter is optional, with a default value of the `step_pause_interval` property of the rpalite object.

We previously mentioned that this value cannot be set to 0, because the Windows system or the program being controlled also need some time to respond after simulating mouse or keyboard actions; otherwise, the likelihood of issues would increase significantly. If you set this parameter to 0, RPALite uses the value of the `step_pause_interval` attribute. If the `step_pause_interval` attribute of RPALite is set to 0, RPALite skips the sleep operation.

### Show Desktop

```python
rpalite.show_desktop()
```

### Getting Screen Size

```python
size = rpalite.get_screen_size()
print(f"Screen size: {size}")
```

The `get_screen_size` function returns a tuple indicating the dimensions of the screen. For example, (1920, 1080) indicates a screen width of 1920 pixels and a height of 1080 pixels.

### Taking Screenshot

```python
pil_image = rpalite.take_screenshot()
```

The `take_screenshot` function returns a PIL image object representing the current screenshot. It has two optional parameters:

- `all_screens`: Boolean, default value is False, meaning only the current screen is captured. If set to True, all screens are captured. This parameter is useful in multi-monitor environments.
- `filename`: String indicating the path where the screenshot file should be saved. If this parameter is specified, RPALite saves the screenshot to the specified file. If this string is None, RPALite does not save the screenshot.

```python
# Take screenshot and save to file
rpalite.take_screenshot(filename="screenshot.png")

# Capture all screens
rpalite.take_screenshot(all_screens=True)
```

### Generic Locator

RPALite provides a generic `locate` function that can find objects in different ways:

```python
# Locate by text
position = rpalite.locate("OK Button")

# Locate by image path
position = rpalite.locate("image:path/to/image.png")

# Locate by automation ID (Windows only)
app = rpalite.find_application("Notepad")
position = rpalite.locate("automateId:EditControl", app=app)
```

You can also use the general-purpose `click` function that works with these locators:

```python
# Click on text
rpalite.click("OK Button")

# Click on image
rpalite.click("image:path/to/image.png")

# Click by automation ID
rpalite.click("automateId:EditControl", app=app)
```
