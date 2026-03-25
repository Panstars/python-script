#!/usr/bin/env python3
"""
给当前文件夹下所有文件名前加数字0
例如：file.txt → 0file.txt
"""
import os
import sys

def add_zero_prefix():
    """给当前目录下所有文件添加0前缀"""
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 获取所有文件（不包括子目录）
    files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    
    # 过滤掉隐藏文件和脚本自身
    files = [f for f in files if not f.startswith('.') and f != os.path.basename(__file__)]
    
    if not files:
        print("当前目录没有可处理的文件")
        return
    
    print(f"找到 {len(files)} 个文件:")
    for f in files:
        print(f"  {f}")
    
    # 确认
    response = input(f"\n确认给这 {len(files)} 个文件添加 '0' 前缀？(y/n): ")
    if response.lower() != 'y':
        print("取消操作")
        return
    
    # 重命名
    renamed_count = 0
    for filename in files:
        new_name = f"0{filename}"
        old_path = os.path.join(current_dir, filename)
        new_path = os.path.join(current_dir, new_name)
        
        try:
            os.rename(old_path, new_path)
            print(f"✓ {filename} → {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"✗ 重命名 {filename} 失败: {e}")
    
    print(f"\n完成！重命名了 {renamed_count} 个文件")

if __name__ == "__main__":
    add_zero_prefix()