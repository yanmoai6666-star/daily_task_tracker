#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器 (Daily Task Tracker)
用于记录、查询、删除等个人日常任务的基础管理工具
"""

__version__ = "1.0.0"
__author__ = "Daily Task Tracker Team"
__description__ = "一个简单易用的日常任务追踪工具"

# 导入主要模块
from .task_manage import Task, TaskManager
from .config import Config

# 定义包级别的便捷函数
def create_manager():
    """创建一个TaskManager实例"""
    return TaskManager()

def get_config():
    """获取配置实例"""
    return Config()
