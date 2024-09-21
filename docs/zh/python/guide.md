# 在Python中使用RPALite

可以通过以下链接直接跳转到对应的部分：

- [安装RPALite](#安装)
- [创建 RPALite 对象](#创建-RPALite-对象)
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
### 休眠

你可以使用以下代码让RPALite休眠：

```python
rpalite.sleep(5)
```
`sleep`函数接受一个整数参数，表示 RPALite 需要休眠多少秒。这个参数是可选的，默认值是rpalite对象的`step_pause_interval`属性。

我们前面讲过，这个值不能设定为 0，因为在鼠标或者键盘模拟动作以后，Windows 或者你所操作的程序本身也需要一点时间进行响应，否则程序出问题的可能性会大大增加。如果你将这个参数设定为0，RPALite会直接使用`step_pause_interval`的值。如果你将RPALite的`step_pause_interval`属性设定为0，那么RPALite会直接跳过休眠操作。

### 最大化窗口

你可以使用以下代码最大化一个应用窗口：

```python
app = rpalite.find_application(".*Notepad")
rpalite.maximize_window(app)
```

## 模拟鼠标操作

RPALite 支持通过多种鼠标模拟操作，譬如点击文本，点击图片，点击坐标等

### 按坐标点击

你可以使用以下代码点击坐标：

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

## 模拟键盘操作

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
