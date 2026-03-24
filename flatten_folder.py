import os
import shutil
import tkinter as tk
from tkinter import filedialog

def flatten_folder(root):
    # 收集所有文件
    all_files = []
    for dirpath, _, filenames in os.walk(root):
        if dirpath == root:
            continue
        for f in filenames:
            all_files.append(os.path.join(dirpath, f))

    if not all_files:
        print("没有找到子文件夹中的文件。")
        input("按回车退出...")
        return

    print(f"找到 {len(all_files)} 个文件，即将移动到根目录：")
    for f in all_files:
        print(f"  {os.path.relpath(f, root)}")

    confirm = input("\n确认操作？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消。")
        input("按回车退出...")
        return

    # 移动文件，处理同名冲突
    for src in all_files:
        filename = os.path.basename(src)
        dst = os.path.join(root, filename)
        if os.path.exists(dst):
            name, ext = os.path.splitext(filename)
            i = 1
            while os.path.exists(dst):
                dst = os.path.join(root, f"{name}_{i}{ext}")
                i += 1
        shutil.move(src, dst)
        print(f"✓ 移动: {os.path.basename(dst)}")

    # 删除空文件夹（从深到浅）
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if dirpath == root:
            continue
        if not os.listdir(dirpath):
            os.rmdir(dirpath)
            print(f"✓ 删除空文件夹: {os.path.relpath(dirpath, root)}")

    input("\n完成！按回车退出...")

def main():
    tk.Tk().withdraw()
    folder = filedialog.askdirectory(title="选择要整理的文件夹")
    if not folder:
        print("未选择文件夹。")
        return
    print(f"目标文件夹: {folder}\n")
    flatten_folder(folder)

if __name__ == "__main__":
    main()
