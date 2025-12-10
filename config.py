#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器配置管理
daily_task_tracker - config.py
功能：管理应用程序的配置设置
"""

import os
import json
from typing import Dict, Any, Optional


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.default_config = {
            "data_file": "data/tasks.json",
            "default_status": "pending",
            "date_format": "YYYY-MM-DD",
            "auto_backup": False,
            "backup_directory": "data/backups"
        }
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    # 合并默认配置和加载的配置
                    return {**self.default_config, **loaded_config}
            except (json.JSONDecodeError, IOError):
                # 如果配置文件无效，使用默认配置
                return self.default_config.copy()
        else:
            # 如果配置文件不存在，创建默认配置文件
            self._save_config(self.default_config)
            return self.default_config.copy()
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """
        保存配置到文件
        
        Args:
            config: 配置字典
        """
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except IOError:
            # 保存失败时不抛出异常，使用内存中的配置
            pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        设置配置项
        
        Args:
            key: 配置键
            value: 配置值
        """
        self.config[key] = value
        self._save_config(self.config)
    
    def reset(self) -> None:
        """
        重置配置为默认值
        """
        self.config = self.default_config.copy()
        self._save_config(self.config)
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        批量更新配置项
        
        Args:
            updates: 配置更新字典
        """
        self.config.update(updates)
        self._save_config(self.config)
    
    def __getitem__(self, key: str) -> Any:
        """
        支持通过索引方式获取配置项
        
        Args:
            key: 配置键
            
        Returns:
            配置值
        """
        return self.config[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        支持通过索引方式设置配置项
        
        Args:
            key: 配置键
            value: 配置值
        """
        self.set(key, value)


# 创建全局配置实例
config = Config()


if __name__ == "__main__":
    # 测试配置功能
    print("当前配置:")
    print(f"数据文件路径: {config['data_file']}")
    print(f"默认任务状态: {config['default_status']}")
    print(f"日期格式: {config['date_format']}")
    print(f"自动备份: {config['auto_backup']}")
    print(f"备份目录: {config['backup_directory']}")
    
    # 更新配置
    config['auto_backup'] = True
    print(f"\n更新后自动备份: {config['auto_backup']}")
    
    # 重置配置
    # config.reset()
    # print(f"\n重置后自动备份: {config['auto_backup']}")