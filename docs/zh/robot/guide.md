# 在 Robot Framework 中使用 RPALite 库

可以通过以下链接直接跳转到对应的部分：

- [安装 RPALite](#安装)
- [导入 RPALite 库](#导入-RPALite-库)
- [程序应用操作](#程序应用操作)
  - [查找应用](#查找应用)
  - [启动应用](#启动应用)
  - [关闭应用](#关闭应用)
  - [最大化窗口](#最大化窗口)
  - [休眠](#休眠)
- [模拟鼠标操作](#模拟鼠标操作)
  - [按坐标点击](#按坐标点击)
  - [点击文本](#点击文本)
  - [点击图片](#点击图片)
- [模拟键盘操作](#模拟键盘操作)
  - [在当前光标位置输入文本](#在当前光标位置输入文本)
  - [发送按键](#发送按键)
- [全局操作](#全局操作)
  - [休眠](#休眠)
  - [获取屏幕尺寸](#获取屏幕尺寸)
  - [屏幕截图](#屏幕截图)
  - [显示桌面](#显示桌面)
  - [录屏](#录屏)
    - [开始录屏](#开始录屏)
    - [结束录屏](#结束录屏)


## 安装

你可以通过 pip 安装 RPALite：

```bash
pip install RPALite
```

## 导入 RPALite 库

你可以通过以下代码导入 RPALite 库：

```robotframework
Library    RPALite
```

## 程序应用操作

### 启动应用

你可以使用以下代码启动一个应用：

```robotframework
Run Command    notepad.exe
```

### 查找应用

你可以使用以下代码查找一个应用：

```robotframework
${app} =    Find Application    .*Notepad
```

`Find Application`支持通过以下参数查找一个应用：

- `title`: 字符串，表示应用标题需要匹配的正则表达式，
- `classname`: 字符串，表示应用类名。如果需要查找应用的类名，可以使用 [Accessibility Insights for Windows 工具](https://accessibilityinsights.io/)查看

### 关闭应用

你可以使用以下代码关闭一个应用：

```robotframework
${app} =    Find Application    .*Notepad
Close App
```

### 最大化窗口

要最大化一个程序，首先你需要找到该程序（参照 [查找应用](#查找应用))，之后调用`Maximize Window`方法：

```robotframework
${app} =     Find Application    .*Notepad
Maximize Window    ${app}
```

````

## 模拟鼠标操作

RPALite 支持通过多种鼠标模拟操作，譬如点击文本，点击图片，点击坐标等

### 按坐标点击

你可以使用以下代码点击坐标：

```robotframework
Click By Position    10    20
````

### 点击文本

```robotframework
Click By Text    Text to click
```

### 点击图片

你可以使用以下代码点击图片：

```robotframework
Click By Image    path/to/image.png
```

## 模拟键盘操作

### 在当前光标位置输入文本

你可以使用以下代码输入一段文本：

```robotframework
Input Text    This is a demo using RPALite.
```

### 发送按键

你可以使用以下代码模拟按下键盘上的某个键：

```robotframework
Send Keys    {VK_LWIN down}D{VK_LWIN up}
```

## 全局操作

### 休眠

你可以使用以下代码模拟程序休眠：

```robotframework
Sleep    1
```

`Sleep`函数接受一个整数参数，表示 RPALite 需要休眠多少秒。这个参数是可选的，默认值是 rpalite 对象的`step_pause_interval`属性。

我们前面讲过，这个值不能设定为 0，因为在鼠标或者键盘模拟动作以后，Windows 或者你所操作的程序本身也需要一点时间进行响应，否则程序出问题的可能性会大大增加。如果你将这个参数设定为 0，RPALite 会直接使用`step_pause_interval`的值。如果你将 RPALite 的`step_pause_interval`属性设定为 0，那么 RPALite 会直接跳过休眠操作。

### 显示桌面

```robotframework
Show Desktop
```

### 获取屏幕尺寸

```robotframework
${size} = Get Screen Size
${log_message} =  Format String    Screen size: {0} ${size}
Log    ${log_message}
```
`get_screen_size`函数返回一个元组，表示屏幕的尺寸。例如 (1920, 1080) 表示屏幕宽度为 1920 像素，高度为 1080 像素。

### 屏幕截图

```robotframework
${pil_image} =    Take Screenshot
```
`Take Screenshot`函数返回一个 PIL 图像对象，表示当前屏幕的截图。它有两个可选的参数：

- `all_screens`: 布尔值，默认值为 False，意思是只截取当前屏幕的截图。如果为 True，则截取所有屏幕的截图。这个参数在多屏幕环境中很有用。
- `filename`: 字符串，表示要保存的截图文件的路径。如果这个参数被指定了，那么 RPALite 会将截图保存到指定的文件中。这个字符串为 None 时，RPALite 不会保存截图。无论是否指定了这个参数，`Take Screenshot`函数都会返回一个 PIL 图像对象。

### 录屏

#### 开始录屏

```robotframework
Start Screen Recording
```

`Start Screen Recording`函数会启动录屏功能，并开始录制屏幕。它有两个可选参数：

- `target_avi_file_path`: 字符串，表示要保存录屏文件（AVI 格式）的路径。如果这个参数被指定了，那么 RPALite 会将录屏内容保存到指定的文件中。这个字符串为 None 时，RPALite 会在临时目录中创建一个临时文件来保存录屏内容。无论是否指定了这个参数，`Start Screen Recording`函数都会返回一个字符串，表示录屏文件的路径。
- `fps`: 整数，表示录屏的帧率。默认值为 10。

start_screen_recording 目前只支持保存为 AVI 格式的录屏文件。

#### 结束录屏
```robotframework
Stop Screen Recording
```