# main.py
import tkinter as tk
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils import Utils
from device_manager import DeviceManager
from adb_manager import ADBManager
from fastboot_manager import FastbootManager
from ui_manager import UIManager

def main():
    """主函数"""
    # 检查ADB工具是否可用
    if not Utils.check_tool_available():
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showerror("错误", "未找到ADB工具！")
        sys.exit(1)
    
    # 创建主窗口
    root = tk.Tk()
    
    # 初始化管理器
    device_manager = DeviceManager()
    adb_manager = ADBManager()
    fastboot_manager = FastbootManager()
    
    # 创建界面管理器
    ui_manager = UIManager(root, adb_manager, fastboot_man # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()
