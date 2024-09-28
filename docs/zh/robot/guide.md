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
