#!/usr/bin/env python3
"""
WAV 文件重编号工具 - tkinter 可视化界面
功能：选择文件夹，预览修改，应用编号
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

class WavRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WAV 文件重编号工具")
        self.root.geometry("700x550")
        
        self.folder_path = tk.StringVar()
        self.start_num = tk.IntVar(value=1)
        self.digits = tk.StringVar(value="4")
        self.prefix = tk.StringVar()
        self.keep_original = tk.BooleanVar(value=False)
        self.keep_length = tk.IntVar(value=4)
        
        self.wav_files = []
        self.current_folder = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # 文件夹选择
        frame_folder = ttk.LabelFrame(self.root, text="选择文件夹", padding=10)
        frame_folder.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(frame_folder, textvariable=self.folder_path, width=50).pack(side="left", padx=5)
        ttk.Button(frame_folder, text="浏览...", command=self.browse_folder).pack(side="left")
        
        # 设置面板
        frame_settings = ttk.LabelFrame(self.root, text="编号设置", padding=10)
        frame_settings.pack(fill="x", padx=10, pady=5)
        
        # 第一行
        row1 = ttk.Frame(frame_settings)
        row1.pack(fill="x", pady=3)
        ttk.Label(row1, text="起始数字:").pack(side="left")
        ttk.Spinbox(row1, from_=0, to=9999, textvariable=self.start_num, width=8).pack(side="left", padx=5)
        ttk.Label(row1, text="  数字位数:").pack(side="left")
        ttk.Combobox(row1, textvariable=self.digits, values=["3", "4", "5", "6"], width=5).pack(side="left", padx=5)
        
        # 第二行
        row2 = ttk.Frame(frame_settings)
        row2.pack(fill="x", pady=3)
        ttk.Label(row2, text="前缀:").pack(side="left")
        ttk.Entry(row2, textvariable=self.prefix, width=15).pack(side="left", padx=5)
        ttk.Checkbutton(row2, text="保留原名", variable=self.keep_original).pack(side="left", padx=10)
        ttk.Label(row2, text="字符数:").pack(side="left")
        ttk.Spinbox(row2, from_=0, to=20, textvariable=self.keep_length, width=5).pack(side="left", padx=5)
        
        # 刷新按钮
        ttk.Button(frame_settings, text="刷新文件列表", command=self.refresh_files).pack(pady=5)
        
        # 预览列表
        frame_preview = ttk.LabelFrame(self.root, text="预览", padding=10)
        frame_preview.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.preview_listbox = tk.Listbox(frame_preview, font=("Courier", 10), height=12)
        self.preview_listbox.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.preview_listbox, orient="vertical", command=self.preview_listbox.yview)
        self.preview_listbox.configure(yscrollcommand=scrollbar.set)
        
        # 操作按钮
        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(frame_buttons, text="预览修改", command=self.preview_rename).pack(side="left", padx=5)
        ttk.Button(frame_buttons, text="应用修改", command=self.apply_rename).pack(side="left", padx=5)
        ttk.Button(frame_buttons, text="重置", command=self.reset).pack(side="left", padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(self.root, textvariable=self.status_var, relief="sunken").pack(fill="x", padx=10, pady=5)
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.current_folder = folder
            self.load_wav_files()
    
    def load_wav_files(self):
        self.wav_files = []
        if os.path.isdir(self.current_folder):
            for f in sorted(os.listdir(self.current_folder)):
                if f.lower().endswith('.wav'):
                    self.wav_files.append(f)
        self.status_var.set(f"已加载 {len(self.wav_files)} 个 WAV 文件")
    
    def refresh_files(self):
        if self.current_folder:
            self.load_wav_files()
    
    def generate_new_name(self, original_name, index):
        name_without_ext = Path(original_name).stem
        new_num = self.start_num.get() + index
        digits = int(self.digits.get())
        prefix = self.prefix.get()
        keep_length = self.keep_length.get()
        
        if prefix:
            new_name = f"{prefix}{new_num:0{digits}d}"
        else:
            new_name = f"{new_num:0{digits}d}"
        
        if self.keep_original.get() and keep_length > 0:
            new_name = f"{new_name}_{name_without_ext[:keep_length]}"
        
        return f"{new_name}.wav"
    
    def preview_rename(self):
        if not self.wav_files:
            messagebox.showwarning("警告", "请先选择文件夹")
            return
        
        self.preview_listbox.delete(0, tk.END)
        
        for i, wav_file in enumerate(self.wav_files):
            new_name = self.generate_new_name(wav_file, i)
            self.preview_listbox.insert(tk.END, f"{wav_file:<40} → {new_name}")
        
        self.status_var.set(f"预览 {len(self.wav_files)} 个文件")
    
    def apply_rename(self):
        if not self.wav_files:
            messagebox.showwarning("警告", "请先选择文件夹")
            return
        
        confirm = messagebox.askyesno("确认", f"确定要重命名 {len(self.wav_files)} 个文件吗？\n\n此操作不可撤销！")
        if not confirm:
            return
        
        renamed = 0
        errors = []
        
        for i, wav_file in enumerate(self.wav_files):
            try:
                new_name = self.generate_new_name(wav_file, i)
                old_path = os.path.join(self.current_folder, wav_file)
                new_path = os.path.join(self.current_folder, new_name)
                
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    renamed += 1
            except Exception as e:
                errors.append(f"{wav_file}: {str(e)}")
        
        # 刷新列表
        self.load_wav_files()
        self.preview_listbox.delete(0, tk.END)
        
        if errors:
            messagebox.showwarning("完成", f"成功: {renamed} 个\n错误: {len(errors)} 个\n\n" + "\n".join(errors))
        else:
            messagebox.showinfo("完成", f"成功重命名 {renamed} 个文件")
        
        self.status_var.set(f"已完成 {renamed} 个文件的重命名")
    
    def reset(self):
        self.start_num.set(1)
        self.digits.set("4")
        self.prefix.set("")
        self.keep_original.set(False)
        self.keep_length.set(4)
        self.preview_listbox.delete(0, tk.END)
        self.status_var.set("已重置")

if __name__ == "__main__":
    root = tk.Tk()
    app = WavRenamerApp(root)
    root.mainloop()
