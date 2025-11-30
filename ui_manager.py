# ui_manager.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import tkinter.simpledialog
from config import Config

class UIManager:
    """界面管理类"""
    
    def __init__(self, root, adb_manager, fastboot_manager, device_manager):
        self.root = root
        self.adb_manager = adb_manager
        self.fastboot_manager = fastboot_manager
        self.device_manager = device_manager
        
        self.selected_device = None
        self.current_mode = "adb"
        
        # 创建界面组件
        self.device_frame = None
        self.main_frame = None
        self.output_text = None
        self.current_device_label = None
        self.mode_label = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        
        self.create_device_selection_ui()
        self.create_main_interface()
        
        # 初始显示设备选择界面
        self.main_frame.pack_forget()
    
    def create_device_selection_ui(self):
        """创建设备选择界面"""
        self.device_frame = ttk.Frame(self.root, padding="10")
        self.device_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(self.device_frame, text="ADB/Fastboot 设备选择", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        # 工具路径显示
        path_frame = ttk.Frame(self.device_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_frame, text=f"ADB路径: {Config.get_adb_path()}").pack(anchor=tk.W)
        ttk.Label(path_frame, text=f"Fastboot路径: {Config.get_fastboot_path()}").pack(anchor=tk.W)
        
        # 创建选项卡
        notebook = ttk.Notebook(self.device_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # ADB设备选项卡
        adb_tab = ttk.Frame(notebook, padding="5")
        notebook.add(adb_tab, text="ADB设备")
        
        ttk.Label(adb_tab, text="已连接的ADB设备:").pack(anchor=tk.W, pady=5)
        self.adb_listbox = tk.Listbox(adb_tab, height=8)
        self.adb_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Fastboot设备选项卡
        fastboot_tab = ttk.Frame(notebook, padding="5")
        notebook.add(fastboot_tab, text="Fastboot设备")
        
        ttk.Label(fastboot_tab, text="已连接的Fastboot设备:").pack(anchor=tk.W, pady=5)
        self.fastboot_listbox = tk.Listbox(fastboot_tab, height=8)
        self.fastboot_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(self.device_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="刷新设备列表", 
                  command=self.refresh_devices).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="选择ADB设备", 
                  command=lambda: self.select_device("adb")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="选择Fastboot设备", 
                  command=lambda: self.select_device("fastboot")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="退出", 
                  command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def create_main_interface(self):
        """创建主界面"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # 标题和当前设备显示
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(title_frame, text="ADB/Fastboot 完整工具", 
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        self.current_device_label = ttk.Label(title_frame, text="当前设备: 无", foreground="red")
        self.current_device_label.pack(side=tk.RIGHT)
        
        # 模式指示器
        self.mode_label = ttk.Label(self.main_frame, text="当前模式: ADB", 
                                   font=("Arial", 10, "bold"))
        self.mode_label.pack(anchor=tk.W, pady=2)
        
        # 创建主选项卡
        main_notebook = ttk.Notebook(self.main_frame)
        main_notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建各功能选项卡
        self.adb_tab = self.create_adb_tab()
        self.fastboot_tab = self.create_fastboot_tab()
        self.common_tab = self.create_common_tab()
        
        main_notebook.add(self.adb_tab, text="ADB功能")
        main_notebook.add(self.fastboot_tab, text="Fastboot功能")
        main_notebook.add(self.common_tab, text="通用功能")
        
        # 输出框
        output_frame = ttk.LabelFrame(self.main_frame, text="命令输出", padding="5")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=12, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # 底部按钮
        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(bottom_frame, text="选择其他设备", 
                  command=self.back_to_device_selection).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="清除输出", 
                  command=self.clear_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="自定义命令", 
                  command=self.custom_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="退出", 
                  command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def create_adb_tab(self):
        """创建ADB功能选项卡"""
        tab = ttk.Frame(self.main_frame, padding="5")
        
        # 设备操作框架
        device_frame = ttk.LabelFrame(tab, text="设备操作", padding="5")
        device_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(device_frame, text="重启设备", 
                  command=lambda: self.adb_reboot("")).pack(side=tk.LEFT, padx=2)
        ttk.Button(device_frame, text="重启到Recovery", 
                  command=lambda: self.adb_reboot("recovery")).pack(side=tk.LEFT, padx=2)
        ttk.Button(device_frame, text="重启到Bootloader", 
                  command=lambda: self.adb_reboot("bootloader")).pack(side=tk.LEFT, padx=2)
        ttk.Button(device_frame, text="重启到Fastboot", 
                  command=lambda: self.adb_reboot("fastboot")).pack(side=tk.LEFT, padx=2)
        ttk.Button(device_frame, text="进入ADB Shell", 
                  command=self.adb_shell).pack(side=tk.LEFT, padx=2)
        
        # 文件操作框架
        file_frame = ttk.LabelFrame(tab, text="文件操作", padding="5")
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(file_frame, text="推送文件到设备", 
                  command=self.adb_push).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame, text="从设备拉取文件", 
                  command=self.adb_pull).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame, text="安装APK", 
                  command=self.adb_install).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame, text="卸载APK", 
                  command=self.adb_uninstall).pack(side=tk.LEFT, padx=2)
        
        # 系统信息框架
        info_frame = ttk.LabelFrame(tab, text="系统信息", padding="5")
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(info_frame, text="获取设备信息", 
                  command=self.adb_get_device_info).pack(side=tk.LEFT, padx=2)
        ttk.Button(info_frame, text="查看日志", 
                  command=self.adb_logcat).pack(side=tk.LEFT, padx=2)
        ttk.Button(info_frame, text="查看进程", 
                  command=self.adb_ps).pack(side=tk.LEFT, padx=2)
        ttk.Button(info_frame, text="查看存储空间", 
                  command=self.adb_df).pack(side=tk.LEFT, padx=2)
        
        return tab
    
    def create_fastboot_tab(self):
        """创建Fastboot功能选项卡"""
        tab = ttk.Frame(self.main_frame, padding="5")
        
        # 刷写操作框架
        flash_frame = ttk.LabelFrame(tab, text="刷写操作", padding="5")
        flash_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(flash_frame, text="刷写Boot", 
                  command=lambda: self.fastboot_flash("boot")).pack(side=tk.LEFT, padx=2)
        ttk.Button(flash_frame, text="刷写System", 
                  command=lambda: self.fastboot_flash("system")).pack(side=tk.LEFT, padx=2)
        ttk.Button(flash_frame, text="刷写Recovery", 
                  command=lambda: self.fastboot_flash("recovery")).pack(side=tk.LEFT, padx=2)
        ttk.Button(flash_frame, text="刷写Cache", 
                  command=lambda: self.fastboot_flash("cache")).pack(side=tk.LEFT, padx=2)
        ttk.Button(flash_frame, text="刷写Userdata", 
                  command=lambda: self.fastboot_flash("userdata")).pack(side=tk.LEFT, padx=2)
        ttk.Button(flash_frame, text="刷写自定义分区", 
                  command=self.fastboot_flash_custom).pack(side=tk.LEFT, padx=2)
        
        # Bootloader操作框架
        bootloader_frame = ttk.LabelFrame(tab, text="Bootloader操作", padding="5")
        bootloader_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(bootloader_frame, text="解锁Bootloader", 
                  command=self.fastboot_unlock).pack(side=tk.LEFT, padx=2)
        ttk.Button(bootloader_frame, text="锁定Bootloader", 
                  command=self.fastboot_lock).pack(side=tk.LEFT, padx=2)
        ttk.Button(bootloader_frame, text="查询解锁状态", 
                  command=self.fastboot_get_unlock_data).pack(side=tk.LEFT, padx=2)
        
        return tab
    
    def create_common_tab(self):
        """创建通用功能选项卡"""
        tab = ttk.Frame(self.main_frame, padding="5")
        
        # 重启框架
        reboot_frame = ttk.LabelFrame(tab, text="重启选项", padding="5")
        reboot_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(reboot_frame, text="正常重启", 
                  command=self.common_reboot).pack(side=tk.LEFT, padx=2)
        ttk.Button(reboot_frame, text="重启到Recovery", 
                  command=self.common_reboot_recovery).pack(side=tk.LEFT, padx=2)
        ttk.Button(reboot_frame, text="重启到Bootloader", 
                  command=self.common_reboot_bootloader).pack(side=tk.LEFT, padx=2)
        ttk.Button(reboot_frame, text="重启到Fastboot", 
                  command=self.common_reboot_fastboot).pack(side=tk.LEFT, padx=2)
        
        # 工具框架
        tool_frame = ttk.LabelFrame(tab, text="工具", padding="5")
        tool_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(tool_frame, text="检查设备连接", 
                  command=self.common_check_connection).pack(side=tk.LEFT, padx=2)
        ttk.Button(tool_frame, text="重启ADB服务", 
                  command=self.common_restart_adb).pack(side=tk.LEFT, padx=2)
        
        return tab
    
    def output_text(self, text):
        """输出文本到界面"""
        if self.output_text:
            self.output_text.insert(tk.END, text + "\n")
            self.output_text.see(tk.END)
            self.root.update()
    
    def refresh_devices(self):
        """刷新设备列表"""
        self.adb_listbox.delete(0, tk.END)
        self.fastboot_listbox.delete(0, tk.END)
        
        adb_devices, fastboot_devices = self.device_manager.refresh_devices()
        
        for device in adb_devices:
            self.adb_listbox.insert(tk.END, device)
        
        for device in fastboot_devices:
            self.fastboot_listbox.insert(tk.END, device)
        
        if not adb_devices:
            self.adb_listbox.insert(tk.END, "未找到ADB设备")
        if not fastboot_devices:
            self.fastboot_listbox.insert(tk.END, "未找到Fastboot设备")
    
    def select_device(self, mode):
        """选择设备"""
        if mode == "adb":
            selection = self.adb_listbox.curselection()
            if not selection:
                messagebox.showwarning("警告", "请先选择一个ADB设备")
                return
            devices = self.device_manager.adb_devices
        else:
            selection = self.fastboot_listbox.curselection()
            if not selection:
                messagebox.showwarning("警告", "请先选择一个Fastboot设备")
                return
            devices = self.device_manager.fastboot_devices
        
        if selection[0] < len(devices):
            self.selected_device = devices[selection[0]]
            self.current_mode = mode
            
            # 切换到主界面
            self.device_frame.pack_forget()
            self.main_frame.pack(fill=tk.BOTH, expand=True)
            
            mode_text = "ADB" if mode == "adb" else "Fastboot"
            self.current_device_label.config(text=f"当前设备: {self.selected_device}")
            self.mode_label.config(text=f"当前模式: {mode_text}")
            
            self.output_text(f"已选择设备: {self.selected_device} ({mode_text}模式)")
    
    def back_to_device_selection(self):
        """返回设备选择界面"""
        self.main_frame.pack_forget()
        self.device_frame.pack(fill=tk.BOTH, expand=True)
        self.selected_device = None
        self.current_mode = "adb"
        self.refresh_devices()
    
    def clear_output(self):
        """清除输出"""
        if self.output_text:
            self.output_text.delete(1.0, tk.END)
    
    def custom_command(self):
        """自定义命令"""
        command = tk.simpledialog.askstring("自定义命令", "请输入命令:")
        if command:
            self.output_text(f"执行自定义命令: {command}")
            # 这里可以添加自定义命令的执行逻辑
    
    # ADB功能方法
    def adb_reboot(self, mode):
        """ADB重启"""
        if self.selected_device and self.current_mode == "adb":
            result = self.adb_manager.reboot(self.selected_device, mode)
            self.output_text(f"重启到{mode if mode else '系统'}: {result['output']}")
    
    def adb_shell(self):
        """ADB Shell"""
        if self.selected_device and self.current_mode == "adb":
            self.adb_manager.shell(self.selected_device)
    
    def adb_push(self):
        """推送文件"""
        if self.selected_device and self.current_mode == "adb":
            file_path = filedialog.askopenfilename(title="选择要推送的文件")
            if file_path:
                dest_path = tk.simpledialog.askstring("目标路径", "请输入设备上的目标路径:")
                if dest_path:
                    result = self.adb_manager.push_file(self.selected_device, file_path, dest_path)
                    self.output_text(f"推送文件: {result['output']}")
    
    def adb_pull(self):
        """拉取文件"""
        if self.selected_device and self.current_mode == "adb":
            src_path = tk.simpledialog.askstring("源路径", "请输入设备上的文件路径:")
            if src_path:
                dest_path = filedialog.asksaveasfilename(title="保存文件到")
                if dest_path:
                    result = self.adb_manager.pull_file(self.selected_device, src_path, dest_path)
                    self.output_text(f"拉取文件: {result['output']}")
    
    def adb_install(self):
        """安装APK"""
        if self.selected_device and self.current_mode == "adb":
            apk_path = filedialog.askopenfilename(title="选择APK文件", filetypes=[("APK文件", "*.apk")])
            if apk_path:
                result = self.adb_manager.install_apk(self.selected_device, apk_path)
                self.output_text(f"安装APK: {result['output']}")
    
    def adb_uninstall(self):
        """卸载APK"""
        if self.selected_device and self.current_mode == "adb":
            package = tk.simpledialog.askstring("卸载应用", "请输入包名:")
            if package:
                result = self.adb_manager.uninstall_apk(self.selected_device, package)
                self.output_text(f"卸载应用: {result['output']}")
    
    def adb_get_device_info(self):
        """获取设备信息"""
        if self.selected_device and self.current_mode == "adb":
            info = self.device_manager.get_device_info(self.selected_device, False)
            self.output_text("设备信息:")
            for key, value in info.items():
                self.output_text(f"  {key}: {value}")
    
    def adb_logcat(self):
        """查看日志"""
        if self.selected_device and self.current_mode == "adb":
            self.adb_manager.get_logcat(self.selected_device)
    
    def adb_ps(self):
        """查看进程"""
        if self.selected_device and self.current_mode == "adb":
            self.output_text("查看进程功能待实现")
    
    def adb_df(self):
        """查看存储"""
        if self.selected_device and self.current_mode == "adb":
            self.output_text("查看存储功能待实现")
    
    # Fastboot功能方法
    def fastboot_flash(self, partition):
        """刷写分区"""
        if self.selected_device and self.current_mode == "fastboot":
            file_path = filedialog.askopenfilename(title=f"选择{partition}镜像", filetypes=[("镜像文件", "*.img")])
            if file_path:
                result = self.fastboot_manager.flash_partition(self.selected_device, partition, file_path)
                self.output_text(f"刷写{partition}: {result['output']}")
    
    def fastboot_flash_custom(self):
        """刷写自定义分区"""
        if self.selected_device and self.current_mode == "fastboot":
            partition = tk.simpledialog.askstring("刷写分区", "请输入分区名称:")
            if partition:
                file_path = filedialog.askopenfilename(title="选择镜像文件", filetypes=[("镜像文件", "*.img")])
                if file_path:
                    result = self.fastboot_manager.flash_partition(self.selected_device, partition, file_path)
                    self.output_text(f"刷写{partition}: {result['output']}")
    
    def fastboot_unlock(self):
        """解锁Bootloader"""
        if self.selected_device and self.current_mode == "fastboot":
            if messagebox.askyesno("警告", "解锁Bootloader会清除设备数据！确定继续吗？"):
                result = self.fastboot_manager.unlock_bootloader(self.selected_device)
                self.output_text(f"解锁Bootloader: {result['output']}")
    
    def fastboot_lock(self):
        """锁定Bootloader"""
        if self.selected_device and self.current_mode == "fastboot":
            if messagebox.askyesno("警告", "锁定Bootloader会清除设备数据！确定继续吗？"):
                result = self.fastboot_manager.lock_bootloader(self.selected_device)
                self.output_text(f"锁定Bootloader: {result['output']}")
    
    def fastboot_get_unlock_data(self):
        """获取解锁数据"""
        if self.selected_device and self.current_mode == "fastboot":
            result = self.fastboot_manager.oem_command(self.selected_device, "get_unlock_data")
            self.output_text(f"解锁数据: {result['output']}")
    
    # 通用功能方法
    def common_reboot(self):
        """通用重启"""
        if self.selected_device:
            if self.current_mode == "adb":
                self.adb_reboot("")
            else:
                result = self.fastboot_manager.reboot(self.selected_device, "")
                self.output_text(f"重启: {result['output']}")
    
    def common_reboot_recovery(self):
        """重启到Recovery"""
        if self.selected_device:
            if self.current_mode == "adb":
                self.adb_reboot("recovery")
            else:
                result = self.fastboot_manager.reboot(self.selected_device, "recovery")
                self.output_text(f"重启到Recovery: {result['output']}")
    
    def common_reboot_bootloader(self):
        """重启到Bootloader"""
        if self.selected_device:
            if self.current_mode == "adb":
                self.adb_reboot("bootloader")
            else:
                result = self.fastboot_manager.reboot(self.selected_device, "bootloader")
                self.output_text(f"重启到Bootloader: {result['output']}")
    
    def common_reboot_fastboot(self):
        """重启到Fastboot"""
        if self.selected_device and self.current_mode == "adb":
            self.adb_reboot("fastboot")
    
    def common_check_connection(self):
        """检查设备连接"""
        self.refresh_devices()
        self.output_text("设备连接状态已刷新")
    
    def common_restart_adb(self):
        """重启ADB服务"""
        self.output_text("重启ADB服务功能待实现")
