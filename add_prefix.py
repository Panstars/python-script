import os
import sys

def main():
    folder = input("输入文件夹路径（留空则当前目录）: ").strip()
    if not folder:
        folder = os.getcwd()
    
    if not os.path.isdir(folder):
        print("文件夹不存在。")
        input("按回车退出...")
        return

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    
    if not files:
        print("文件夹中没有文件。")
        input("按回车退出...")
        return

    files.sort()
    renamed = []

    for filename in files:
        old_path = os.path.join(folder, filename)
        new_name = "0000" + filename
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        renamed.append((filename, new_name))

    print(f"\n完成，共处理 {len(renamed)} 个文件：")
    for old, new in renamed:
        print(f"  {old} → {new}")
    
    input("\n按回车退出...")

if __name__ == "__main__":
    main()
