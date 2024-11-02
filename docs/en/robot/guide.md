# Using the RPALite Library in Robot Framework

You can directly jump to the corresponding section via the following links:

- [Installation](#installation)
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

## Installation

You can install RPALite through pip:

```bash
pip install RPALite
```

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

As mentioned earlier, this value cannot be set to 0 because after simulating mouse or keyboard actions, Windows or the program being operated also needs some time to respond. Otherwise, the likelihood of issues occurring will greatly increase. If you set this parameter to 0, RPALite will directly use the value of `step_pause_interval`. If you set the `step_pause_interval` attribute of RPALite to 0, RPALite will skip the sleep operation.

### Showing the Desktop

```robotframework
Show Desktop
```

### Getting Screen Dimensions

```robotframework
${size} = Get Screen Size
${log_message} =  Format String    Screen size: {0} ${size}
Log    ${log_message}
```

The `get_screen_size` function returns a tuple representing the screen dimensions. For example, (1920, 1080) indicates a screen width of 1920 pixels and a height of 1080 pixels.

### Taking a Screenshot

```robotframework
${pil_image} =    Take Screenshot
```

The `Take Screenshot` function returns a PIL image object representing a screenshot of the current screen. It has two optional parameters:

- `all_screens`: A Boolean value, defaulting to False, which means taking a screenshot of only the current screen. If set to True, it takes a screenshot of all screens. This parameter is very useful in multi-monitor environments.
- `filename`: A string representing the path to save the screenshot file. If this parameter is specified, RPALite will save the screenshot to the designated file. When this string is None, RPALite does not save the screenshot. Regardless of whether this parameter is specified, the `Take Screenshot` function always returns a PIL image object.

### Screen Recording

#### Starting a Screen Recording

```robotframework
Start Screen Recording
```

The `Start Screen Recording` function initiates screen recording and starts capturing the screen. It has two optional parameters:

- `target_avi_file_path`: A string representing the path to save the screen recording file (in AVI format). If this parameter is specified, RPALite will save the recording content to the designated file. When this string is None, RPALite creates a temporary file in the temporary directory to store the recording content. Regardless of whether this parameter is specified, the `Start Screen Recording` function always returns a string representing the path of the recording file.
- `fps`: An integer representing the frame rate of the recording. The default value is 10.

`start_screen_recording` currently only supports saving recordings in AVI format.

#### Stopping a Screen Recording

```robotframework
Stop Screen Recording
```