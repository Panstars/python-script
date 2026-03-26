import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import wave

def get_wav_duration(filepath):
    try:
        with wave.open(filepath, 'rb') as w:
            frames = w.getnframes()
            rate = w.getframerate()
            duration = frames / float(rate)
            return duration
    except Exception:
        return None

def format_duration(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"

def main():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder = filedialog.askdirectory(title="选择音频文件夹")
    root.destroy()

    if not folder:
        print("未选择文件夹，退出。")
        input("按回车退出...")
        return

    wav_files = []
    for f in os.listdir(folder):
        if f.lower().endswith('.wav'):
            wav_files.append(f)

    if not wav_files:
        print("文件夹中没有 .wav 文件。")
        input("按回车退出...")
        return

    wav_files.sort()
    results = []
    total_duration = 0
    durations = []

    print(f"正在统计 {len(wav_files)} 个 wav 文件...\n")

    for i, filename in enumerate(wav_files, 1):
        filepath = os.path.join(folder, filename)
        dur = get_wav_duration(filepath)
        if dur is not None:
            durations.append(dur)
            total_duration += dur
            results.append(f"{i:04d}. {filename}: {format_duration(dur)}")
        else:
            results.append(f"{i:04d}. {filename}: 读取失败")

    avg_dur = total_duration / len(durations) if durations else 0

    print("=" * 60)
    print(f"文件夹: {folder}")
    print(f" wav 文件数: {len(wav_files)}")
    print("=" * 60)
    for r in results:
        print(r)
    print("=" * 60)
    print(f"总时长: {format_duration(total_duration)}")
    print(f"平均时长: {format_duration(avg_dur)}")
    print("=" * 60)
    input("\n按回车退出...")

if __name__ == "__main__":
    main()
