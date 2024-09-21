# 在Python中使用RPALite

可以通过以下链接直接跳转到对应的部分：

- [安装RPALite](#安装)
- [创建 RPALite 对象](#创建-RPALite-对象)
- [程序应用操作](#程序应用操作)
    - [查找应用](#查找应用)
    - [启动应用](#启动应用)
    - [关闭应用](#关闭应用)
    - [最大化窗口](#最大化窗口)
- [模拟鼠标操作](#模拟鼠标操作)
    - [得到当前光标坐标](#得到当前光标坐标)
    - [移动鼠标到指定位置](#移动鼠标到指定位置)
    - [按坐标点击](#按坐标点击)
    - [点击文本](#点击文本)
    - [点击图片](#点击图片)
- [键盘/文本操作](#键盘文本操作)
    - [在当前光标位置输入文本](#在当前光标位置输入文本)
    - [发送按键](#发送按键)
- [剪贴板操作](#剪贴板操作)
    - [获取剪贴板文本](#获取剪贴板文本)
    - [把文本复制到剪贴板](#把文本复制到剪贴板)
- [全局操作](#全局操作)
    - [休眠](#休眠)
    - [获取屏幕尺寸](#获取屏幕尺寸)
    - [屏幕截图](#屏幕截图)
    - [录屏](#录屏)
        - [开始录屏](#开始录屏)
        - [结束录屏](#结束录屏)

## 安装

你可以通过 pip 安装 RPALite：

```bash
pip install RPALite
```

## 创建 RPALite 对象

你可以通过以下代码创建 RPALite 对象：

```python
from RPALite import RPALite
rpalite = RPALite()
```

RPALite 的构造函数包含多个可选参数：

- `debug_mode`: 布尔值，默认值为 False。如果为 True，则 RPALite 会输出调试信息，在一些需要图像识别的地方，会显示图像中元素的标记等
- `step_pause_interval`: 整数。含义为每个模拟操作后等待的时间。默认值为 **3** 秒。这个值不能设定为 0，这主要是因为在鼠标或者键盘模拟动作以后，Windows 或者你所操作的程序本身也需要一点时间进行响应，否则程序出问题的可能性会大大增加。
- `languages`: 字符串列表，表示 RPALite 会使用哪些语言来进行 OCR 识别。默认值为 `["en"]`也就是英语，你可以通过传入其他语言代码来指定使用其他语言的键盘输入。关于支持的语言列表，可以参考[EasyOCR文档中的语言列表](https://www.jaided.ai/easyocr)

## 程序应用操作

### 启动应用

你可以使用`run_command`启动一个应用：

```python
rpalite.run_command("notepad.exe")
```

run_command 函数有两个参数：

- `command`: 字符串，表示要启动的应用的命令，可以是一个可执行文件的路径，也可以是操作系统可以运行的命令
- `noblock`: 可选的布尔值，默认值为 True，也就意味着 RPALite 不会等待应用启动完成，而是直接返回。如果设置为 False，则 RPALite 会等待应用启动完成才会从 run_command 返回。

### 查找应用

你可以使用以下代码查找一个应用：

```python
app = rpalite.find_application(".*Notepad")
```

find_application 支持通过以下参数查找一个应用：

- `title`: 字符串，表示应用标题需要匹配的正则表达式，
- `classname`: 字符串，表示应用类名。如果需要查找应用的类名，可以使用 [Accessibility Insights for Windows 工具](https://accessibilityinsights.io/)查看

### 关闭应用

通过 find_application 函数获取到 application 实例后，你可以使用以下代码关闭一个应用：

```python
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```


### 最大化窗口

你可以使用以下代码最大化一个应用窗口：

```python
app = rpalite.find_application(".*Notepad")
rpalite.maximize_window(app)
```

## 模拟鼠标操作

RPALite 支持通过多种鼠标模拟操作，譬如点击文本，点击图片，点击坐标等

### 得到当前光标坐标

示例：
```python
position = rpalite.get_cursor_position()
print(f"Current mouse position: {position}")
```
得到的坐标为元组形式(x, y)，例如 (10, 20)表示横坐标为10，纵坐标为20。注意，这里的坐标是相对于屏幕左上角的坐标。

### 移动鼠标到指定位置

示例：

```python
rpalite.mouse_move(10, 20)
```
参数为横坐标 x, 纵坐标 y。屏幕左上角为(0, 0)

### 按坐标点击

示例：
```python
rpalite.click_by_position(10, 20)
```

其中第一个参数为 横坐标 x,第二个参数为纵坐标 y。屏幕左上角为(0, 0)

### 点击文本

你可以使用以下代码点击文本：

```python
rpalite.click_by_text("Text to click")
```

### 点击图片

你可以使用以下代码点击图片：

```python
rpalite.click_by_image("path/to/image.png")
```

RPALite 会使用 OpenCV 在屏幕上查找对应的图片，如果找到则点击该图片的左上角。

## 键盘/文本操作

### 在当前光标位置输入文本

你可以使用以下代码输入一段文本：

```python
rpalite.input_text("This is a demo using RPALite.\n")
```

### 发送按键

你可以使用以下代码模拟按下键盘上的某个键：

```python
rpalite.send_keys("{VK_LWIN down}D{VK_LWIN up}")
```
## 剪贴板操作

### 获取剪贴板文本
示例：

```python
text = rpalite.get_clipboard_text()
print(f"Clipboard content: {text}")
```

### 把文本复制到剪贴板
示例：

```python
rpalite.copy_text_to_clipboard("This is a demo using RPALite.")
```


## 全局操作

### 休眠

示例：

```python
rpalite.sleep(5)
```
`sleep`函数接受一个整数参数，表示 RPALite 需要休眠多少秒。这个参数是可选的，默认值是rpalite对象的`step_pause_interval`属性。

我们前面讲过，这个值不能设定为 0，因为在鼠标或者键盘模拟动作以后，Windows 或者你所操作的程序本身也需要一点时间进行响应，否则程序出问题的可能性会大大增加。如果你将这个参数设定为0，RPALite会直接使用`step_pause_interval`的值。如果你将RPALite的`step_pause_interval`属性设定为0，那么RPALite会直接跳过休眠操作。

### 获取屏幕尺寸
示例：

```python
size = rpalite.get_screen_size()
print(f"Screen size: {size}")
```
`get_screen_size`函数返回一个元组，表示屏幕的尺寸。例如 (1920, 1080) 表示屏幕宽度为 1920 像素，高度为 1080 像素。

### 屏幕截图

示例：

```python
pil_image = rpalite.take_screenshot()
```
`take_screenshot`函数返回一个 PIL 图像对象，表示当前屏幕的截图。它有两个可选的参数：

- `all_screens`: 布尔值，默认值为 False，意思是只截取当前屏幕的截图。如果为 True，则截取所有屏幕的截图。这个参数在多屏幕环境中很有用。
- `filename`: 字符串，表示要保存的截图文件的路径。如果这个参数被指定了，那么 RPALite 会将截图保存到指定的文件中。这个字符串为None时，RPALite 不会保存截图。无论是否指定了这个参数，`take_screenshot`函数都会返回一个 PIL 图像对象。

### 录屏

### 开始录屏

```python
rpalite.start_screen_recording()
```

`start_screen_recording`函数会启动录屏功能，并开始录制屏幕。它有两个可选参数：

- `target_avi_file_path`: 字符串，表示要保存录屏文件（AVI格式）的路径。如果这个参数被指定了，那么 RPALite 会将录屏内容保存到指定的文件中。这个字符串为None时，RPALite 会在临时目录中创建一个临时文件来保存录屏内容。无论是否指定了这个参数，`start_screen_recording`函数都会返回一个字符串，表示录屏文件的路径。
- `fps`: 整数，表示录屏的帧率。默认值为 10。

### 结束录屏

```python
rpalite.stop_screen_recording()
```
