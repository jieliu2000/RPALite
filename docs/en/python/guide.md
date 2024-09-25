# Using RPALite in Python

You can directly navigate to each section via the following links:

- [Installation](#installation)
- [Creating an RPALite Object](#creating-an-rpalite-object)
  - [debug_mode](#debug_mode)
  - [step_pause_interval](#step_pause_interval)
  - [languages](#languages)
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
- [Keyboard/Text Operations](#keyboard-text-operations)
  - [Inputting Text at Current Cursor Position](#inputting-text-at-current-cursor-position)
  - [Getting Value of a Field](#getting-value-of-a-field)
  - [Simulating Input Text Based on Field Name](#simulating-input-text-based-on-field-name)
  - [Sending Keys](#sending-keys)
- [Clipboard Operations](#clipboard-operations)
  - [Getting Clipboard Text](#getting-clipboard-text)
  - [Copying Text to Clipboard](#copying-text-to-clipboard)
- [Global Operations](#global-operations)
  - [Sleeping](#sleeping)
  - [Getting Screen Size](#getting-screen-size)
  - [Taking Screenshots](#taking-screenshots)
  - [Screen Recording](#screen-recording)
    - [Starting Screen Recording](#starting-screen-recording)
    - [Stopping Screen Recording](#stopping-screen-recording)

## Installation

You can install RPALite through pip:

```bash
pip install RPALite
```

Alternatively, you can also install after downloading the source code:

### Installing After Downloading the Code

First, clone the project locally:

```bash
git clone https://github.com/jieliu2000/RPALite.git
```

Then navigate to the rpalite directory and build and install it:

```bash
cd RPALite
```

Install the libraries required for building:

```bash
pip install -r requirements.txt
```

Build the project:

```bash
python -m build
```

Finally, install using pip. Below is an example, _replace XXX with the actual version number when using_:

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

The constructor of RPALite includes several optional parameters:

- `debug_mode`: Boolean, default is False. If set to True, RPALite will output debug information and mark elements in images during recognition.
- `step_pause_interval`: Integer, represents the waiting time after each simulated action. The default value is **3** seconds. This value cannot be set to 0 because Windows or the program you're operating needs some time to respond to mouse or keyboard actions, otherwise the likelihood of issues increases significantly.
- `languages`: A list of strings indicating which languages RPALite will use for OCR recognition. The default is `["en"]`, meaning English. You can specify other languages by passing their respective codes.

In subsequent examples within this document, it's assumed that the `rpalite` object has been created.

## Application Operations

### Launching an Application

You can launch an application using `run_command`:

```python
rpalite.run_command("notepad.exe")
```

The `run_command` function takes two arguments:

- `command`: A string representing the command to start the application, could be the path to an executable file or a command that the operating system can execute.
- `noblock`: An optional boolean, defaults to True, meaning RPALite won't wait for the application to finish launching. If set to False, RPALite waits until the application is fully launched.

### Finding an Application

You can use the following code to find an application:

```python
app = rpalite.find_application(".*Notepad")
```

The `find_application` function supports finding applications via these parameters:

- `title`: A string representing the regular expression that matches the application's title.
- `classname`: A string representing the class name of the application. To find the class name of an application, you can use the [Accessibility Insights for Windows tool](https://accessibilityinsights.io/).

### Closing an Application

After obtaining an application instance with `find_application`, you can close an application using:

```python
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```

### Maximizing a Window

You can maximize an application window using:

```python
app = rpalite.find_application(".*Notepad")
rpalite.maximize_window(app)
```

## Simulating Mouse Actions

RPALite supports multiple types of mouse simulation operations, such as clicking text, images, and coordinates.

### Getting Current Cursor Position

Example:

```python
position = rpalite.get_cursor_position()
print(f"Current mouse position: {position}")
```

The returned coordinates are in tuple form (x, y), for example (10, 20) means the horizontal coordinate is 10 and the vertical coordinate is 20. Note that the coordinates are relative to the top-left corner of the screen.

### Moving Mouse to Specified Position

Example:

```python
rpalite.mouse_move(10, 20)
```

Parameters are horizontal coordinate x and vertical coordinate y. The top-left corner of the screen is (0, 0).

### Clicking by Coordinates

Example:

```python
rpalite.click_by_position(10, 20)
```

The first parameter is the horizontal coordinate x, and the second parameter is the vertical coordinate y. The top-left corner of the screen is (0, 0).

### Clicking Text

You can click text using the following code:

```python
rpalite.click_by_text("Text to click")
```

### Clicking an Image

You can click an image using the following code:

```python
rpalite.click_by_image("path/to/image.png")
```

RPALite uses OpenCV to search for the corresponding image on the screen and clicks the top-left corner if found.

## Keyboard/Text Operations

### Inputting Text at Current Cursor Position

You can input a piece of text using the following code:

```python
rpalite.input_text("This is a demo using RPALite.\n")
```

### Getting Value of a Field

Example:

```python
value = rpalite.get_text_field_value("Field name")
print(f"Value of field: {value}")
```

RPALite uses OCR and AI image technology to recognize the corresponding field and its value. Since this recognition isn't always accurate, there may be a chance of errors or inaccuracies. Adjustments might be needed based on actual usage.

### Simulating Input Text Based on Field Name

Example:

```python
rpalite.enter_in_field("Field name", "New value")
```

The `enter_in_field` function takes two parameters:

- `field_name`: A string representing the name of the field.
- `text`: A string representing the text to input.

RPALite uses OCR and AI image technology to recognize the corresponding field and the position of the text box. Similarly, there may be a chance of errors or inaccuracies. Adjustments might be needed based on actual usage.

### Sending Keys

You can simulate pressing a key on the keyboard using the following code:

```python
rpalite.send_keys("{VK_LWIN down}D{VK_LWIN up}")
```

## Clipboard Operations

### Getting Clipboard Text

Example:

```python
text = rpalite.get_clipboard_text()
print(f"Clipboard content: {text}")
```

### Copying Text to Clipboard

Example:

```python
rpalite.copy_text_to_clipboard("This is a demo using RPALite.")
```

## Global Operations

### Sleeping

Example:

```python
rpalite.sleep(5)
```

The `sleep` function accepts an integer parameter indicating how many seconds RPALite should sleep. This parameter is optional; the default value is the `step_pause_interval` attribute of the rpalite object.

As mentioned earlier, this value cannot be set to 0 because Windows or the program being operated needs some time to respond to mouse or keyboard actions; otherwise, the likelihood of issues increases significantly. If you set this parameter to 0, RPALite will use the value of `step_pause_interval`. If `step_pause_interval` is set to 0, RPALite will skip the sleep operation.

### Getting Screen Size

Example:

```python
size = rpalite.get_screen_size()
print(f"Screen size: {size}")
```

The `get_screen_size` function returns a tuple representing the dimensions of the screen. For example, (1920, 1080) indicates a screen width of 1920 pixels and height of 1080 pixels.

### Taking Screenshots

Example:

```python
pil_image = rpalite.take_screenshot()
```

The `take_screenshot` function returns a PIL image object representing the current screenshot. It has two optional parameters:

- `all_screens`: A boolean, default is False, meaning only the current screen is captured. If set to True, all screens are captured. This parameter is useful in multi-monitor environments.
- `filename`: A string representing the path where the screenshot should be saved. If specified, RPALite saves the screenshot to the specified file. If not specified, RPALite does not save the screenshot. Regardless of whether this parameter is specified, the `take_screenshot` function returns a PIL image object.

### Screen Recording

### Starting Screen Recording

```python
rpalite.start_screen_recording()
```

The `start_screen_recording` function starts screen recording. It has two optional parameters:

- `target_avi_file_path`: A string representing the path where the recorded video (in AVI format) should be saved. If specified, RPALite saves the recording to the specified file. If not specified, RPALite creates a temporary file in the temp directory to save the recording. Regardless of whether this parameter is specified, the `start_screen_recording` function returns a string representing the path of the recording file.
- `fps`: An integer representing the frame rate of the recording. The default value is 10.

### Stopping Screen Recording

```python
rpalite.stop_screen_recording()
```
