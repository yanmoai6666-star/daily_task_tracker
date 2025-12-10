#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日常任务追踪器命令行界面
daily_task_tracker - cli.py
功能：提供命令行交互界面，方便用户操作任务
"""

import argparse
import sys
import datetime
from task_manage import TaskManager, Task


def print_task(task: Task) -> None:
    """打印单个任务的详细信息"""
    print(f"\n任务ID: {task.id}")
    print(f"标题: {task.title}")
    print(f"描述: {task.description}")
    print(f"状态: {task.status}")
    print(f"截止日期: {task.due_date if task.due_date else '无'}")
    print(f"创建时间: {datetime.datetime.fromisoformat(task.created_at).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"更新时间: {datetime.datetime.fromisoformat(task.updated_at).strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)


def print_tasks(tasks: list[Task]) -> None:
    """打印任务列表"""
    if not tasks:
        print("没有找到任务")
        return
    
    print(f"\n找到 {len(tasks)} 个任务:")
    print("-" * 80)
    print(f"{'ID':<5} {'状态':<12} {'标题':<30} {'截止日期':<15} {'创建时间':<20}")
    print("-" * 80)
    
    for task in tasks:
        status_emoji = {
            "pending": "⏳ 待办",
            "in_progress": "🔄 进行中",
            "completed": "✅ 已完成"
        }
        due_date = task.due_date if task.due_date else "无"
        created_at = datetime.datetime.fromisoformat(task.created_at).strftime("%Y-%m-%d %H:%M")
        
        print(f"{task.id:<5} {status_emoji.get(task.status, task.status):<12} {task.title:<30.30} {due_date:<15} {created_at:<20}")
    
    print("-" * 80)


def add_task_command(args: argparse.Namespace) -> None:
    """处理添加任务命令"""
    manager = TaskManager()
    task = manager.add_task(args.title, args.description, args.due_date)
    print(f"✅ 成功添加任务: {task.title} (ID: {task.id})")


def list_tasks_command(args: argparse.Namespace) -> None:
    """处理列出任务命令"""
    manager = TaskManager()
    
    if args.status:
        tasks = manager.get_tasks_by_status(args.status)
    elif args.search:
        tasks = manager.search_tasks(args.search)
    else:
        tasks = manager.get_all_tasks()
    
    print_tasks(tasks)


def show_task_command(args: argparse.Namespace) -> None:
    """处理查看任务详情命令"""
    manager = TaskManager()
    task = manager.get_task(args.id)
    
    if task:
        print_task(task)
    else:
        print(f"❌ 找不到ID为 {args.id} 的任务")


def update_task_command(args: argparse.Namespace) -> None:
    """处理更新任务命令"""
    manager = TaskManager()
    
    # 收集要更新的字段
    update_fields = {}
    if args.title is not None:
        update_fields["title"] = args.title
    if args.description is not None:
        update_fields["description"] = args.description
    if args.due_date is not None:
        update_fields["due_date"] = args.due_date
    if args.status is not None:
        update_fields["status"] = args.status
    
    if not update_fields:
        print("❌ 没有提供要更新的字段")
        return
    
    updated_task = manager.update_task(args.id, **update_fields)
    
    if updated_task:
        print(f"✅ 成功更新任务 (ID: {updated_task.id})")
        print_task(updated_task)
    else:
        print(f"❌ 找不到ID为 {args.id} 的任务")


def delete_task_command(args: argparse.Namespace) -> None:
    """处理删除任务命令"""
    manager = TaskManager()
    success = manager.delete_task(args.id)
    
    if success:
        print(f"🗑️  成功删除ID为 {args.id} 的任务")
    else:
        print(f"❌ 找不到ID为 {args.id} 的任务")


def mark_in_progress_command(args: argparse.Namespace) -> None:
    """处理标记任务为进行中命令"""
    manager = TaskManager()
    updated_task = manager.update_task(args.id, status="in_progress")
    
    if updated_task:
        print(f"🔄 已将任务 {updated_task.title} (ID: {updated_task.id}) 标记为进行中")
    else:
        print(f"❌ 找不到ID为 {args.id} 的任务")


def mark_completed_command(args: argparse.Namespace) -> None:
    """处理标记任务为已完成命令"""
    manager = TaskManager()
    updated_task = manager.update_task(args.id, status="completed")
    
    if updated_task:
        print(f"✅ 已将任务 {updated_task.title} (ID: {updated_task.id}) 标记为已完成")
    else:
        print(f"❌ 找不到ID为 {args.id} 的任务")


def search_tasks_command(args: argparse.Namespace) -> None:
    """处理搜索任务命令"""
    manager = TaskManager()
    tasks = manager.search_tasks(args.keyword)
    print_tasks(tasks)


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="日常任务追踪器 - 命令行工具",
        usage="task-cli <command> [options]"
    )
    
    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 添加任务命令
    add_parser = subparsers.add_parser("add", help="添加新任务")
    add_parser.add_argument("title", help="任务标题")
    add_parser.add_argument("-d", "--description", default="", help="任务描述")
    add_parser.add_argument("-dd", "--due-date", help="截止日期 (格式: YYYY-MM-DD)")
    add_parser.set_defaults(func=add_task_command)
    
    # 列出任务命令
    list_parser = subparsers.add_parser("list", aliases=["ls"], help="列出所有任务")
    list_parser.add_argument("-s", "--status", choices=["pending", "in_progress", "completed"], help="按状态过滤任务")
    list_parser.add_argument("-q", "--search", help="搜索任务标题或描述")
    list_parser.set_defaults(func=list_tasks_command)
    
    # 查看任务详情命令
    show_parser = subparsers.add_parser("show", help="查看任务详情")
    show_parser.add_argument("id", type=int, help="任务ID")
    show_parser.set_defaults(func=show_task_command)
    
    # 更新任务命令
    update_parser = subparsers.add_parser("update", aliases=["edit"], help="更新任务信息")
    update_parser.add_argument("id", type=int, help="任务ID")
    update_parser.add_argument("-t", "--title", help="新的任务标题")
    update_parser.add_argument("-d", "--description", help="新的任务描述")
    update_parser.add_argument("-dd", "--due-date", help="新的截止日期 (格式: YYYY-MM-DD)")
    update_parser.add_argument("-s", "--status", choices=["pending", "in_progress", "completed"], help="新的任务状态")
    update_parser.set_defaults(func=update_task_command)
    
    # 删除任务命令
    delete_parser = subparsers.add_parser("delete", aliases=["rm"], help="删除任务")
    delete_parser.add_argument("id", type=int, help="任务ID")
    delete_parser.set_defaults(func=delete_task_command)
    
    # 标记任务为进行中命令
    in_progress_parser = subparsers.add_parser("start", help="标记任务为进行中")
    in_progress_parser.add_argument("id", type=int, help="任务ID")
    in_progress_parser.set_defaults(func=mark_in_progress_command)
    
    # 标记任务为已完成命令
    completed_parser = subparsers.add_parser("finish", help="标记任务为已完成")
    completed_parser.add_argument("id", type=int, help="任务ID")
    completed_parser.set_defaults(func=mark_completed_command)
    
    # 搜索任务命令
    search_parser = subparsers.add_parser("search", help="搜索任务")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.set_defaults(func=search_tasks_command)
    
    # 如果没有提供命令，显示帮助信息
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    # 解析命令行参数并执行相应的函数
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()