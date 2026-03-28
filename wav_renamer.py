#!/usr/bin/env python3
"""
WAV 文件重编号工具 - 可视化界面
功能：选择文件夹，预览修改，应用编号
"""

import os
import re
import PySimpleGUI as sg
from pathlib import Path
from datetime import datetime

sg.theme('LightBlue3')

def get_wav_files(folder_path):
    """获取文件夹中所有 WAV 文件"""
    wav_files = []
    if os.path.isdir(folder_path):
        for f in sorted(os.listdir(folder_path)):
            if f.lower().endswith('.wav'):
                wav_files.append(f)
    return wav_files

def generate_new_name(original_name, start_num, digits, prefix, keep_original, keep_length):
    """生成新文件名"""
    # 提取原文件名（不含扩展名）
    name_without_ext = Path(original_name).stem
    
    # 计算新编号
    new_num = start_num
    
    # 构建新文件名
    if prefix:
        new_name = f"{prefix}{new_num:0{digits}d}"
    else:
        new_name = f"{new_num:0{digits}d}"
    
    # 如果要保留原文件名的部分
    if keep_original and keep_length > 0:
        # 保留原文件名的前 N 个字符
        new_name = f"{new_name}_{name_without_ext[:keep_length]}"
    
    return f"{new_name}.wav"

def main():
    # 布局定义
    layout = [
        # 文件夹选择
        [
            sg.Text('文件夹:', size=(8, 1)),
            sg.Input(key='-FOLDER-', size=(50, 1), readonly=True),
            sg.FolderBrowse('选择文件夹', key='-BROWSE-')
        ],
        
        # 设置面板
        sg.Frame('编号设置', [
            [
                sg.Text('起始数字:', size=(8, 1)),
                sg.Spin(values=list(range(0, 10000)), initial_value=1, size=(8, 1), key='-START_NUM-'),
                sg.Text('  数字位数:', size=(8, 1)),
                sg.Combo(['3', '4', '5', '6'], default_value='4', size=(6, 1), key='-DIGITS-'),
            ],
            [
                sg.Text('前缀:', size=(8, 1)),
                sg.Input(default_text='', size=(20, 1), key='-PREFIX-'),
                sg.Text('  保留原名:', size=(10, 1)),
                sg.Checkbox('', default=False, key='-KEEP_ORIGINAL-'),
                sg.Spin(values=list(range(0, 20)), initial_value=4, size=(4, 1), key='-KEEP_LENGTH-'),
                sg.Text('个字符', size=(6, 1)),
            ],
        ]),
        
        # 刷新按钮
        [sg.Button('刷新文件列表', key='-REFRESH-')],
        
        # 文件列表预览
        sg.Frame('预览', [
            [sg.Text('原文件名', size=(30, 1), font=('Helvetica', 10, 'bold'))],
            [sg.Text('  ↓', font=('Helvetica', 10, 'bold'), text_color='green')],
            [sg.Text('新文件名', size=(30, 1), font=('Helvetica', 10, 'bold'))],
            [sg.Listbox(values=[], size=(50, 10), key='-PREVIEW-', font=('Courier', 10))],
        ]),
        
        # 操作按钮
        [
            sg.Button('预览修改', key='-PREVIEW-', button_color=('white', 'green')),
            sg.Button('应用修改', key='-APPLY-', button_color=('white', 'blue')),
            sg.Button('重置', key='-RESET-'),
            sg.Button('退出', key='-EXIT-')
        ],
        
        # 状态栏
        [sg.StatusBar('就绪', key='-STATUS-', size=(50, 1))],
    ]
    
    window = sg.Window('WAV 文件重编号工具', layout, finalize=True)
    
    current_folder = ''
    wav_files = []
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, '-EXIT-'):
            break
        
        elif event == '-BROWSE-':
            current_folder = values['-FOLDER-']
            window['-FOLDER-'].update(current_folder)
            if current_folder:
                wav_files = get_wav_files(current_folder)
                window['-STATUS-'].update(f'已加载 {len(wav_files)} 个 WAV 文件')
        
        elif event == '-REFRESH-':
            if current_folder:
                wav_files = get_wav_files(current_folder)
                window['-STATUS-'].update(f'已刷新 {len(wav_files)} 个 WAV 文件')
        
        elif event == '-PREVIEW-':
            if not wav_files:
                window['-STATUS-'].update('请先选择文件夹')
                continue
            
            start_num = int(values['-START_NUM-'])
            digits = int(values['-DIGITS-'])
            prefix = values['-PREFIX-']
            keep_original = values['-KEEP_ORIGINAL-']
            keep_length = int(values['-KEEP_LENGTH-'])
            
            preview_items = []
            for i, wav_file in enumerate(wav_files):
                new_name = generate_new_name(
                    wav_file, 
                    start_num + i, 
                    digits, 
                    prefix, 
                    keep_original, 
                    keep_length
                )
                preview_items.append(f'{wav_file:<40} → {new_name}')
            
            window['-PREVIEW-'].update(values=preview_items)
            window['-STATUS-'].update(f'预览 {len(preview_items)} 个文件')
        
        elif event == '-APPLY-':
            if not wav_files:
                window['-STATUS-'].update('请先选择文件夹')
                continue
            
            start_num = int(values['-START_NUM-'])
            digits = int(values['-DIGITS-'])
            prefix = values['-PREFIX-']
            keep_original = values['-KEEP_ORIGINAL-']
            keep_length = int(values['-KEEP_LENGTH-'])
            
            # 确认对话框
            confirm = sg.popup_yes_no(
                f'确定要重命名 {len(wav_files)} 个文件吗？\n\n此操作不可撤销！',
                title='确认修改'
            )
            
            if confirm == 'Yes':
                renamed_count = 0
                errors = []
                
                for i, wav_file in enumerate(wav_files):
                    try:
                        new_name = generate_new_name(
                            wav_file,
                            start_num + i,
                            digits,
                            prefix,
                            keep_original,
                            keep_length
                        )
                        
                        old_path = os.path.join(current_folder, wav_file)
                        new_path = os.path.join(current_folder, new_name)
                        
                        if old_path != new_path:
                            os.rename(old_path, new_path)
                            renamed_count += 1
                    
                    except Exception as e:
                        errors.append(f'{wav_file}: {str(e)}')
                
                # 刷新文件列表
                wav_files = get_wav_files(current_folder)
                window['-PREVIEW-'].update(values=[])
                
                if errors:
                    sg.popup(f'完成！成功: {renamed_count} 个\n错误: {len(errors)} 个\n\n' + '\n'.join(errors))
                else:
                    sg.popup(f'完成！成功重命名 {renamed_count} 个文件')
                
                window['-STATUS-'].update(f'已完成 {renamed_count} 个文件的重命名')
        
        elif event == '-RESET-':
            window['-START_NUM-'].update(1)
            window['-DIGITS-'].update('4')
            window['-PREFIX-'].update('')
            window['-KEEP_ORIGINAL-'].update(False)
            window['-KEEP_LENGTH-'].update(4)
            window['-PREVIEW-'].update(values=[])
            window['-STATUS-'].update('已重置')
    
    window.close()

if __name__ == '__main__':
    main()
