# Python 编程指南

## 目录

- [简介](#简介)
- [平台支持](#平台支持)
- [OCR 引擎配置](#OCR引擎配置)
- [安装](#安装)
- [基本用法](#基本用法)
- [高级功能](#高级功能)
- [故障排除](#故障排除)
- [创建 RPALite 对象](#创建-RPALite-对象)
- [程序应用操作](#程序应用操作)
  - [启动应用](#启动应用)
  - [查找应用](#查找应用)
  - [关闭应用](#关闭应用)
  - [最大化窗口](#最大化窗口)
- [模拟鼠标操作](#模拟鼠标操作)
  - [得到当前光标坐标](#得到当前光标坐标)
  - [移动鼠标到指定位置](#移动鼠标到指定位置)
  - [移动鼠标到文本](#移动鼠标到文本)
  - [按坐标点击](#按坐标点击)
  - [点击文本](#点击文本)
  - [点击图片](#点击图片)
  - [鼠标按下和释放](#鼠标按下和释放)
  - [滚轮操作](#滚轮操作)
- [键盘/文本操作](#键盘文本操作)
  - [在当前光标位置输入文本](#在当前光标位置输入文本)
  - [发送按键](#发送按键)
  - [获取字段的值](#获取字段的值)
  - [根据字段名称模拟输入文本](#根据字段名称模拟输入文本)
  - [校验文本是否存在](#校验文本是否存在)
  - [获取文本的坐标](#获取文本的坐标)
  - [等待文本出现](#等待文本出现)
  - [等待文本消失](#等待文本消失)
- [剪贴板操作](#剪贴板操作)
  - [获取剪贴板文本](#获取剪贴板文本)
  - [把文本复制到剪贴板](#把文本复制到剪贴板)
- [图像操作](#图像操作)
  - [查找图像](#查找图像)
  - [查找所有图像实例](#查找所有图像实例)
  - [等待图像出现](#等待图像出现)
- [控件操作](#控件操作)
  - [通过标签查找控件](#通过标签查找控件)
  - [查找文本附近的控件](#查找文本附近的控件)
  - [通过标签点击控件](#通过标签点击控件)
  - [通过自动化 ID 查找控件](#通过自动化ID查找控件)
- [窗口操作](#窗口操作)
  - [通过标题查找窗口](#通过标题查找窗口)
- [屏幕录制](#屏幕录制)
  - [开始录屏](#开始录屏)
  - [结束录屏](#结束录屏)
- [全局操作](#全局操作)
  - [休眠](#休眠)
  - [获取屏幕尺寸](#获取屏幕尺寸)
  - [屏幕截图](#屏幕截图)
  - [显示桌面](#显示桌面)
  - [通用定位器](#通用定位器)

## 简介

本指南详细介绍了如何在 Python 中使用 RPALite。RPALite 是一个开源的 RPA（机器人流程自动化）库，允许您通过 Python 自动化各种任务。

### 平台支持

RPALite 目前支持以下平台：

- **Windows**：完整的自动化支持，包括 UI 控件
- **macOS (开发中)**：基本自动化支持已实现，但有一些限制

## OCR 引擎配置

RPALite 支持两种 OCR 引擎：

- **EasyOCR**（默认）
  - 支持更多语言
  - 更适合通用 OCR 任务
  - 模型体积较大
- **PaddleOCR**
  - 对中文文本识别效果更好
  - 模型体积更小
  - 推理速度更快

你可以在初始化 RPALite 时配置 OCR 引擎：

```python
# 使用 EasyOCR（默认）
rpalite = RPALite(ocr_engine="easyocr")

# 使用 PaddleOCR
rpalite = RPALite(ocr_engine="paddleocr")
```

### 安装

要安装 RPALite，请使用 pip：

```bash
pip install RPALite
```

### 基本用法

以下是一个使用 RPALite 的简单 Python 示例：

```python
from RPALite import RPALite

# 初始化 RPALite
rpalite = RPALite()

# 显示桌面
rpalite.show_desktop()

# 运行记事本并输入文本
rpalite.run_command("notepad.exe")
rpalite.input_text("Hello from RPALite!")

# 查找并关闭记事本
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```

### 高级功能

RPALite 提供了许多高级功能，包括：

- 图像识别
- OCR（光学字符识别）支持多种引擎
- 窗口管理
- 剪贴板操作
- 键盘和鼠标控制
- 屏幕录制
- 控件查找和自动化
- 文本和图像的等待机制

### 故障排除

如果遇到任何问题：

1. 确保您具有所需的权限
2. 检查日志文件中的错误信息
3. 验证所有依赖项是否正确安装
4. 对于 Windows，如果需要，请确保您具有管理员权限

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
- `ocr_engine`: 字符串，默认值为 "easyocr"。指定使用的 OCR 引擎（可以是 "easyocr" 或 "paddleocr"）
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
- `class_name`: 字符串，表示应用类名。如果需要查找应用的类名，可以使用 [Accessibility Insights for Windows 工具](https://accessibilityinsights.io/)查看

### 关闭应用

通过 find_application 函数获取到 application 实例后，你可以使用以下代码关闭一个应用：

```python
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```

你也可以通过设置 `force_quit` 参数为 True 来强制关闭应用：

```python
rpalite.close_app(app, force_quit=True)
```

### 最大化窗口

你可以使用以下代码最大化一个应用窗口：

```python
app = rpalite.find_application(".*Notepad")
rpalite.maximize_window(app)
```

如果你想最大化应用中的特定窗口，可以指定窗口标题模式：

```python
rpalite.maximize_window(app, window_title_pattern="文档 - 记事本")
```

## 模拟鼠标操作

RPALite 支持通过多种鼠标模拟操作，譬如点击文本，点击图片，点击坐标等

### 得到当前光标坐标

```python
position = rpalite.get_cursor_position()
print(f"当前鼠标位置: {position}")
```

得到的坐标为元组形式(x, y)，例如 (10, 20)表示横坐标为 10，纵坐标为 20。注意，这里的坐标是相对于屏幕左上角的坐标。

### 移动鼠标到指定位置

```python
rpalite.mouse_move(10, 20)
```

参数为横坐标 x, 纵坐标 y。屏幕左上角为(0, 0)

### 移动鼠标到文本

```python
rpalite.move_mouse_to_the_middle_of_text("要移动到的文本")
```

这个函数会将鼠标光标移动到屏幕上指定文本的中心位置。

### 按坐标点击

```python
rpalite.click_by_position(10, 20)
```

其中第一个参数为横坐标 x，第二个参数为纵坐标 y。屏幕左上角为(0, 0)

你也可以指定按钮和双击参数：

```python
# 右键点击
rpalite.click_by_position(10, 20, button='right')

# 左键双击
rpalite.click_by_position(10, 20, double_click=True)
```

### 点击文本

你可以使用以下代码点击文本：

```python
rpalite.click_by_text("要点击的文本")
```

你也可以指定按钮（左键或右键）以及是否双击：

```python
# 右键点击文本
rpalite.click_by_text("要点击的文本", button='right')

# 左键双击文本
rpalite.click_by_text("要点击的文本", double_click=True)
```

### 点击图片

你可以使用以下代码点击图片：

```python
rpalite.click_by_image("图片/路径.png")
```

你也可以指定按钮（左键或右键）以及是否双击：

```python
# 右键点击图片
rpalite.click_by_image("图片/路径.png", button='right')

# 左键双击图片
rpalite.click_by_image("图片/路径.png", double_click=True)
```

RPALite 会使用 OpenCV 在屏幕上查找对应的图片，如果找到则点击该图片的中心位置。

### 鼠标按下和释放

你可以分别模拟鼠标按钮的按下和释放：

```python
# 按下左键
rpalite.mouse_press(button='left')

# 在按住按钮的同时移动鼠标（用于拖放操作）
rpalite.mouse_move(100, 200)

# 释放左键
rpalite.mouse_release(button='left')
```

### 滚轮操作

你可以使用以下代码操作鼠标滚轮：

```python
# 向上滚动3次
rpalite.scroll(3)

# 向下滚动2次
rpalite.scroll(-2)

# 滚动后自定义等待时间
rpalite.scroll(1, sleep=1)
```

## 键盘/文本操作

### 在当前光标位置输入文本

你可以使用以下代码输入一段文本：

```python
rpalite.input_text("这是使用RPALite的演示。\n")
```

如同上面代码所示，input_text 函数不会自动换行，你需要自己添加换行符。
如果你需要在某个特定位置输入文本，可以首先用 mouse_move 函数移动到指定位置，然后再输入文本。

你也可以指定输入文本后等待的时间：

```python
rpalite.input_text("这是使用RPALite的演示。\n", seconds=5)
```

### 获取字段的值

```python
value = rpalite.get_text_field_value("字段名称")
print(f"字段值: {value}")
```

RPALite 使用 OCR 和 AI 图像技术识别对应的字段和字段的值。由于这种识别并不总是准确的，这个函数可能会有一定的概率出现误差或者错误。在实际的使用中，需要根据实际情况进行调整。

### 根据字段名称模拟输入文本

```python
rpalite.enter_in_field("字段名称", "新值")
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

对于 Windows，它使用 pywinauto 的 send_keys 格式。对于 macOS，它会将按键转换为 keyboard 模块格式。

按键格式示例：

- `"Hello World"` - 输入文本
- `"^c"` - Ctrl+C
- `"%{F4}"` - Alt+F4
- `"{ENTER}"` - 按回车键
- `"+(abc)"` - Shift+ABC（大写）

### 校验文本是否存在

```python
rpalite.validate_text_exists("要检查的文本")
```

你可能注意到在上面的代码中`validate_text_exists`并没有返回值，这是因为如果文本不存在，该函数会直接抛出一个 AssertionError 异常。

你可以通过设置`throw_exception_when_failed`为 False 来禁用异常抛出：

```python
result = rpalite.validate_text_exists("要检查的文本", throw_exception_when_failed=False)
```

RPALite 使用 OCR 技术来识别文本，这种识别并不总是准确的，而且我们的识别都只是识别单行文本，所以一方面这个函数可能会识别出错，另一方面无法识别多行文本。你在实际的使用中，需要根据实际情况进行调整。

### 获取文本的坐标

```python
positions = rpalite.find_text_positions("要查找的文本")
print(f"文本位置: {positions}")
print(f"第一个匹配文本的位置: {positions[0]}")
```

注意`find_text_positions`函数返回的是一个列表，表示文本在屏幕上的位置。其中列表中的每一项都是一个结构为 (x, y, width, height) 的元组，表示文本在屏幕上的位置。x, y 表示文本的左上角坐标，width 和 height 分别表示识别出来的文本的宽度和高度。

你可以使用精确匹配来提高准确性：

```python
positions = rpalite.find_text_positions("要查找的文本", exact_match=True)
```

### 等待文本出现

你可以等待文本在屏幕上出现，并设置超时时间：

```python
position = rpalite.wait_until_text_shown("要等待的文本", timeout=30)
```

这将最多等待 30 秒，直到文本出现。如果找到文本，将返回文本的位置；如果在超时时间内未找到，将引发 AssertionError。

### 等待文本消失

类似地，你可以等待文本从屏幕上消失：

```python
rpalite.wait_until_text_disappears("要等待消失的文本", timeout=30)
```

## 剪贴板操作

### 获取剪贴板文本

```python
text = rpalite.get_clipboard_text()
print(f"剪贴板内容: {text}")
```

### 把文本复制到剪贴板

```python
rpalite.copy_text_to_clipboard("这是使用RPALite的演示。")
```

## 图像操作

### 查找图像

你可以在屏幕上查找图像：

```python
location = rpalite.find_image_location("图片/路径.png")
```

或者直接使用 PIL Image 对象：

```python
from PIL import Image
img = Image.open("图片/路径.png")
location = rpalite.find_image_location(img)
```

你也可以在另一个图像中搜索：

```python
location = rpalite.find_image_location("要查找的图片.png", "在此图片中查找.png")
```

### 查找所有图像实例

要查找屏幕上某个图像的所有实例：

```python
locations = rpalite.find_all_image_locations("图片/路径.png")
for loc in locations:
    print(f"在以下位置找到图像: {loc}")
```

如果未找到匹配项，此函数将返回空列表，而不是 None。

### 等待图像出现

你可以等待图像在屏幕上出现：

```python
location = rpalite.wait_until_image_shown("图片/路径.png", timeout=30)
```

## 控件操作

### 通过标签查找控件

```python
control = rpalite.find_control_by_label("标签文本")
print(f"控件位置: {control}")
```

### 查找文本附近的控件

```python
control = rpalite.find_control_near_text("控件附近的文本")
print(f"控件位置: {control}")
```

### 通过标签点击控件

```python
rpalite.click_control_by_label("按钮标签")
```

使用右键点击或双击：

```python
rpalite.click_control_by_label("按钮标签", button="right", double_click=True)
```

### 通过自动化 ID 查找控件

对于 Windows 应用程序，你可以使用其自动化属性查找控件：

```python
app = rpalite.find_application("记事本")
control = rpalite.find_control(app, class_name="Edit", title="文本编辑器")
```

然后你可以点击控件的特定部分：

```python
rpalite.click_control(app, class_name="Edit", click_position="center")
```

点击位置选项包括'center'（中心）、'center-left'（中左）、'center-right'（中右）、'left'（左侧）和'right'（右侧）。

## 窗口操作

### 通过标题查找窗口

```python
windows = rpalite.find_windows_by_title("窗口标题")
```

## 屏幕录制

### 开始录屏

你可以将屏幕录制到 AVI 文件：

```python
video_path = rpalite.start_screen_recording("输出.avi")
```

如果你不指定文件路径，RPALite 将在临时目录中创建一个随机文件：

```python
video_path = rpalite.start_screen_recording()
print(f"录制到: {video_path}")
```

你也可以指定每秒帧数：

```python
video_path = rpalite.start_screen_recording(fps=30)
```

### 结束录屏

```python
final_path = rpalite.stop_screen_recording()
print(f"录制保存到: {final_path}")
```

## 全局操作

### 休眠

```python
rpalite.sleep(5)
```

`sleep`函数接受一个整数参数，表示 RPALite 需要休眠多少秒。这个参数是可选的，默认值是 rpalite 对象的`step_pause_interval`属性。

我们前面讲过，这个值不能设定为 0，因为在鼠标或者键盘模拟动作以后，Windows 或者你所操作的程序本身也需要一点时间进行响应，否则程序出问题的可能性会大大增加。如果你将这个参数设定为 0，RPALite 会直接使用`step_pause_interval`的值。如果你将 RPALite 的`step_pause_interval`属性设定为 0，那么 RPALite 会直接跳过休眠操作。

### 显示桌面

```python
rpalite.show_desktop()
```

### 获取屏幕尺寸

```python
size = rpalite.get_screen_size()
print(f"屏幕尺寸: {size}")
```

`get_screen_size`函数返回一个元组，表示屏幕的尺寸。例如 (1920, 1080) 表示屏幕宽度为 1920 像素，高度为 1080 像素。

### 屏幕截图

```python
pil_image = rpalite.take_screenshot()
```

`take_screenshot`函数返回一个 PIL 图像对象，表示当前屏幕的截图。它有两个可选的参数：

- `all_screens`: 布尔值，默认值为 False，意思是只截取当前屏幕的截图。如果为 True，则截取所有屏幕的截图。这个参数在多屏幕环境中很有用。
- `filename`: 字符串，表示要保存的截图文件的路径。如果这个参数被指定了，那么 RPALite 会将截图保存到指定的文件中。这个字符串为 None 时，RPALite 不会保存截图。

```python
# 截图并保存到文件
rpalite.take_screenshot(filename="截图.png")

# 捕获所有屏幕
rpalite.take_screenshot(all_screens=True)
```

### 通用定位器

RPALite 提供了一个通用的`locate`函数，可以以不同方式查找对象：

```python
# 通过文本定位
position = rpalite.locate("确定按钮")

# 通过图像路径定位
position = rpalite.locate("image:图片/路径.png")

# 通过自动化ID定位（仅Windows）
app = rpalite.find_application("记事本")
position = rpalite.locate("automateId:EditControl", app=app)
```

你也可以使用通用的`click`函数，它可以与这些定位器一起工作：

```python
# 点击文本
rpalite.click("确定按钮")

# 点击图像
rpalite.click("image:图片/路径.png")

# 通过自动化ID点击
rpalite.click("automateId:EditControl", app=app)
```
