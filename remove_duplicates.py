#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
递归删除文件夹中的重复文件

此脚本会递归扫描指定文件夹中的所有文件，
计算每个文件的哈希值，找出内容完全相同的文件，
并提供删除重复文件的选项。
"""

import os
import sys
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict


def calculate_file_hash(file_path, block_size=65536):
    """
    计算文件的SHA256哈希值
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()
    except Exception as e:
        print(f"无法计算文件哈希值: {file_path}. 错误: {e}")
        return None


def find_duplicate_files(directory):
    """
    递归查找目录中的重复文件
    返回一个字典，键为哈希值，值为具有相同哈希值的文件路径列表
    """
    hash_dict = defaultdict(list)
    file_count = 0
    processed_count = 0
    
    # 获取所有文件路径
    all_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            all_files.append(file_path)
    
    file_count = len(all_files)
    print(f"找到 {file_count} 个文件，开始计算哈希值...")
    
    # 计算每个文件的哈希值
    for file_path in all_files:
        processed_count += 1
        if processed_count % 100 == 0 or processed_count == file_count:
            print(f"已处理: {processed_count}/{file_count} 文件")
        
        file_hash = calculate_file_hash(file_path)
        if file_hash:
            hash_dict[file_hash].append(file_path)
    
    # 只保留有重复的哈希值
    duplicate_dict = {k: v for k, v in hash_dict.items() if len(v) > 1}
    return duplicate_dict


def format_size(size_bytes):
    """
    将字节大小格式化为人类可读的格式
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024 or unit == 'TB':
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024


def main():
    parser = argparse.ArgumentParser(description='递归删除文件夹中的重复文件')
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='要扫描的目录路径 (默认为当前目录)')
    parser.add_argument('-d', '--delete', action='store_true',
                        help='自动删除重复文件 (保留每组中的第一个文件)')
    args = parser.parse_args()
    
    directory = os.path.abspath(args.directory)
    
    if not os.path.isdir(directory):
        print(f"错误: '{directory}' 不是一个有效的目录路径!")
        return 1
    
    print(f"开始扫描目录: {directory}")
    
    # 查找重复文件
    duplicate_files = find_duplicate_files(directory)
    
    if not duplicate_files:
        print("未找到重复文件。")
        return 0
    
    # 统计重复文件数量和总大小
    total_duplicates = 0
    total_wasted_size = 0
    
    for file_list in duplicate_files.values():
        # 每组重复文件中，第一个保留，其余都是重复的
        duplicate_count = len(file_list) - 1
        total_duplicates += duplicate_count
        
        # 计算浪费的空间
        file_size = os.path.getsize(file_list[0])
        wasted_size = file_size * duplicate_count
        total_wasted_size += wasted_size
    
    print(f"\n找到 {total_duplicates} 个重复文件，占用空间: {format_size(total_wasted_size)}")
    
    # 显示重复文件列表
    print("\n重复文件列表:")
    group_index = 1
    
    for hash_value, file_list in duplicate_files.items():
        if len(file_list) > 1:
            print(f"\n组 {group_index} (哈希值: {hash_value[:8]}...)")
            print(f"  原始文件 (将保留): {file_list[0]}")
            print(f"  大小: {format_size(os.path.getsize(file_list[0]))}")
            print("  重复文件 (将删除):")
            
            for i, duplicate in enumerate(file_list[1:], 1):
                print(f"    {i}. {duplicate}")
            
            group_index += 1
    
    # 删除重复文件
    if args.delete:
        delete_mode = 'y'
    else:
        delete_mode = input("\n是否要删除所有重复文件? (y/n): ").lower()
    
    if delete_mode == 'y':
        deleted_count = 0
        deleted_size = 0
        
        for file_list in duplicate_files.values():
            # 保留第一个文件，删除其余重复文件
            for duplicate in file_list[1:]:
                try:
                    file_size = os.path.getsize(duplicate)
                    os.remove(duplicate)
                    deleted_count += 1
                    deleted_size += file_size
                    print(f"已删除: {duplicate}")
                except Exception as e:
                    print(f"无法删除文件: {duplicate}. 错误: {e}")
        
        print(f"\n操作完成! 已删除 {deleted_count} 个重复文件，释放空间: {format_size(deleted_size)}")
    else:
        print("操作已取消，未删除任何文件。")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())



#  [目录路径] [-d/--delete]

# python remove_duplicates.py E:\BaiduNetdiskDownload -d