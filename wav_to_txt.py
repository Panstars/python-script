#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
folder = filedialog.askdirectory(title="选择目标文件夹")

if folder:
    count = 0
    for f in os.listdir(folder):
        if f.lower().endswith('.wav'):
            txt_path = os.path.join(folder, os.path.splitext(f)[0] + '.txt')
            open(txt_path, 'w').close()
            count += 1
    print(f"完成！生成了 {count} 个 .txt 文件")
else:
    print("已取消")
