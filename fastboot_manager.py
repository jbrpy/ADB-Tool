# fastboot_manager.py
from utils import Utils

class FastbootManager:
    """Fastboot功能管理类"""
    
    def __init__(self, output_callback=None):
        self.output_callback = output_callback
    
    def set_output_callback(self, callback):
        """设置输出回调函数"""
        self.output_callback = callback
    
    def _output(self, text):
        """输出文本"""
        if self.output_callback:
            self.output_callback(text)
    
    def flash_partition(self, device_id, partition, image_path):
        """刷写分区"""
        return Utils.run_command(["flash", partition, image_path], use_fastboot=True, device=device_id)
    
    def erase_partition(self, device_id, partition):
        """擦除分区"""
        return Utils.run_command(["erase", partition], use_fastboot=True, device=device_id)
    
    def unlock_bootloader(self, device_id):
        """解锁Bootloader"""
        return Utils.run_command(["flashing", "unlock"], use_fastboot=True, device=device_id)
    
    def lock_bootloader(self, device_id):
        """锁定Bootloader"""
        return Utils.run_command(["flashing", "lock"], use_fastboot=True, device=device_id)
    
    def reboot(self, device_id, mode=""):
        """重启设备"""
        if mode:
            return Utils.run_command(["reboot", mode], use_fastboot=True, device=device_id)
        else:
            return Utils.run_command(["reboot"], use_fastboot=True, device=device_id)
    
    def boot_image(self, device_id, image_path):
        """临时启动镜像"""
        return Utils.run_command(["boot", image_path], use_fastboot=True, device=device_id)
    
    def get_var(self, device_id, var_name="all"):
        """获取设备变量"""
        return Utils.run_command(["getvar", var_name], use_fastboot=True, device=device_id)
    
    def oem_command(self, device_id, command):
        """执行OEM命令"""
        return Utils.run_command(["oem", command], use_fastboot=True, device=device_id)
