# 在 Robot Framework 中使用 RPALite 库

## 目录

- [简介](#简介)
- [平台支持](#平台支持)
- [OCR 引擎配置](#OCR引擎配置)
- [安装](#安装)
- [基本用法](#基本用法)
- [高级功能](#高级功能)
- [故障排除](#故障排除)
- [应用程序操作](#应用程序操作)
  - [启动应用程序](#启动应用程序)
  - [查找应用程序](#查找应用程序)
  - [关闭应用程序](#关闭应用程序)
  - [最大化窗口](#最大化窗口)
- [鼠标操作](#鼠标操作)
  - [获取当前光标位置](#获取当前光标位置)
  - [移动鼠标](#移动鼠标)
  - [移动鼠标到文本](#移动鼠标到文本)
  - [按坐标点击](#按坐标点击)
  - [点击文本](#点击文本)
  - [点击图像](#点击图像)
  - [鼠标按下和释放](#鼠标按下和释放)
  - [滚动](#滚动)
- [键盘操作](#键盘操作)
  - [输入文本](#输入文本)
  - [发送按键](#发送按键)
  - [在字段中输入文本](#在字段中输入文本)
  - [获取字段值](#获取字段值)
  - [验证文本存在](#验证文本存在)
  - [查找文本位置](#查找文本位置)
  - [等待文本出现](#等待文本出现)
  - [等待文本消失](#等待文本消失)
- [剪贴板操作](#剪贴板操作)
  - [获取剪贴板文本](#获取剪贴板文本)
  - [复制文本到剪贴板](#复制文本到剪贴板)
- [图像操作](#图像操作)
  - [查找图像](#查找图像)
  - [查找所有图像实例](#查找所有图像实例)
  - [等待图像出现](#等待图像出现)
- [控件操作](#控件操作)
  - [通过标签查找控件](#通过标签查找控件)
  - [在文本附近查找控件](#在文本附近查找控件)
  - [通过标签点击控件](#通过标签点击控件)
  - [通过自动化 ID 查找控件](#通过自动化ID查找控件)
- [窗口操作](#窗口操作)
  - [通过标题查找窗口](#通过标题查找窗口)
- [屏幕录制](#屏幕录制)
  - [开始屏幕录制](#开始屏幕录制)
  - [停止屏幕录制](#停止屏幕录制)
- [全局操作](#全局操作)
  - [休眠](#休眠)
  - [显示桌面](#显示桌面)
  - [获取屏幕尺寸](#获取屏幕尺寸)
  - [屏幕截图](#屏幕截图)
  - [通用定位器](#通用定位器)

## 简介

本指南提供了如何在 Robot Framework 中使用 RPALite 的详细信息。RPALite 是一个开源的 RPA（机器人流程自动化）库，允许您通过 Robot Framework 自动化各种任务。

### 平台支持

RPALite 目前支持以下平台：

- **Windows**：包括 UI 控件在内的完整自动化支持
- **macOS（开发中）**：基本自动化支持正在开发中

### OCR 引擎配置

RPALite 支持两种 OCR 引擎：

- **EasyOCR**（默认）
  - 支持更多开箱即用的语言
  - 更适合通用 OCR
  - 模型体积较大
- **PaddleOCR**
  - 对中文文本识别效果更好
  - 模型体积更小
  - 推理速度更快

您可以在初始化 RPALite 时配置 OCR 引擎：

```robotframework
*** Settings ***
Library    RPALite    ocr_engine=easyocr    # 使用EasyOCR（默认）

*** Settings ***
Library    RPALite    ocr_engine=paddleocr  # 使用PaddleOCR
```

您还可以配置其他参数，如调试模式、语言和步骤暂停间隔：

```robotframework
*** Settings ***
Library    RPALite    debug_mode=${TRUE}    languages=["zh", "en"]    step_pause_interval=5
```

### 安装

使用 pip 安装 RPALite：

```bash
pip install RPALite
```

### 基本用法

以下是使用 Robot Framework 和 RPALite 的简单示例：

```robotframework
*** Settings ***
Library    RPALite

*** Test Cases ***
测试记事本
    Send Keys    {VK_LWIN down}D{VK_LWIN up}
    Run Command    notepad.exe
    ${app} =     Find Application    .*记事本
    Maximize Window    ${app}
    Input Text    这是一个使用RPALite的演示。
    Close App    ${app}
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
- 文本和图像等待机制

### 故障排除

如果遇到任何问题：

1. 确保您拥有所需的权限
2. 检查日志文件中的错误消息
3. 验证所有依赖项已正确安装
4. 对于 Windows，如果需要，请确保您拥有管理员权限

## 应用程序操作

### 启动应用程序

您可以使用以下代码启动应用程序：

```robotframework
Run Command    notepad.exe
```

要等待应用程序完全启动后再继续：

```robotframework
Run Command    notepad.exe    noblock=${FALSE}
```

### 查找应用程序

您可以使用以下代码查找应用程序：

```robotframework
${app} =    Find Application    .*记事本
```

`Find Application`关键字支持通过以下参数查找应用程序：

- `title`：一个字符串，表示应用程序标题必须匹配的正则表达式
- `class_name`：一个字符串，表示应用程序的类名。要查找应用程序的类名，您可以使用[Accessibility Insights for Windows 工具](https://accessibilityinsights.io/)。

使用类名的示例：

```robotframework
${app} =    Find Application    title=${NONE}    class_name=Notepad
```

### 关闭应用程序

您可以使用以下代码关闭应用程序：

```robotframework
${app} =    Find Application    .*记事本
Close App    ${app}
```

您还可以强制关闭应用程序：

```robotframework
Close App    ${app}    force_quit=${TRUE}
```

### 最大化窗口

要最大化程序，您首先需要定位程序，然后调用`Maximize Window`方法：

```robotframework
${app} =     Find Application    .*记事本
Maximize Window    ${app}
```

您还可以指定窗口标题模式：

```robotframework
Maximize Window    ${app}    window_title_pattern=文档 - 记事本
```

## 鼠标操作

### 获取当前光标位置

```robotframework
${position} =    Get Cursor Position
Log    光标位置：${position}
```

### 移动鼠标

```robotframework
Mouse Move    100    200    # 移动到绝对位置(x=100, y=200)
```

### 移动鼠标到文本

```robotframework
Move Mouse To The Middle Of Text    要移动到的文本
```

### 按坐标点击

```robotframework
Click By Position    100    200    # 在位置(100, 200)处左键点击
```

您还可以指定按钮和双击参数：

```robotframework
# 右键点击
Click By Position    100    200    button=right

# 左键双击
Click By Position    100    200    double_click=${TRUE}
```

### 点击文本

```robotframework
Click By Text    点击我    # 点击匹配"点击我"的文本
```

使用右键点击或双击：

```robotframework
# 右键点击文本
Click By Text    点击我    button=right

# 左键双击文本
Click By Text    点击我    double_click=${TRUE}
```

### 点击图像

```robotframework
Click By Image    path/to/image.png    # 点击图像
```

自定义点击：

```robotframework
# 右键点击图像
Click By Image    path/to/image.png    button=right

# 左键双击图像
Click By Image    path/to/image.png    double_click=${TRUE}
```

### 鼠标按下和释放

用于拖放操作：

```robotframework
Mouse Press    button=left
Mouse Move    300    400    # 按住按钮移动
Mouse Release    button=left
```

### 滚动

```robotframework
# 向上滚动3次
Scroll    3

# 向下滚动2次
Scroll    -2

# 滚动后自定义等待时间
Scroll    1    sleep=1
```

## 键盘操作

### 输入文本

```robotframework
Input Text    你好世界    # 在当前光标位置键入"你好世界"
```

您还可以指定输入文本后等待多长时间：

```robotframework
Input Text    你好世界    seconds=5
```

### 发送按键

```robotframework
Send Keys    {ENTER}                 # 发送回车键
Send Keys    ^c                      # 发送Ctrl+C
Send Keys    %{F4}                   # 发送Alt+F4
Send Keys    +(abc)                  # 发送Shift+ABC（大写）
Send Keys    {VK_LWIN down}D{VK_LWIN up}    # 显示桌面
```

### 在字段中输入文本

```robotframework
Enter In Field    用户名    john.doe
Enter In Field    密码    secret123
```

### 获取字段值

```robotframework
${value} =    Get Text Field Value    用户名
Log    用户名是：${value}
```

### 验证文本存在

```robotframework
Validate Text Exists    欢迎使用RPALite
```

您可以禁用抛出异常：

```robotframework
${result} =    Validate Text Exists    欢迎使用RPALite    throw_exception_when_failed=${FALSE}
```

### 查找文本位置

```robotframework
${positions} =    Find Text Positions    要查找的文本
Log    文本位置：${positions}
Log    第一个匹配的文本位置：${positions}[0]
```

使用精确匹配：

```robotframework
${positions} =    Find Text Positions    要查找的文本    exact_match=${TRUE}
```

### 等待文本出现

```robotframework
${position} =    Wait Until Text Shown    等待出现的文本    timeout=30
```

### 等待文本消失

```robotframework
Wait Until Text Disappears    等待消失的文本    timeout=30
```

## 剪贴板操作

### 获取剪贴板文本

```robotframework
${text} =    Get Clipboard Text
Log    剪贴板内容：${text}
```

### 复制文本到剪贴板

```robotframework
Copy Text To Clipboard    这是一个测试
```

## 图像操作

### 查找图像

```robotframework
${location} =    Find Image Location    path/to/image.png
```

在另一个图像中搜索：

```robotframework
${location} =    Find Image Location    path/to/needle.png    path/to/haystack.png
```

### 查找所有图像实例

```robotframework
${locations} =    Find All Image Locations    path/to/image.png
FOR    ${loc}    IN    @{locations}
    Log    在以下位置找到图像：${loc}
END
```

注意：如果未找到匹配项，此函数将返回空列表，而不是 None。

### 等待图像出现

```robotframework
${location} =    Wait Until Image Shown    path/to/image.png    timeout=30
```

## 控件操作

### 通过标签查找控件

```robotframework
${control} =    Find Control By Label    标签文本
Log    控件位置：${control}
```

### 在文本附近查找控件

```robotframework
${control} =    Find Control Near Text    控件附近的文本
Log    控件位置：${control}
```

### 通过标签点击控件

```robotframework
Click Control By Label    按钮标签
```

使用右键点击或双击：

```robotframework
Click Control By Label    按钮标签    button=right    double_click=${TRUE}
```

### 通过自动化 ID 查找控件

对于 Windows 应用程序：

```robotframework
${app} =    Find Application    记事本
${control} =    Find Control    ${app}    class_name=Edit    title=文本编辑器
```

点击控件的特定部分：

```robotframework
Click Control    ${app}    class_name=Edit    click_position=center
```

点击位置选项包括'center'（中心）、'center-left'（中左）、'center-right'（中右）、'left'（左）和'right'（右）。

## 窗口操作

### 通过标题查找窗口

```robotframework
${windows} =    Find Windows By Title    窗口标题
```

## 屏幕录制

### 开始屏幕录制

```robotframework
${video_path} =    Start Screen Recording    output.avi
```

不指定文件路径：

```robotframework
${video_path} =    Start Screen Recording
Log    录制到：${video_path}
```

自定义帧率：

```robotframework
${video_path} =    Start Screen Recording    fps=30
```

### 停止屏幕录制

```robotframework
${final_path} =    Stop Screen Recording
Log    录制保存到：${final_path}
```

## 全局操作

### 休眠

```robotframework
Sleep    5    # 休眠5秒
```

### 显示桌面

```robotframework
Show Desktop
```

### 获取屏幕尺寸

```robotframework
${size} =    Get Screen Size
Log    屏幕尺寸：${size}
```

### 屏幕截图

```robotframework
${image} =    Take Screenshot
```

使用文件保存和多显示器选项：

```robotframework
# 截屏并保存到文件
Take Screenshot    filename=screenshot.png

# 捕获所有屏幕
${all_screens_image} =    Take Screenshot    all_screens=${TRUE}
```

### 通用定位器

RPALite 提供了一个通用的`Locate`函数，可以以不同方式查找对象：

```robotframework
# 通过文本定位
${position} =    Locate    确定按钮

# 通过图像路径定位
${position} =    Locate    image:path/to/image.png

# 通过自动化ID定位（仅限Windows）
${app} =    Find Application    记事本
${position} =    Locate    automateId:EditControl    app=${app}
```

您还可以使用通用的`Click`函数，该函数适用于这些定位器：

```robotframework
# 点击文本
Click    确定按钮

# 点击图像
Click    image:path/to/image.png

# 通过自动化ID点击
${app} =    Find Application    记事本
Click    automateId:EditControl    app=${app}
```
