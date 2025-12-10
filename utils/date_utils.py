#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器 - 日期工具函数
daily_task_tracker - utils/date_utils.py
功能：提供日期处理相关的工具函数
"""

from datetime import datetime, timedelta
from typing import Optional


def format_date(date_obj: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    将日期对象格式化为字符串
    
    Args:
        date_obj: 日期对象
        format_str: 日期格式字符串
        
    Returns:
        格式化后的日期字符串
    """
    return date_obj.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """
    将字符串解析为日期对象
    
    Args:
        date_str: 日期字符串
        format_str: 日期格式字符串
        
    Returns:
        日期对象，如果解析失败则返回None
    """
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def is_valid_date(date_str: str, format_str: str = "%Y-%m-%d") -> bool:
    """
    验证日期字符串是否有效
    
    Args:
        date_str: 日期字符串
        format_str: 日期格式字符串
        
    Returns:
        如果日期有效返回True，否则返回False
    """
    return parse_date(date_str, format_str) is not None


def get_today_date(format_str: str = "%Y-%m-%d") -> str:
    """
    获取今天的日期字符串
    
    Args:
        format_str: 日期格式字符串
        
    Returns:
        今天的日期字符串
    """
    return format_date(datetime.now(), format_str)


def get_tomorrow_date(format_str: str = "%Y-%m-%d") -> str:
    """
    获取明天的日期字符串
    
    Args:
        format_str: 日期格式字符串
        
    Returns:
        明天的日期字符串
    """
    tomorrow = datetime.now() + timedelta(days=1)
    return format_date(tomorrow, format_str)


def get_date_difference(start_date: str, end_date: str, format_str: str = "%Y-%m-%d") -> Optional[int]:
    """
    计算两个日期之间的天数差
    
    Args:
        start_date: 开始日期字符串
        end_date: 结束日期字符串
        format_str: 日期格式字符串
        
    Returns:
        天数差，如果日期无效则返回None
    """
    start = parse_date(start_date, format_str)
    end = parse_date(end_date, format_str)
    
    if start and end:
        return (end - start).days
    
    return None
