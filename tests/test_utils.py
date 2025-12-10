#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器 - 工具函数测试
daily_task_tracker - tests/test_utils.py
功能：测试工具函数模块
"""

import os
import sys
import tempfile
import shutil
from unittest import TestCase

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from daily_task_tracker.utils.date_utils import (
    format_date,
    parse_date,
    is_valid_date,
    get_today_date,
    get_tomorrow_date,
    get_date_difference
)

from daily_task_tracker.utils.io_utils import (
    ensure_directory,
    read_json_file,
    write_json_file,
    backup_file
)

from daily_task_tracker.utils.validation_utils import (
    validate_task_title,
    validate_task_status,
    validate_due_date,
    validate_task_id,
    validate_task_data
)
from daily_task_tracker.utils.validation_utils import VALID_TASK_STATUSES


class TestDateUtils(TestCase):
    """测试日期工具函数"""
    
    def test_format_date(self):
        """测试日期格式化"""
        from datetime import datetime
        date_obj = datetime(2025, 12, 31, 14, 30, 45)
        
        formatted_date = format_date(date_obj, "%Y-%m-%d")
        self.assertEqual(formatted_date, "2025-12-31")
        
        formatted_date = format_date(date_obj, "%Y/%m/%d %H:%M:%S")
        self.assertEqual(formatted_date, "2025/12/31 14:30:45")
    
    def test_parse_date(self):
        """测试日期解析"""
        date_str = "2025-12-31"
        
        parsed_date = parse_date(date_str, "%Y-%m-%d")
        self.assertIsNotNone(parsed_date)
        self.assertEqual(parsed_date.year, 2025)
        self.assertEqual(parsed_date.month, 12)
        self.assertEqual(parsed_date.day, 31)
        
        # 测试无效日期
        invalid_date = parse_date("2025-13-31", "%Y-%m-%d")
        self.assertIsNone(invalid_date)
    
    def test_is_valid_date(self):
        """测试日期有效性验证"""
        self.assertTrue(is_valid_date("2025-12-31", "%Y-%m-%d"))
        self.assertTrue(is_valid_date("2025-02-28", "%Y-%m-%d"))
        self.assertFalse(is_valid_date("2025-13-31", "%Y-%m-%d"))
        self.assertFalse(is_valid_date("2025-02-29", "%Y-%m-%d"))  # 2025不是闰年
    
    def test_get_today_date(self):
        """测试获取今天的日期"""
        from datetime import datetime
        today = datetime.now().date().strftime("%Y-%m-%d")
        
        self.assertEqual(get_today_date(), today)
        self.assertEqual(get_today_date("%Y/%m/%d"), today.replace("-", "/"))
    
    def test_get_tomorrow_date(self):
        """测试获取明天的日期"""
        from datetime import datetime, timedelta
        tomorrow = (datetime.now() + timedelta(days=1)).date().strftime("%Y-%m-%d")
        
        self.assertEqual(get_tomorrow_date(), tomorrow)
    
    def test_get_date_difference(self):
        """测试日期差异计算"""
        self.assertEqual(get_date_difference("2025-12-01", "2025-12-10"), 9)
        self.assertEqual(get_date_difference("2025-12-10", "2025-12-01"), -9)
        self.assertEqual(get_date_difference("2025-01-01", "2025-12-31"), 364)
        
        # 测试无效日期
        self.assertIsNone(get_date_difference("2025-13-01", "2025-12-31"))


class TestIOUtils(TestCase):
    """测试IO工具函数"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """测试后的清理工作"""
        self.temp_dir.cleanup()
    
    def test_ensure_directory(self):
        """测试确保目录存在"""
        new_dir = os.path.join(self.temp_dir.name, "new_dir", "sub_dir")
        ensure_directory(new_dir)
        
        self.assertTrue(os.path.exists(new_dir))
    
    def test_read_json_file(self):
        """测试读取JSON文件"""
        # 创建测试JSON文件
        test_data = {"key": "value", "number": 42}
        test_file = os.path.join(self.temp_dir.name, "test.json")
        
        with open(test_file, "w", encoding="utf-8") as f:
            import json
            json.dump(test_data, f)
        
        # 读取JSON文件
        read_data = read_json_file(test_file)
        
        self.assertEqual(read_data, test_data)
        
        # 读取不存在的文件
        self.assertIsNone(read_json_file(os.path.join(self.temp_dir.name, "non_existent.json")))
        
        # 读取无效JSON文件
        invalid_file = os.path.join(self.temp_dir.name, "invalid.json")
        with open(invalid_file, "w", encoding="utf-8") as f:
            f.write("{invalid json}")
        
        self.assertIsNone(read_json_file(invalid_file))
    
    def test_write_json_file(self):
        """测试写入JSON文件"""
        # 测试数据
        test_data = {"key": "value", "number": 42}
        test_file = os.path.join(self.temp_dir.name, "test.json")
        
        # 写入JSON文件
        result = write_json_file(test_file, test_data)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(test_file))
        
        # 验证文件内容
        with open(test_file, "r", encoding="utf-8") as f:
            import json
            read_data = json.load(f)
        
        self.assertEqual(read_data, test_data)
        
        # 测试写入到不存在的目录
        new_dir_file = os.path.join(self.temp_dir.name, "new_dir", "test.json")
        result = write_json_file(new_dir_file, test_data)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(new_dir_file))
    
    def test_backup_file(self):
        """测试文件备份"""
        # 创建测试文件
        test_file = os.path.join(self.temp_dir.name, "test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("test content")
        
        # 备份文件
        backup_dir = os.path.join(self.temp_dir.name, "backups")
        backup_path = backup_file(test_file, backup_dir)
        
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))
        
        # 验证备份文件内容
        with open(backup_path, "r", encoding="utf-8") as f:
            backup_content = f.read()
        
        self.assertEqual(backup_content, "test content")
        
        # 测试备份不存在的文件
        self.assertIsNone(backup_file(os.path.join(self.temp_dir.name, "non_existent.txt"), backup_dir))


class TestValidationUtils(TestCase):
    """测试验证工具函数"""
    
    def test_validate_task_title(self):
        """测试任务标题验证"""
        # 有效标题
        is_valid, error = validate_task_title("有效的任务标题")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        # 空标题
        is_valid, error = validate_task_title("")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # 太短的标题
        is_valid, error = validate_task_title("a")
        self.assertTrue(is_valid)  # 最短长度是1
        
        # 太长的标题
        long_title = "a" * 200
        is_valid, error = validate_task_title(long_title)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # 非字符串标题
        is_valid, error = validate_task_title(123)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_task_status(self):
        """测试任务状态验证"""
        # 有效状态
        for status in VALID_TASK_STATUSES:
            is_valid, error = validate_task_status(status)
            self.assertTrue(is_valid)
            self.assertIsNone(error)
        
        # 无效状态
        is_valid, error = validate_task_status("invalid_status")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # 非字符串状态
        is_valid, error = validate_task_status(123)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_due_date(self):
        """测试截止日期验证"""
        # None值
        is_valid, error = validate_due_date(None)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        # 有效日期
        is_valid, error = validate_due_date("2025-12-31")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        # 无效日期格式
        is_valid, error = validate_due_date("2025/12/31")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # 无效日期
        is_valid, error = validate_due_date("2025-13-31")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # 非字符串日期
        is_valid, error = validate_due_date(123)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_task_id(self):
        """测试任务ID验证"""
        # 有效UUID
        valid_id = "550e8400-e29b-41d4-a716-446655440000"
        is_valid, error = validate_task_id(valid_id)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        # 无效UUID
        is_valid, error = validate_task_id("invalid-uuid")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # 非字符串ID
        is_valid, error = validate_task_id(123)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_task_data(self):
        """测试完整任务数据验证"""
        # 有效数据
        errors = validate_task_data(
            title="有效的任务标题",
            description="有效的任务描述",
            due_date="2025-12-31",
            status="pending"
        )
        
        self.assertEqual(errors, {})
        
        # 无效数据
        errors = validate_task_data(
            title="",
            description="a" * 2000,  # 太长的描述
            due_date="2025-13-31",  # 无效日期
            status="invalid_status"  # 无效状态
        )
        
        self.assertIn("title", errors)
        self.assertIn("description", errors)
        self.assertIn("due_date", errors)
        self.assertIn("status", errors)


if __name__ == "__main__":
    import unittest
    unittest.main()
