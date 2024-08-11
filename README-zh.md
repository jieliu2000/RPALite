# RPALite - 用于Python和Robot Framework的开源RPA(Robotic Process Automation，机器人流程自动化)编程库

| [English](README.md) |  [中文](README-zh.md) |

## 介绍

RPALite是一个开源的RPA(Robotic Process Automation，机器人流程自动化)库。你可以通过Python或者[Robot Framework](https://robotframework.org/)使用RPALite，实现各种自动化任务。

*在目前版本，RPALite仅支持Windows平台，我们计划在未来版本中添加对mac和Linux的支持，不过目前rpalite仅支持Windows平台。*

## 特性

目前RPALite在Windows平台支持以下操作：

* 启动应用
* 根据应用名称或者ClassName查找应用
* 关闭应用
* 支持对特定文字的鼠标点击
* 支持基于文本框提示词或者文本框标签的文本框定位和输入
* 支持基于坐标的鼠标点击
* 鼠标点击支持左键，右键，和双击
* 支持基于Windows控件的名称，类，或者Automation ID查找对应控件的坐标
* 支持对基于图片的定位。你可以通过传给RPALite一张屏幕局部的图片返回对应图片部分在屏幕上的坐标

## 文档

目前我们提供一份英文的Robot Framework文档，你可以在[这里](https://jieliu2000.github.io/RPALite/docs/robot/RPALite.html)访问。如果你希望在本地打开，可以直接打开[项目录下的Robot Framework帮助文档](docs/robot/RPALite.html)。

## 快速开始

### 安装

由于目前我们还在项目早期阶段，你需要把项目克隆到本地后进行安装。首先将项目克隆到本地：
```
git clone https://github.com/jieliu2000/RPALite.git
```
之后进入rpalite目录后build并安装
```
cd RPALite
```
安装build所需要的库：
```
pip install -r requirements.txt
```
进行项目构建：
```
python -m build
```
之后使用pip进行安装。以下代码为一个示例，实际使用时请把XXX改成对应的实际版本号。
```
cd dist
pip install rpalite-XXX.tar.gz
```

### 使用示例

你可以使用Python或者Robot Framework使用RPALite。下面部分是一些示例：

#### Python示例

以下为使用RPALite操作Notepad的一个示例：

```python
from RPALite import RPALite
rpalite = RPALite()

# 按下Windows + D以显示桌面
rpalite.send_keys("{VK_LWIN down}D{VK_LWIN up}")

# 运行notepad并输入一段文字
rpalite.run_command("notepad.exe")
rpalite.input_text("This is a demo using RPALite.\n")

# 找到notepad app并关闭
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)

```

#### Robot Framework示例

以下为使用RPALite操作Notepad的一个示例：

```robotframework
*** Settings ***
Library    RPALite

*** Test Cases ***
Test Notepad
    Send Keys    {VK_LWIN down}D{VK_LWIN up}
    Run Command    notepad.exe
    Input Text    This is a demo using RPALite.
    ${app} = Find Application    .*Notepad
    Close App    ${app}
```
