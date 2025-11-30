# device_manager.py
import subprocess
from config import Config
from utils import Utils

class DeviceManager:
    """设备管理类"""
    
    def __init__(self):
        self.adb_devices = []
        self.fastboot_devices = []
    
    def refresh_devices(self):
        """刷新设备列表"""
        self._refresh_adb_devices()
        self._refresh_fastboot_devices()
        return self.adb_devices, self.fastboot_devices
    
    def _refresh_adb_devices(self):
        """刷新ADB设备"""
        self.adb_devices = []
        try:
            result = Utils.run_command(["devices"])
            if result['success']:
                lines = result['output'].strip().split('\n')
                for line in lines[1:]:
                    if line.strip() and '\tdevice' in line:
                        device_id = line.split('\t')[0]
                        self.adb_devices.append(device_id)
        except Exception as e:
            print(f"刷新ADB设备错误: {e}")
    
    def _refresh_fastboot_devices(self):
        """刷新Fastboot设备"""
        self.fastboot_devices = []
        try:
            result = Utils.run_command(["devices"], use_fastboot=True)
            if result['success']:
                lines = result['output'].strip().split('\n')
                for line in lines:
                    if line.strip():
                        device_id = line.split('\t')[0]
                        self.fastboot_devices.append(device_id)
        except Exception as e:
            print(f"刷新Fastboot设备错误: {e}")
    
    def get_device_info(self, device_id, use_fastboot=False):
        """获取设备信息"""
        if use_fastboot:
            return self._get_fastboot_device_info(device_id)
        else:
            return self._get_adb_device_info(device_id)
    
    def _get_adb_device_info(self, device_id):
        """获取ADB设备信息"""
        info = {}
        commands = {
            'model': ['shell', 'getprop', 'ro.product.model'],
            'android_version': ['shell', 'getprop', 'ro.build.version.release'],
            'sdk_version': ['shell', 'getprop', 'ro.build.version.sdk'],
            'serial': ['shell', 'getprop', 'ro.serialno']
        }
        
        for key, cmd in commands.items():
            result = Utils.run_command(cmd, device=device_id)
            if result['success']:
                info[key] = result['output'].strip()
        
        return info
    
    def _get_fastboot_device_info(self, device_id):
        """获取Fastboot设备信息"""
        result = Utils.run_command(["getvar", "all"], use_fastboot=True, device=device_id)
        return {'fastboot_info': result['output'] if result['success'] else '获取失败'}
