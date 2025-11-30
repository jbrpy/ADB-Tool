# config.py
import os

class Config:
    """配置类"""
    # 工具路径配置
    ADB_DIR = "ADB"
    
    # 获取工具路径
    @staticmethod
    def get_adb_path():
        adb_dir = os.path.join(os.path.dirname(__file__), Config.ADB_DIR)
        if os.path.exists(adb_dir):
            for file in os.listdir(adb_dir):
                if file.lower().startswith('adb') and not file.lower().endswith('.dll'):
                    return os.path.join(adb_dir, file)
        return "adb"
    
    @staticmethod
    def get_fastboot_path():
        fastboot_dir = os.path.join(os.path.dirname(__file__), Config.ADB_DIR)
        if os.path.exists(fastboot_dir):
            for file in os.listdir(fastboot_dir):
                if file.lower().startswith('fastboot') and not file.lower().endswith('.dll'):
                    return os.path.join(fastboot_dir, file)
        return "fastboot"
    
    # 界面常量
    WINDOW_TITLE = "ADB/Fastboot 完整工具"
    WINDOW_SIZE = "800x700"
