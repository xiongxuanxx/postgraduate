#!/usr/bin/env python3
"""
PNG文件数量检查器（命令行版）
用法: python check_png.py 目录路径 [期望数量]
"""

import os
import sys
from pathlib import Path


def main():
    # 获取命令行参数
    if len(sys.argv) < 2:
        print("用法: python check_png.py 目录路径 [期望数量]")
        print("示例: python check_png.py ./my_batch_results 48")
        return

    root_dir = sys.argv[1]
    expected_count = 48  # 默认值

    if len(sys.argv) >= 3:
        try:
            expected_count = int(sys.argv[2])
        except ValueError:
            print(f"错误: 期望数量必须是整数，而不是 '{sys.argv[2]}'")
            return

    root_path = Path(root_dir)

    # 检查目录是否存在
    if not root_path.exists():
        print(f"错误: 目录不存在: {root_dir}")
        return

    if not root_path.is_dir():
        print(f"错误: 路径不是目录: {root_dir}")
        return

    # 获取所有直接子文件夹
    subfolders = [f for f in root_path.iterdir() if f.is_dir()]

    if not subfolders:
        print(f"警告: 目录中没有子文件夹: {root_dir}")
        return

    # 检查每个子文件夹
    incorrect_folders = []

    for folder in subfolders:
        png_files = list(folder.glob("*.png")) + list(folder.glob("*.PNG"))
        png_count = len(png_files)

        if png_count != expected_count:
            incorrect_folders.append((folder.name, png_count))

    # 输出结果
    if incorrect_folders:
        print(f"发现 {len(incorrect_folders)} 个不正确的文件夹（期望 {expected_count} 张PNG）:")
        for folder_name, png_count in incorrect_folders:
            diff = png_count - expected_count
            if diff < 0:
                print(f"  {folder_name}: {png_count} 张PNG (缺少 {abs(diff)} 张)")
            else:
                print(f"  {folder_name}: {png_count} 张PNG (多出 {diff} 张)")
    else:
        print(f"✅ 所有 {len(subfolders)} 个文件夹都包含 {expected_count} 张PNG图片")


if __name__ == "__main__":
    main()