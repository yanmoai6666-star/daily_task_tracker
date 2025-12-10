#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器 - 验证工具函数
daily_task_tracker - utils/validation_utils.py
功能：提供任务数据验证相关的工具函数
"""

import uuid
from typing import Optional
from .date_utils import is_valid_date


VALID_TASK_STATUSES = ["pending", "in_progress", "completed"]
MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 1000


def validate_task_title(title: str) -> tuple[bool, Optional[str]]:
    """
    验证任务标题
    
    Args:
        title: 任务标题
        
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(title, str):
        return False, "任务标题必须是字符串"
    
    title = title.strip()
    if not title:
        return False, "任务标题不能为空"
    
    if len(title) < MIN_TITLE_LENGTH:
        return False, f"任务标题长度不能少于 {MIN_TITLE_LENGTH} 个字符"
    
    if len(title) > MAX_TITLE_LENGTH:
        return False, f"任务标题长度不能超过 {MAX_TITLE_LENGTH} 个字符"
    
    return True, None


def validate_task_status(status: str) -> tuple[bool, Optional[str]]:
    """
    验证任务状态
    
    Args:
        status: 任务状态
        
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(status, str):
        return False, "任务状态必须是字符串"
    
    if status not in VALID_TASK_STATUSES:
        return False, f"无效的任务状态，必须是 {', '.join(VALID_TASK_STATUSES)} 之一"
    
    return True, None


def validate_due_date(due_date: Optional[str]) -> tuple[bool, Optional[str]]:
    """
    验证截止日期
    
    Args:
        due_date: 截止日期 (YYYY-MM-DD)，可以为None
        
    Returns:
        (是否有效, 错误信息)
    """
    if due_date is None:
        return True, None
    
    if not isinstance(due_date, str):
        return False, "截止日期必须是字符串"
    
    if not is_valid_date(due_date, "%Y-%m-%d"):
        return False, "截止日期格式无效，必须是 YYYY-MM-DD 格式"
    
    return True, None


def validate_task_id(task_id: str) -> tuple[bool, Optional[str]]:
    """
    验证任务ID
    
    Args:
        task_id: 任务ID
        
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(task_id, str):
        return False, "任务ID必须是字符串"
    
    try:
        uuid.UUID(task_id)
        return True, None
    except ValueError:
        return False, "无效的任务ID格式"


def validate_task_data(title: str, description: Optional[str] = None, 
                      due_date: Optional[str] = None, status: Optional[str] = None) -> dict[str, list[str]]:
    """
    验证完整的任务数据
    
    Args:
        title: 任务标题
        description: 任务描述
        due_date: 截止日期
        status: 任务状态
        
    Returns:
        验证结果字典，包含每个字段的错误信息
    """
    errors = {}
    
    # 验证标题
    is_valid, error = validate_task_title(title)
    if not is_valid and error:
        errors["title"] = [error]
    
    # 验证描述
    if description is not None:
        if not isinstance(description, str):
            errors["description"] = ["任务描述必须是字符串"]
        elif len(description) > MAX_DESCRIPTION_LENGTH:
            errors["description"] = [f"任务描述长度不能超过 {MAX_DESCRIPTION_LENGTH} 个字符"]
    
    # 验证截止日期
    if due_date is not None:
        is_valid, error = validate_due_date(due_date)
        if not is_valid and error:
            errors["due_date"] = [error]
    
    # 验证状态
    if status is not None:
        is_valid, error = validate_task_status(status)
        if not is_valid and error:
            errors["status"] = [error]
    
    return errors
