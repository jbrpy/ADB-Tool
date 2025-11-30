# adb_manager.py
import threading
import tkinter.simpledialog
import tkinter.filedialog
from utils import Utils

class ADBManager:
    """ADB功能管理类"""
    
    def __init__(self, output_callback=None):
        self.output_callback = output_callback
    
    def set_output_callback(self, callback):
        """设置输出回调函数"""
        self.output_callback = callback
    
    def _output(self, text):
        """输出文本"""
        if self.output_callback:
            self.output_callback(text)
    
    def reboot(self, device_id, mode=""):
        """重启设备"""
        if mode:
            return Utils.run_command(["reboot", mode], device=device_id)
        else:
            return Utils.run_command(["reboot"], device=device_id)
    
    def shell(self, device_id):
        """进入ADB Shell"""
        def run_shell():
            try:
                import subprocess
                if device_id:
                    subprocess.run([Utils.get_adb_path(), "-s", device_id, "shell"])
                else:
                    subprocess.run([Utils.get_adb_path(), "shell"])
            except Exception as e:
                self._output(f"Shell错误: {str(e)}")
        
        threading.Thread(target=run_shell, daemon=True).start()
    
    def push_file(self, device_id, local_path, remote_path):
        """推送文件到设备"""
        return Utils.run_command(["push", local_path, remote_path], device=device_id)
    
    def pull_file(self, device_id, remote_path, local_path):
        """从设备拉取文件"""
        return Utils.run_command(["pull", remote_path, local_path], device=device_id)
    
    def install_apk(self, device_id, apk_path):
        """安装APK"""
        return Utils.run_command(["install", apk_path], device=device_id)
    
    def uninstall_apk(self, device_id, package_name):
        """卸载APK"""
        return Utils.run_command(["uninstall", package_name], device=device_id)
    
    def take_screenshot(self, device_id):
        """截图"""
        import time
        filename = f"screenshot_{int(time.time())}.png"
        
        # 截图到设备
        result1 = Utils.run_command(["shell", "screencap", "-p", f"/sdcard/{filename}"], device=device_id)
        if result1['success']:
            # 拉取到电脑
            result2 = Utils.run_command(["pull", f"/sdcard/{filename}", f"./{filename}"], device=device_id)
            return result2
        return result1
    
    def get_logcat(self, device_id):
        """获取日志"""
        def run_logcat():
            try:
                import subprocess
                if device_id:
                    subprocess.run([Utils.get_adb_path(), "-s", device_id, "logcat"])
                else:
                    subprocess.run([Utils.get_adb_path(), "logcat"])
            except Exception as e:
                self._output(f"Logcat错误: {str(e)}")
        
        threading.Thread(target=run_logcat, daemon=True).start()
