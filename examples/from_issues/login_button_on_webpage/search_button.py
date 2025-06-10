from RPALite import RPALite
from PIL import Image
import threading
import time

def show_image():
    """在单独线程中显示图片"""
    try:
        image = Image.open("1.png")
        image.show()
        print("图片已显示")
    except FileNotFoundError:
        print("找不到1.png文件")
    except Exception as e:
        print(f"显示图片时出错: {e}")

# 在新线程中显示图片，避免阻塞主线程
image_thread = threading.Thread(target=show_image)
image_thread.daemon = True  # 设为守护线程，主程序结束时自动关闭
image_thread.start()

# 稍等一下让图片有时间显示
time.sleep(1)

# 使用RPALite的click_by_text进行点击
rpa = RPALite( languages=["en", "ch_sim"])
try:
    # 这里您可以根据需要修改要点击的文本
    rpa.wait_until_text_shown("登录")
    rpa.click_by_text("登录")  # 示例：点击包含"搜索"文本的元素
    print("点击操作已执行")
except Exception as e:
    print(f"点击操作失败: {e}")

