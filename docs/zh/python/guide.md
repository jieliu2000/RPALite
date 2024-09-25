# 在 Python 中使用 RPALite

可以通过以下链接直接跳转到对应的部分：

- [安装 RPALite](#安装)
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
  - [获取字段的值](#获取字段的值)
  - [根据字段名称模拟输入文本](#根据字段名称模拟输入文本)
  - [校验文本是否存在](#校验文本是否存在)
  - [获取文本的坐标](#获取文本的坐标)
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

也可以通过下面的方法在下载代码以后进行安装：

### 下载代码后安装

首先将项目克隆到本地：

```bash
git clone https://github.com/jieliu2000/RPALite.git
```

之后进入 rpalite 目录后 build 并安装

```bash
cd RPALite
```

安装 build 所需要的库：

```bash
pip install -r requirements.txt
```

进行项目构建：

```bash
python -m build
```

之后使用 pip 进行安装。以下代码为一个示例，_实际使用时请把 XXX 改成对应的实际版本号_。

```bash
cd dist
pip install rpalite-XXX.tar.gz
```

## 创建 RPALite 对象

由于 RPALite 被声明为一个类，**在所有操作开始之前，你需要首先创建 RPALite 对象**：

```python
from RPALite import RPALite
rpalite = RPALite()
```

RPALite 的构造函数包含多个可选参数：

- `debug_mode`: 布尔值，默认值为 False。如果为 True，则 RPALite 会输出调试信息，在一些需要图像识别的地方，会显示图像中元素的标记等
- `step_pause_interval`: 整数。含义为每个模拟操作后等待的时间。默认值为 **3** 秒。这个值不能设定为 0，这主要是因为在鼠标或者键盘模拟动作以后，Windows 或者你所操作的程序本身也需要一点时间进行响应，否则程序出问题的可能性会大大增加。
- `languages`: 字符串列表，表示 RPALite 会使用哪些语言来进行 OCR 识别。默认值为 `["en"]`也就是英语，你可以通过传入其他语言代码来指定使用其他语言的键盘输入。关于支持的语言列表，可以参考[EasyOCR 文档中的语言列表](https://www.jaided.ai/easyocr)

本文档之后的示例中使用的 rpalite 对象，都假设已经执行了创建对象的代码。

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

得到的坐标为元组形式(x, y)，例如 (10, 20)表示横坐标为 10，纵坐标为 20。注意，这里的坐标是相对于屏幕左上角的坐标。

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

如同上面代码所示，input_text 函数不会自动换行，你需要自己添加换行符。
如果你需要在某个特定位置输入文本，可以首先用 mouse_move 函数移动到指定位置，然后再输入文本。

### 获取字段的值

示例：

```python
value = rpalite.get_text_field_value("Field name")
print(f"Value of field: {value}")
```

RPALite 使用 OCR 和 AI 图像技术识别对应的字段和字段的值。由于这种识别并不总是准确的，这个函数可能会有一定的概率出现误差或者错误。在实际的使用中，需要根据实际情况进行调整。

### 根据字段名称模拟输入文本

示例：

```python
rpalite.enter_in_field("Field name", "New value")
```

`enter_in_field`函数有两个参数：

- `field_name`: 字符串，表示字段的名称
- `text`: 字符串，表示要输入的文本

RPALite 使用 OCR 和 AI 图像技术识别对应的字段和文本框位置。同样的，存在一定概率出现误差或者错误。在实际的使用中，需要根据实际情况进行调整。

### 发送按键

你可以使用以下代码模拟按下键盘上的某个键：

```python
rpalite.send_keys("{VK_LWIN down}D{VK_LWIN up}")
```

### 校验文本是否存在

示例：

```python
rpalite.validate_text_exists("Text to check")
```

你可能注意到在上面的代码中`validate_text_exists`并没有返回值，这是因为如果文本不存在，该函数会直接抛出一个 AssertionError 异常。

RPALite 使用 OCR 技术来识别文本，这种识别并不总是准确的，而且我们的识别都只是识别单行文本，所以一方面这个函数可能会识别出错，另一方面无法识别多行文本。你在实际的使用中，需要根据实际情况进行调整。

### 获取文本的坐标

示例：

```python
positions = rpalite.find_text_positions("Text to find")
print(f"Text positions: {positions}")
print(f"First matched text position: {positions[0]}")
```

注意`find_text_positions`函数返回的是一个列表，表示文本在屏幕上的位置。其中列表中的每一项都是一个结构为 (x, y, width, height) 的元组，表示文本在屏幕上的位置。x, y 表示文本的左上角坐标，width 和 height 分别表示识别出来的文本的宽度和高度。

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

`sleep`函数接受一个整数参数，表示 RPALite 需要休眠多少秒。这个参数是可选的，默认值是 rpalite 对象的`step_pause_interval`属性。

我们前面讲过，这个值不能设定为 0，因为在鼠标或者键盘模拟动作以后，Windows 或者你所操作的程序本身也需要一点时间进行响应，否则程序出问题的可能性会大大增加。如果你将这个参数设定为 0，RPALite 会直接使用`step_pause_interval`的值。如果你将 RPALite 的`step_pause_interval`属性设定为 0，那么 RPALite 会直接跳过休眠操作。

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
- `filename`: 字符串，表示要保存的截图文件的路径。如果这个参数被指定了，那么 RPALite 会将截图保存到指定的文件中。这个字符串为 None 时，RPALite 不会保存截图。无论是否指定了这个参数，`take_screenshot`函数都会返回一个 PIL 图像对象。

### 录屏

### 开始录屏

```python
rpalite.start_screen_recording()
```

`start_screen_recording`函数会启动录屏功能，并开始录制屏幕。它有两个可选参数：

- `target_avi_file_path`: 字符串，表示要保存录屏文件（AVI 格式）的路径。如果这个参数被指定了，那么 RPALite 会将录屏内容保存到指定的文件中。这个字符串为 None 时，RPALite 会在临时目录中创建一个临时文件来保存录屏内容。无论是否指定了这个参数，`start_screen_recording`函数都会返回一个字符串，表示录屏文件的路径。
- `fps`: 整数，表示录屏的帧率。默认值为 10。

start_screen_recording 目前只支持保存为 AVI 格式的录屏文件。

### 结束录屏

```python
rpalite.stop_screen_recording()
```
