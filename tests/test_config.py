#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器 - 配置管理测试
daily_task_tracker - tests/test_config.py
功能：测试Config类的功能
"""

import os
import sys
import tempfile
import json
from unittest import TestCase

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from daily_task_tracker.config import Config


class TestConfig(TestCase):
    """测试Config类"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 创建临时目录和临时配置文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_config_file = os.path.join(self.temp_dir.name, "test_config.json")
    
    def tearDown(self):
        """测试后的清理工作"""
        self.temp_dir.cleanup()
    
    def test_config_initialization_with_existing_file(self):
        """测试使用现有配置文件初始化"""
        # 创建测试配置文件
        test_config = {
            "data_file": "custom_data.json",
            "default_status": "in_progress",
            "auto_backup": True
        }
        
        with open(self.temp_config_file, "w", encoding="utf-8") as f:
            json.dump(test_config, f)
        
        # 初始化Config实例
        config = Config(self.temp_config_file)
        
        # 验证配置是否正确加载
        self.assertEqual(config.get("data_file"), "custom_data.json")
        self.assertEqual(config.get("default_status"), "in_progress")
        self.assertEqual(config.get("auto_backup"), True)
        
        # 验证默认配置是否被正确合并
        self.assertEqual(config.get("date_format"), "YYYY-MM-DD")  # 这是默认配置
    
    def test_config_initialization_without_existing_file(self):
        """测试没有现有配置文件时的初始化"""
        # 初始化Config实例，配置文件不存在
        config = Config(self.temp_config_file)
        
        # 验证默认配置是否被正确加载
        self.assertEqual(config.get("data_file"), "data/tasks.json")
        self.assertEqual(config.get("default_status"), "pending")
        self.assertEqual(config.get("date_format"), "YYYY-MM-DD")
        self.assertEqual(config.get("auto_backup"), False)
        self.assertEqual(config.get("backup_directory"), "data/backups")
        
        # 验证配置文件是否被创建
        self.assertTrue(os.path.exists(self.temp_config_file))
    
    def test_get_config_value(self):
        """测试获取配置值"""
        config = Config(self.temp_config_file)
        
        # 获取存在的配置值
        self.assertEqual(config.get("data_file"), "data/tasks.json")
        
        # 获取不存在的配置值，使用默认值
        self.assertEqual(config.get("non_existent_key", "default_value"), "default_value")
        
        # 获取不存在的配置值，不使用默认值
        self.assertIsNone(config.get("non_existent_key"))
    
    def test_set_config_value(self):
        """测试设置配置值"""
        config = Config(self.temp_config_file)
        
        # 设置新的配置值
        config.set("data_file", "new_data.json")
        config.set("auto_backup", True)
        config.set("new_key", "new_value")
        
        # 验证配置值是否被正确设置
        self.assertEqual(config.get("data_file"), "new_data.json")
        self.assertEqual(config.get("auto_backup"), True)
        self.assertEqual(config.get("new_key"), "new_value")
        
        # 验证配置是否保存到文件
        with open(self.temp_config_file, "r", encoding="utf-8") as f:
            saved_config = json.load(f)
        
        self.assertEqual(saved_config["data_file"], "new_data.json")
        self.assertEqual(saved_config["auto_backup"], True)
        self.assertEqual(saved_config["new_key"], "new_value")
    
    def test_reset_config(self):
        """测试重置配置"""
        config = Config(self.temp_config_file)
        
        # 修改配置
        config.set("data_file", "new_data.json")
        config.set("auto_backup", True)
        config.set("new_key", "new_value")
        
        # 重置配置
        config.reset()
        
        # 验证配置是否被重置为默认值
        self.assertEqual(config.get("data_file"), "data/tasks.json")
        self.assertEqual(config.get("auto_backup"), False)
        self.assertEqual(config.get("new_key", "not_found"), "not_found")  # 新添加的键应该被移除
    
    def test_update_config(self):
        """测试批量更新配置"""
        config = Config(self.temp_config_file)
        
        # 批量更新配置
        config.update({
            "data_file": "new_data.json",
            "auto_backup": True,
            "backup_directory": "new_backups"
        })
        
        # 验证配置是否被正确更新
        self.assertEqual(config.get("data_file"), "new_data.json")
        self.assertEqual(config.get("auto_backup"), True)
        self.assertEqual(config.get("backup_directory"), "new_backups")
        
        # 验证配置是否保存到文件
        with open(self.temp_config_file, "r", encoding="utf-8") as f:
            saved_config = json.load(f)
        
        self.assertEqual(saved_config["data_file"], "new_data.json")
        self.assertEqual(saved_config["auto_backup"], True)
        self.assertEqual(saved_config["backup_directory"], "new_backups")


if __name__ == "__main__":
    import unittest
    unittest.main()
