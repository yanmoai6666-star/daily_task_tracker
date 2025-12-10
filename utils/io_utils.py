#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器 - IO工具函数
daily_task_tracker - utils/io_utils.py
功能：提供文件操作相关的工具函数
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional


def ensure_directory(directory_path: str) -> None:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        directory_path: 目录路径
    """
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
        except OSError as e:
            print(f"创建目录失败 {directory_path}: {e}")


def read_json_file(file_path: str) -> Optional[Any]:
    """
    读取JSON文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        JSON数据，如果读取失败则返回None
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"读取JSON文件失败 {file_path}: {e}")
    return None


def write_json_file(file_path: str, data: Any, indent: int = 2) -> bool:
    """
    写入JSON文件
    
    Args:
        file_path: JSON文件路径
        data: 要写入的数据
        indent: 缩进空格数
        
    Returns:
        如果写入成功返回True，否则返回False
    """
    try:
        # 确保目录存在
        ensure_directory(os.path.dirname(file_path))
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except IOError as e:
        print(f"写入JSON文件失败 {file_path}: {e}")
        return False


def backup_file(file_path: str, backup_dir: str = "backups") -> Optional[str]:
    """
    备份文件
    
    Args:
        file_path: 要备份的文件路径
        backup_dir: 备份目录路径
        
    Returns:
        备份文件路径，如果备份失败则返回None
    """
    if not os.path.exists(file_path):
        return None
    
    try:
        # 确保备份目录存在
        ensure_directory(backup_dir)
        
        # 生成备份文件名，包含时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        backup_filename = f"{name}_{timestamp}{ext}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # 复制文件到备份目录
        shutil.copy2(file_path, backup_path)
        return backup_path
    except (IOError, shutil.Error) as e:
        print(f"备份文件失败 {file_path}: {e}")
        return None
