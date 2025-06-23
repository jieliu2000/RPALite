# RPALite Linux支持改进

本文档详细说明了RPALite在Linux平台上的功能改进和使用方法。

## 主要改进

### 1. 键盘输入支持完善
- **问题**: 原版本缺少Linux平台的`send_keys`方法实现
- **解决**: 添加了完整的Linux键盘输入支持，包括：
  - 特殊键映射（如ENTER、ESC、功能键等）
  - 修饰键组合（Ctrl+C、Alt+F4等）
  - 中文输入支持

### 2. 鼠标操作改进
- **问题**: 导入冲突和平台兼容性问题
- **解决**: 修复了鼠标相关方法的导入问题：
  - `mouse_move()` - 鼠标移动
  - `click_by_position()` - 位置点击
  - `scroll()` - 滚轮滚动

### 3. 窗口管理增强
- **问题**: Linux窗口管理功能不完善
- **解决**: 改进了窗口管理功能：
  - 多工具支持（xdotool + wmctrl）
  - 错误恢复机制
  - 超时处理
  - 详细的调试信息

### 4. 桌面环境适配
- **问题**: show_desktop()方法只支持单一工具
- **解决**: 添加了多种桌面环境支持：
  - GNOME/Unity快捷键
  - KDE快捷键
  - 通用wmctrl命令
  - 自动回退机制

### 5. 应用程序查找改进
- **问题**: 应用查找功能有限
- **解决**: 增强了应用程序查找：
  - xdotool和wmctrl双重支持
  - 更好的错误处理
  - 中文提示信息

### 6. 控件查找适配
- **问题**: find_control()方法仅支持Windows
- **解决**: 为Linux添加了基于OCR的控件查找替代方案

## 系统要求

### 必需的系统工具
```bash
# Ubuntu/Debian
sudo apt-get install xdotool wmctrl

# CentOS/RHEL
sudo yum install xdotool wmctrl

# Fedora
sudo dnf install xdotool wmctrl

# Arch Linux
sudo pacman -S xdotool wmctrl
```

### Python依赖
```bash
pip install python-xlib keyboard mouse pyautogui
```

## 使用方法

### 1. 依赖检查
运行依赖检查脚本：
```bash
python3 check_linux_deps.py
```

### 2. 基本使用
```python
from RPALite import RPALite

# 初始化（建议开启调试模式）
rpalite = RPALite(debug_mode=True)

# 显示桌面
rpalite.show_desktop()

# 键盘输入
rpalite.send_keys("^c")  # Ctrl+C
rpalite.send_keys("{ENTER}")  # 回车键
rpalite.input_text("中文输入测试")

# 鼠标操作
rpalite.click_by_position(100, 100)
rpalite.scroll(3)  # 向上滚动

# 应用管理
app = rpalite.find_application("firefox")
if app:
    rpalite.maximize_window(app)
    rpalite.close_app(app)
```

### 3. 综合示例
运行Linux综合示例：
```bash
python3 examples/python/linux_comprehensive_example.py
```

## 已知限制

1. **UI自动化**: Linux缺乏类似Windows的UI自动化API，某些高级控件操作需要通过OCR实现
2. **权限要求**: 某些操作可能需要特定权限，建议将用户添加到input组
3. **桌面环境**: 在Wayland环境下可能需要切换到X11或设置相应环境变量
4. **发行版差异**: 不同Linux发行版的工具可用性可能不同

## 故障排除

### 1. 权限问题
```bash
# 将用户添加到input组
sudo usermod -a -G input $USER
# 重新登录生效
```

### 2. Wayland环境问题
```bash
# 设置环境变量强制使用X11
export GDK_BACKEND=x11
```

### 3. 工具缺失
```bash
# 检查工具是否安装
which xdotool wmctrl
# 如果缺失，按照系统要求章节安装
```

### 4. Python包问题
```bash
# 安装或更新相关包
pip install --upgrade keyboard mouse pyautogui python-xlib
```

## 桌面环境兼容性

| 桌面环境 | 窗口管理 | 键盘输入 | 鼠标操作 | 截图 |
|---------|---------|---------|---------|------|
| GNOME | ✓ | ✓ | ✓ | ✓ |
| KDE | ✓ | ✓ | ✓ | ✓ |
| XFCE | ✓ | ✓ | ✓ | ✓ |
| Unity | ✓ | ✓ | ✓ | ✓ |
| i3/Sway | 部分 | ✓ | ✓ | ✓ |

## 性能优化建议

1. **启用调试模式**: 在开发阶段启用debug_mode以获得详细信息
2. **合理设置延时**: 根据系统性能调整sleep时间
3. **批量操作**: 尽可能将多个操作组合以减少系统调用
4. **异常处理**: 在生产环境中添加适当的异常处理

## 贡献指南

欢迎为Linux支持贡献代码！请关注：
1. 遵循现有代码风格
2. 添加适当的中文注释和文档
3. 确保跨发行版兼容性
4. 提供测试用例

## 更新日志

- **v1.0**: 初始Linux支持
- **v1.1**: 修复键盘输入缺失问题
- **v1.2**: 改进窗口管理和应用查找
- **v1.3**: 增加桌面环境适配和错误处理
- **v1.4**: 添加依赖检查和综合示例

---

有关更多信息，请参考主要README文档或提交Issue。 