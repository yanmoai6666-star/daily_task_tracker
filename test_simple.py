#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本，用于验证项目是否能正常工作
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from daily_task_tracker import create_manager
from daily_task_tracker.task_manage import Task

print("测试1: 创建Task实例")
task = Task("测试任务", "测试描述", "2025-12-31")
print(f"任务创建成功: {task}")

print("\n测试2: 创建TaskManager实例")
manager = create_manager()
print(f"管理器创建成功")

print("\n测试3: 添加任务")
added_task = manager.add_task("新任务", "新任务描述", "2025-12-31")
print(f"任务添加成功: {added_task}")

print("\n测试4: 获取所有任务")
tasks = manager.get_all_tasks()
print(f"当前共有 {len(tasks)} 个任务")
for t in tasks:
    print(f"- {t}")

print("\n测试5: 删除任务")
result = manager.delete_task(added_task.id)
print(f"任务删除 {'成功' if result else '失败'}")

print("\n所有测试完成!")