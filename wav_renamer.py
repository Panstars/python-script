import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import re

class WavRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("WAV 文件批量重命名工具")
        self.root.geometry("600x500")
        
        self.folder_path = tk.StringVar()
        self.find_text = tk.StringVar()
        self.replace_text = tk.StringVar()
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()
        self.files = []
        
        self.build_ui()
    
    def build_ui(self):
        # 文件夹选择
        tk.Label(self.root, text="文件夹路径:").pack(pady=(10, 0))
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Entry(frame, textvariable=self.folder_path, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="浏览", command=self.browse_folder).pack(side=tk.LEFT)
        
        # 预览列表
        tk.Label(self.root, text="预览:").pack(pady=(10, 0))
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=10)
        
        self.old_listbox = tk.Listbox(list_frame, width=28, height=12)
        self.old_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.old_scroll = tk.Scrollbar(list_frame, command=self.old_listbox.yview)
        self.old_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.old_listbox.config(yscrollcommand=self.old_scroll.set)
        
        self.new_listbox = tk.Listbox(list_frame, width=28, height=12)
        self.new_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        self.new_scroll = tk.Scrollbar(list_frame, command=self.new_listbox.yview)
        self.new_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.new_listbox.config(yscrollcommand=self.new_scroll.set)
        
        # 重命名选项
        option_frame = tk.LabelFrame(self.root, text="重命名选项")
        option_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(option_frame, text="查找:").grid(row=0, column=0, sticky=W, padx=5, pady=2)
        tk.Entry(option_frame, textvariable=self.find_text, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(option_frame, text="替换为:").grid(row=0, column=2, sticky=W, padx=5, pady=2)
        tk.Entry(option_frame, textvariable=self.replace_text, width=20).grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(option_frame, text="前缀:").grid(row=1, column=0, sticky=W, padx=5, pady=2)
        tk.Entry(option_frame, textvariable=self.prefix, width=20).grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(option_frame, text="后缀:").grid(row=1, column=2, sticky=W, padx=5, pady=2)
        tk.Entry(option_frame, textvariable=self.suffix, width=20).grid(row=1, column=3, padx=5, pady=2)
        
        tk.Button(option_frame, text="预览", command=self.preview).grid(row=2, column=0, pady=5, padx=5)
        tk.Button(option_frame, text="执行重命名", command=self.execute_rename, bg="#4CAF50", fg="white").grid(row=2, column=1, columnspan=3, pady=5, padx=5, sticky=E)
        
        self.find_text.trace_add('write', lambda *args: self.preview())
        self.replace_text.trace_add('write', lambda *args: self.preview())
        self.prefix.trace_add('write', lambda *args: self.preview())
        self.suffix.trace_add('write', lambda *args: self.preview())
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.load_files()
    
    def load_files(self):
        folder = self.folder_path.get()
        if not folder:
            return
        
        self.files = [f for f in os.listdir(folder) if f.lower().endswith('.wav')]
        self.old_listbox.delete(0, tk.END)
        self.new_listbox.delete(0, tk.END)
        
        for f in self.files:
            self.old_listbox.insert(tk.END, f)
        
        self.preview()
    
    def preview(self):
        self.new_listbox.delete(0, tk.END)
        
        find = self.find_text.get()
        replace = self.replace_text.get()
        prefix = self.prefix.get()
        suffix = self.suffix.get()
        
        for f in self.files:
            name = prefix + f
            if find:
                name = name.replace(find, replace)
            if suffix:
                # 在 .wav 之前添加后缀
                name = name[:-4] + suffix + ".wav"
            self.new_listbox.insert(tk.END, name)
    
    def execute_rename(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("警告", "请先选择文件夹")
            return
        
        find = self.find_text.get()
        replace = self.replace_text.get()
        prefix = self.prefix.get()
        suffix = self.suffix.get()
        
        renamed = []
        for f in self.files:
            new_name = prefix + f
            if find:
                new_name = new_name.replace(find, replace)
            if suffix:
                new_name = new_name[:-4] + suffix + ".wav"
            
            if new_name != f:
                src = os.path.join(folder, f)
                dst = os.path.join(folder, new_name)
                try:
                    shutil.move(src, dst)
                    renamed.append((f, new_name))
                except Exception as e:
                    messagebox.showerror("错误", f"重命名 {f} 失败:\n{e}")
                    return
        
        if renamed:
            messagebox.showinfo("完成", f"成功重命名 {len(renamed)} 个文件")
            self.load_files()
        else:
            messagebox.showinfo("提示", "没有文件被重命名")

if __name__ == "__main__":
    root = tk.Tk()
    app = WavRenamer(root)
    root.mainloop()
