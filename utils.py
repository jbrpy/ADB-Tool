# utils.py
import os
import sys
import subprocess
from config import Config

class Utils:
    """工具函数类"""
    
    @staticmethod
    def resource_path(relative_path):
        """获取资源文件的绝对路径"""
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    @staticmethod
    def run_command(command, use_fastboot=False, device=None, timeout=60):
        """执行命令的通用方法"""
        try:
            if use_fastboot:
                tool_path = Config.get_fastboot_path()
                if device:
                    full_command = [tool_path, "-s", device] + command
                else:
                    full_command = [tool_path] + command
            else:
                tool_path = Config.get_adb_path()
                if device:
                    full_command = [tool_path, "-s", device] + command
                else:
                    full_command = [tool_path] + command
            
            result = subprocess.run(full_command, capture_output=True, text=True, timeout=timeout)
            return {
                'success': result.returncode == 0,
                'output': result.stdout if result.stdout else result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': '命令执行超时', 'returncode': -1}
        except Exception as e:
            return {'success': False, 'output': f'错误: {str(e)}', 'returncode': -1}
    
    @staticmethod
    def check_tool_available():
        """检查工具是否可用"""
        try:
            result = subprocess.run([Config.get_adb_path(), "version"], capture_output=True)
            return result.returncode == 0
        except:
            return False
