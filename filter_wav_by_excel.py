import tkinter as tk
from tkinter import filedialog
import openpyxl
import shutil
import os
import re

# 隐藏主窗口
root = tk.Tk()
root.withdraw()

# 选择文件夹
folder = filedialog.askdirectory(title="选择文件夹")
if not folder:
    print("未选择文件夹")
    exit()

# 查找 Excel 文件
excel_files = [f for f in os.listdir(folder) if f.endswith(('.xlsx', '.xls'))]
if not excel_files:
    print("未找到 Excel 文件")
    exit()

excel_path = os.path.join(folder, excel_files[0])
print(f"读取 Excel: {excel_files[0]}")

# 读取 Excel，找到 E 列值为 1 的行，取 A 列序号
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb.active

numbers_to_remove = []
for row in ws.iter_rows(min_row=2):  # 跳过表头
    a_val = row[0].value  # A 列
    e_val = row[4].value  # E 列
    if e_val == 1 and a_val is not None:
        try:
            num = int(float(a_val))
            numbers_to_remove.append(num)
        except (ValueError, TypeError):
            pass

wb.close()
print(f"需要剔除的序号: {numbers_to_remove}")

if not numbers_to_remove:
    print("没有找到需要剔除的文件")
    exit()

# 创建"剔除"文件夹
remove_folder = os.path.join(folder, "剔除")
os.makedirs(remove_folder, exist_ok=True)

# 查找所有 .wav 文件
wav_files = [f for f in os.listdir(folder) if f.lower().endswith('.wav')]
print(f"找到 {len(wav_files)} 个 WAV 文件")

# 移动匹配的文件
moved = []
for wav in wav_files:
    # 提取文件名中的数字
    match = re.search(r'(\d+)', wav)
    if match:
        wav_num = int(match.group(1))
        if wav_num in numbers_to_remove:
            src = os.path.join(folder, wav)
            dst = os.path.join(remove_folder, wav)
            shutil.move(src, dst)
            moved.append(wav)
            print(f"移动: {wav} -> 剔除/")

print(f"\n完成，共移动 {len(moved)} 个文件到「剔除」文件夹")
