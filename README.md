# 日常任务追踪器 (Daily Task Tracker)

一个简单易用的命令行工具，帮助你记录、查询和管理日常任务。

## 项目简介

日常任务追踪器是一个轻量级的命令行工具，旨在帮助用户高效管理个人任务。通过简单的命令，你可以添加、查询、更新和删除任务，设置任务状态（待办、进行中、已完成），以及按各种条件筛选任务。

## 功能特点

- 添加新任务，包含标题、描述和截止日期
- 查看所有任务或特定任务的详细信息
- 更新任务信息（标题、描述、截止日期、状态）
- 删除不需要的任务
- 标记任务为"进行中"或"已完成"
- 按状态筛选任务（待办、进行中、已完成）
- 搜索任务（按标题或描述）

## 安装方法

1. 克隆本仓库：
```bash
git clone https://github.com/yourusername/daily-task-tracker.git
cd daily-task-tracker
```

2. 直接使用（无需安装）：
```bash
python3 -m daily_task_tracker.cli --help
```

## 使用指南

### 基本命令格式

```bash
task-cli <command> [options]
```

### 常用命令

#### 添加任务
```bash
# 添加基本任务
task-cli add "完成项目报告"

# 添加带描述和截止日期的任务
task-cli add "购买办公用品" -d "购买打印机墨盒和纸张" -dd 2025-12-12
```

#### 列出任务
```bash
# 列出所有任务
task-cli list

# 或使用别名
task-cli ls

# 按状态筛选任务
task-cli list -s pending   # 列出待办任务
task-cli list -s in_progress  # 列出进行中任务
task-cli list -s completed  # 列出已完成任务

# 搜索任务
task-cli list -q "会议"   # 搜索包含"会议"的任务
```

#### 查看任务详情
```bash
task-cli show 1  # 查看ID为1的任务详情
```

#### 更新任务
```bash
# 更新任务标题
task-cli update 1 -t "更新后的任务标题"

# 更新任务状态
task-cli update 1 -s in_progress

# 更新截止日期
task-cli update 1 -dd 2025-12-31
```

#### 标记任务状态
```bash
# 标记任务为进行中
task-cli start 1

# 标记任务为已完成
task-cli finish 1
```

#### 删除任务
```bash
task-cli delete 1  # 删除ID为1的任务

# 或使用别名
task-cli rm 1
```

#### 搜索任务
```bash
task-cli search "学习"  # 搜索包含"学习"的任务
```

## 项目结构

```
daily_task_tracker/
├── __init__.py           # 包初始化
├── cli.py                # 命令行界面实现
├── config.py             # 配置管理
├── config.json           # 配置文件
├── task_manage.py        # 任务管理核心功能
├── data/
│   └── tasks.json        # 任务数据存储
├── utils/                # 工具函数
│   ├── __init__.py
│   ├── date_utils.py     # 日期处理工具
│   ├── io_utils.py       # 文件操作工具
│   └── validation_utils.py # 数据验证工具
└── tests/                # 测试文件
    ├── test_task_manage.py
    ├── test_config.py
    └── test_utils.py
```

## 开发与测试

运行测试套件：
```bash
# 运行简单测试
python3 daily_task_tracker/test_simple.py

# 运行完整测试
python3 -m unittest discover daily_task_tracker/tests
```

## 版本信息

当前版本：1.0.0

## 许可证

[MIT](LICENSE)
