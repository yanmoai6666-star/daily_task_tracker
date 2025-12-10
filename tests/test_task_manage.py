#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器 - 任务管理测试
daily_task_tracker - tests/test_task_manage.py
功能：测试Task类和TaskManager类的功能
"""

import os
import sys
import json
import tempfile
from unittest import TestCase, mock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from daily_task_tracker.task_manage import Task, TaskManager
from daily_task_tracker.config import Config


class TestTask(TestCase):
    """测试Task类"""
    
    def test_task_creation(self):
        """测试任务创建"""
        task = Task("测试任务", "测试描述", "2025-12-31")
        
        self.assertEqual(task.title, "测试任务")
        self.assertEqual(task.description, "测试描述")
        self.assertEqual(task.due_date, "2025-12-31")
        self.assertEqual(task.status, "pending")
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)
    
    def test_task_to_dict(self):
        """测试任务转换为字典"""
        task = Task("测试任务", "测试描述", "2025-12-31")
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict["title"], "测试任务")
        self.assertEqual(task_dict["description"], "测试描述")
        self.assertEqual(task_dict["due_date"], "2025-12-31")
        self.assertEqual(task_dict["status"], "pending")
        self.assertEqual(task_dict["id"], task.id)
    
    def test_task_from_dict(self):
        """测试从字典创建任务"""
        task_data = {
            "id": "test-id",
            "title": "测试任务",
            "description": "测试描述",
            "status": "in_progress",
            "due_date": "2025-12-31",
            "created_at": "2025-12-01T00:00:00",
            "updated_at": "2025-12-01T12:00:00"
        }
        
        task = Task.from_dict(task_data)
        
        self.assertEqual(task.id, "test-id")
        self.assertEqual(task.title, "测试任务")
        self.assertEqual(task.description, "测试描述")
        self.assertEqual(task.status, "in_progress")
        self.assertEqual(task.due_date, "2025-12-31")
        self.assertEqual(task.created_at, "2025-12-01T00:00:00")
        self.assertEqual(task.updated_at, "2025-12-01T12:00:00")
    
    def test_task_update(self):
        """测试任务更新"""
        task = Task("测试任务", "测试描述", "2025-12-31")
        old_updated_at = task.updated_at
        
        # 更新任务属性
        task.update(title="更新的任务", status="completed", due_date="2025-12-30")
        
        self.assertEqual(task.title, "更新的任务")
        self.assertEqual(task.status, "completed")
        self.assertEqual(task.due_date, "2025-12-30")
        self.assertNotEqual(task.updated_at, old_updated_at)
    
    def test_task_str(self):
        """测试任务的字符串表示"""
        task = Task("测试任务", "测试描述", "2025-12-31")
        task_str = str(task)
        
        self.assertIn("测试任务", task_str)
        self.assertIn("pending", task_str)
        self.assertIn("2025-12-31", task_str)


class TestTaskManager(TestCase):
    """测试TaskManager类"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 创建临时目录和临时配置文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_config_file = os.path.join(self.temp_dir.name, "test_config.json")
        self.temp_data_file = os.path.join(self.temp_dir.name, "tasks.json")
        
        # 创建测试配置
        test_config = {
            "data_file": self.temp_data_file
        }
        
        with open(self.temp_config_file, "w", encoding="utf-8") as f:
            json.dump(test_config, f)
        
        # 创建TaskManager实例
        self.manager = TaskManager(self.temp_config_file)
    
    def tearDown(self):
        """测试后的清理工作"""
        self.temp_dir.cleanup()
    
    def test_add_task(self):
        """测试添加任务"""
        task = self.manager.add_task("测试任务", "测试描述", "2025-12-31")
        
        # 验证任务是否添加成功
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].id, task.id)
        self.assertEqual(self.manager.tasks[0].title, "测试任务")
        
        # 验证数据是否保存到文件
        with open(self.temp_data_file, "r", encoding="utf-8") as f:
            tasks_data = json.load(f)
        
        self.assertEqual(len(tasks_data), 1)
        self.assertEqual(tasks_data[0]["title"], "测试任务")
    
    def test_get_all_tasks(self):
        """测试获取所有任务"""
        # 添加两个任务
        self.manager.add_task("任务1", "描述1", "2025-12-31")
        self.manager.add_task("任务2", "描述2", "2025-12-30")
        
        # 获取所有任务
        tasks = self.manager.get_all_tasks()
        
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "任务1")
        self.assertEqual(tasks[1].title, "任务2")
    
    def test_get_tasks_by_status(self):
        """测试按状态获取任务"""
        # 添加不同状态的任务
        self.manager.add_task("待办任务", "描述1", "2025-12-31", status="pending")
        self.manager.add_task("进行中任务", "描述2", "2025-12-30", status="in_progress")
        self.manager.add_task("已完成任务", "描述3", "2025-12-29", status="completed")
        
        # 获取待办任务
        pending_tasks = self.manager.get_tasks_by_status("pending")
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].title, "待办任务")
        
        # 获取进行中任务
        in_progress_tasks = self.manager.get_tasks_by_status("in_progress")
        self.assertEqual(len(in_progress_tasks), 1)
        self.assertEqual(in_progress_tasks[0].title, "进行中任务")
        
        # 获取已完成任务
        completed_tasks = self.manager.get_tasks_by_status("completed")
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].title, "已完成任务")
    
    def test_search_tasks(self):
        """测试搜索任务"""
        # 添加测试任务
        self.manager.add_task("编写报告", "编写项目报告", "2025-12-31")
        self.manager.add_task("学习Python", "学习Python编程", "2025-12-30")
        self.manager.add_task("参加会议", "参加团队会议", "2025-12-29")
        
        # 搜索包含"学习"的任务
        search_results = self.manager.search_tasks("学习")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].title, "学习Python")
        
        # 搜索包含"会"的任务
        search_results = self.manager.search_tasks("会")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].title, "参加会议")
        
        # 搜索包含"编写"的任务
        search_results = self.manager.search_tasks("编写")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].title, "编写报告")
    
    def test_get_task(self):
        """测试根据ID获取任务"""
        # 添加测试任务
        task = self.manager.add_task("测试任务", "测试描述", "2025-12-31")
        
        # 根据ID获取任务
        retrieved_task = self.manager.get_task(task.id)
        
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, "测试任务")
        
        # 获取不存在的任务
        non_existent_task = self.manager.get_task("non-existent-id")
        self.assertIsNone(non_existent_task)
    
    def test_update_task(self):
        """测试更新任务"""
        # 添加测试任务
        task = self.manager.add_task("测试任务", "测试描述", "2025-12-31")
        
        # 更新任务
        updated_task = self.manager.update_task(task.id, title="更新的任务", status="completed")
        
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "更新的任务")
        self.assertEqual(updated_task.status, "completed")
        
        # 验证任务是否从文件重新加载
        self.manager = TaskManager(self.temp_config_file)
        loaded_task = self.manager.get_task(task.id)
        
        self.assertEqual(loaded_task.title, "更新的任务")
        self.assertEqual(loaded_task.status, "completed")
    
    def test_delete_task(self):
        """测试删除任务"""
        # 添加测试任务
        task = self.manager.add_task("测试任务", "测试描述", "2025-12-31")
        
        # 删除任务
        result = self.manager.delete_task(task.id)
        
        self.assertTrue(result)
        self.assertEqual(len(self.manager.tasks), 0)
        
        # 验证任务是否从文件删除
        self.manager = TaskManager(self.temp_config_file)
        self.assertEqual(len(self.manager.tasks), 0)
        
        # 删除不存在的任务
        result = self.manager.delete_task("non-existent-id")
        self.assertFalse(result)
    
    def test_mark_as_completed(self):
        """测试标记任务为已完成"""
        # 添加测试任务
        task = self.manager.add_task("测试任务", "测试描述", "2025-12-31")
        
        # 标记为已完成
        updated_task = self.manager.mark_as_completed(task.id)
        
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.status, "completed")
    
    def test_mark_as_in_progress(self):
        """测试标记任务为进行中"""
        # 添加测试任务
        task = self.manager.add_task("测试任务", "测试描述", "2025-12-31")
        
        # 标记为进行中
        updated_task = self.manager.mark_as_in_progress(task.id)
        
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.status, "in_progress")
    
    def test_get_overdue_tasks(self):
        """测试获取过期任务"""
        # 添加过期任务
        self.manager.add_task("过期任务", "描述", "2025-01-01")
        
        # 获取过期任务
        overdue_tasks = self.manager.get_overdue_tasks()
        
        self.assertEqual(len(overdue_tasks), 1)
        self.assertEqual(overdue_tasks[0].title, "过期任务")
    
    def test_get_tasks_due_today(self):
        """测试获取今天截止的任务"""
        # 获取今天的日期
        from datetime import datetime
        today = datetime.now().date().strftime("%Y-%m-%d")
        
        # 添加今天截止的任务
        self.manager.add_task("今天的任务", "描述", today)
        
        # 获取今天截止的任务
        today_tasks = self.manager.get_tasks_due_today()
        
        self.assertEqual(len(today_tasks), 1)
        self.assertEqual(today_tasks[0].title, "今天的任务")


if __name__ == "__main__":
    import unittest
    unittest.main()
