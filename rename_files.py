import os
import sys

def main():
    folder = os.path.dirname(os.path.abspath(sys.argv[0]))
    files = sorted([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f != os.path.basename(sys.argv[0])])
    
    if not files:
        input("没有找到文件。按回车退出...")
        return

    print(f"找到 {len(files)} 个文件，即将重命名：")
    for i, f in enumerate(files, 1):
        ext = os.path.splitext(f)[1]
        new_name = f"{i:04d}{ext}"
        print(f"  {f} → {new_name}")

    confirm = input("\n确认重命名？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消。")
        input("按回车退出...")
        return

    for i, f in enumerate(files, 1):
        ext = os.path.splitext(f)[1]
        new_name = f"{i:04d}{ext}"
        os.rename(os.path.join(folder, f), os.path.join(folder, new_name))
        print(f"✓ {f} → {new_name}")

    input("\n完成！按回车退出...")

if __name__ == "__main__":
    main()
