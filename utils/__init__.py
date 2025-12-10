#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器 - 工具函数模块
daily_task_tracker - utils/__init__.py
功能：提供各种工具函数的统一入口
"""

# 导入工具函数模块
from .date_utils import (
    format_date,
    parse_date,
    is_valid_date,
    get_today_date,
    get_tomorrow_date,
    get_date_difference
)

from .io_utils import (
    ensure_directory,
    read_json_file,
    write_json_file,
    backup_file
)

from .validation_utils import (
    validate_task_title,
    validate_task_status,
    validate_due_date,
    validate_task_id
)

# 导出所有工具函数
__all__ = [
    # date_utils
    'format_date',
    'parse_date',
    'is_valid_date',
    'get_today_date',
    'get_tomorrow_date',
    'get_date_difference',
    # io_utils
    'ensure_directory',
    'read_json_file',
    'write_json_file',
    'backup_file',
    # validation_utils
    'validate_task_title',
    'validate_task_status',
    'validate_due_date',
    'validate_task_id'
]
