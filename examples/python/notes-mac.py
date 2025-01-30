from src.RPALite import RPALite
import time

def main():
    # 初始化 RPALite
    rpa = RPALite(step_pause_interval=1)  # 设置较短的暂停间隔
    
    try:
        # 查找并打开 Notes 应用
        notes_app = rpa.find_application(title="Notes")
        if not notes_app:
            # 如果应用未运行，则启动它
            rpa.run_command("open -a Notes")
            time.sleep(2)  # 等待应用启动
            notes_app = rpa.find_application(title="Notes")
        
        # 激活并最大化窗口
        rpa.maximize_window(notes_app)
        time.sleep(1)
        
        # 创建新笔记 (Command + N)
        rpa.send_keys('#n')  # # 代表 Command 键
        time.sleep(1)
        
        # 输入标题和内容
        rpa.input_text("测试笔记标题")
        rpa.send_keys('{ENTER}')
        time.sleep(0.5)
        
        # 输入正文内容
        content = """这是一个使用 RPALite 自动化创建的笔记。

主要功能：
1. 自动打开 Notes 应用
2. 创建新笔记
3. 输入标题和内容
4. 自动保存

时间：""" + time.strftime("%Y-%m-%d %H:%M:%S")
        
        rpa.input_text(content)
        
        # Notes 会自动保存，等待一下以确保保存完成
        time.sleep(1)
        
        # 关闭笔记窗口 (Command + W)
        rpa.send_keys('#w')
        
        print("笔记创建成功！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        # 可选：关闭 Notes 应用
        # rpa.close_app(notes_app)
        pass

if __name__ == "__main__":
    main()
