# Using RPALite in Python

You can directly navigate to each section via the following links:

- [Installation](#installation)
- [Creating an RPALite Object](#creating-an-rpalite-object)
- [Application Operations](#application-operations)
  - [Launching an Application](#launching-an-application)
  - [Finding an Application](#finding-an-application)
  - [Closing an Application](#closing-an-application)
  - [Maximizing a Window](#maximizing-a-window)
- [Simulating Mouse Actions](#simulating-mouse-actions)
  - [Getting Current Cursor Position](#getting-current-cursor-position)
  - [Moving Mouse to Specified Position](#moving-mouse-to-specified-position)
  - [Clicking by Coordinates](#clicking-by-coordinates)
  - [Clicking Text](#clicking-text)
  - [Clicking an Image](#clicking-an-image)
- [Keyboard/Text Operations](#keyboardtext-operations)

  - [Entering Text at Current Cursor Position](#entering-text-at-current-cursor-position)
  - [Retrieving Field Value](#retrieving-field-value)
  - [Inputting Text by Field Name](#inputting-text-by-field-name)
  - [Simulating Key Presses](#simulating-key-presses)
  - [Validating Text Existence](#validating-text-existence)
  - [Getting Coordinates of Text](#getting-coordinates-of-text)

- [Clipboard Operations](#clipboard-operations)
  - [Getting Clipboard Text](#getting-clipboard-text)
  - [Copying Text to Clipboard](#copying-text-to-clipboard)
- [Global Operations](#global-operations)
  - [Sleeping](#sleeping)
  - [Getting Screen Size](#getting-screen-size)
  - [Taking Screenshot](#taking-screenshot)
  - [Screen Recording](#screen-recording)
    - [Starting Screen Recording](#starting-screen-recording)
    - [Stopping Screen Recording](#stopping-screen-recording)

## Installation

You can install RPALite via pip:

```bash
pip install RPALite
```

Alternatively, you can also install it after downloading the code:

### Installation After Downloading the Code

First, clone the project locally:

```bash
git clone https://github.com/jieliu2000/RPALite.git
```

Then navigate into the rpalite directory and build and install it:

```bash
cd RPALite
```

Install the libraries required for building:

```bash
pip install -r requirements.txt
```

Perform the project build:

```bash
python -m build
```

Afterwards, use pip to install it. Below is an example; _replace XXX with the actual version number_ when using.

```bash
cd dist
pip install rpalite-XXX.tar.gz
```

## Creating an RPALite Object

Since RPALite is declared as a class, **you need to create an RPALite object before performing any operations**:

```python
from RPALite import RPALite
rpalite = RPALite()
```

The constructor of RPALite includes multiple optional parameters:

- `debug_mode`: Boolean, default value is False. If set to True, RPALite will output debug information and mark elements in images during operations that require image recognition.
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
- `classname`: String representing the class name of the application. To find the class name of an application, you can use the [Accessibility Insights for Windows tool](https://accessibilityinsights.io/).

### Closing an Application

After obtaining an application instance using the `find_application` function, you can close the application using the following code:

```python
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```

### Maximizing a Window

You can maximize an application window using the following code:

```python
app = rpalite.find_application(".*Notepad")
rpalite.maximize_window(app)
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

### Clicking by Coordinates

```python
rpalite.click_by_position(10, 20)
```

The first parameter is the X-coordinate x, and the second parameter is the Y-coordinate y. The top-left corner of the screen is (0, 0).

### Clicking Text

You can click on text using the following code:

```python
rpalite.click_by_text("Text to click")
```

### Clicking an Image

You can click an image using the following code:

```python
rpalite.click_by_image("path/to/image.png")
```

RPALite uses OpenCV to locate the corresponding image on the screen, and if found, clicks at the top-left corner of the image.

## Keyboard/Text Operations

### Entering Text at Current Cursor Position

You can enter a piece of text using the following code:

```python
rpalite.input_text("This is a demo using RPALite.\n")
```

As shown above, the `input_text` function does not automatically insert line breaks, so you need to add them yourself.
If you need to enter text at a specific location, first use the `mouse_move` function to move to the specified location, then enter the text.

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

### Validating Text Existence

```python
rpalite.validate_text_exists("Text to check")
```

You may notice that the `validate_text_exists` function does not return a value. This is because if the text does not exist, the function will directly throw an AssertionError exception.

RPALite uses OCR technology to identify text, which is not always accurate and only recognizes single-line text, so this function might sometimes produce errors or mistakes and cannot recognize multi-line text. Adjustments based on actual usage are needed.

### Getting Coordinates of Text

```python
positions = rpalite.find_text_positions("Text to find")
print(f"Text positions: {positions}")
print(f"First matched text position: {positions[0]}")
```

Note that the `find_text_positions` function returns a list representing the locations of the text on the screen. Each item in the list is a tuple structured as (x, y, width, height), indicating the position of the text on the screen. x and y represent the coordinates of the top-left corner of the text, while width and height represent the width and height of the recognized text.

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
- `filename`: String indicating the path where the screenshot file should be saved. If this parameter is specified, RPALite saves the screenshot to the specified file. If this string is None, RPALite does not save the screenshot. Regardless of whether this parameter is specified, the `take_screenshot` function returns a PIL image object.

### Screen Recording

#### Starting Screen Recording

```python
rpalite.start_screen_recording()
```

The `start_screen_recording` function starts screen recording and begins recording the screen. It has two optional parameters:

- `target_avi_file_path`: String indicating the path where the screen recording file (AVI format) should be saved. If this parameter is specified, RPALite saves the recording to the specified file. If this string is None, RPALite creates a temporary file in the temporary directory to save the recording. Regardless of whether this parameter is specified, the `start_screen_recording` function returns a string indicating the path of the recording file.
- `fps`: Integer indicating the frame rate of the recording. Default value is 10.

Currently, `start_screen_recording` only supports saving recordings in AVI format.

#### Stopping Screen Recording

```python
rpalite.stop_screen_recording()
```
