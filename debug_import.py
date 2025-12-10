#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本，用于捕获完整的导入错误信息
"""

import traceback

try:
    # 尝试导入模块
    from task_manage import Task, TaskManager
    from config import Config
    
    print("所有模块导入成功!")
    
    # 尝试创建实例
    task = Task("测试任务", "测试描述", "2025-12-31")
    print(f"Task实例创建成功: {task}")
    
    config = Config()
    print(f"Config实例创建成功")
    
    manager = TaskManager()
    print(f"TaskManager实例创建成功")
    
except Exception as e:
    print(f"导入错误: {type(e).__name__}: {e}")
    print("\n完整的错误堆栈:")
    traceback.print_exc()