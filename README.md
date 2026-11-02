# CS 教学智能体（teaching-agent）

计算机类课程教学智能体 —— 知识点自动整理与标签检索。

## 功能简介

教师上传课程文档（Markdown / TXT / PDF），系统调用大模型（云 API）自动完成：

1. **知识点抽取**：从文档中提取结构化知识点（标题 + 内容摘要）；
2. **自动打标**：为每个知识点生成 3~5 个标签（tag）；
3. **标签检索**：学生按 tag 搜索对应知识点。

## 技术栈

| 层 | 选型 | 说明 |
|---|---|---|
| Web 框架 | Django 5 | 单体应用，前后端不分离（本作业只做 API 骨架） |
| 数据库 | MySQL 8（开发期可用 SQLite） | 存文档、知识点、标签 |
| 大模型 | 云端 API（OpenAI 兼容接口） | 不部署本地模型，无需 GPU |
| 部署 | Docker + K8s | Master + Worker 架构，Worker 负责异步抽取任务 |

## 项目结构

```
teaching-agent/
├── README.md
├── Makefile              # 常用命令封装
├── requirements.txt
├── manage.py
├── config/               # Django 项目配置
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── documents/        # 文档上传与大模型抽取
│   │   ├── models.py     # Document
│   │   ├── services.py   # LLM 调用封装（打知识点 + 打 tag）
│   │   └── views.py
│   └── knowledge/        # 知识点与标签检索
│       ├── models.py     # KnowledgePoint / Tag
│       └── views.py      # /api/knowledge/?tag=xxx
└── docs/
    └── 设计方案.md        # 项目设计方案（作业要求 a~e）
```

## 快速开始

```bash
make venv          # 创建虚拟环境
make install       # 安装依赖
make migrate       # 建表
make run           # 启动开发服务器 http://127.0.0.1:8000
```

## API 一览

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/documents/` | 上传课程文档 |
| POST | `/api/documents/<id>/extract/` | 触发大模型抽取（生成知识点 + tag） |
| GET  | `/api/tags/` | 所有标签列表 |
| GET  | `/api/knowledge/?tag=xxx` | 按标签检索知识点 |

## 大模型配置

复制 `.env.example` 为 `.env`，填入任意 OpenAI 兼容 API 即可（未配置时系统使用假数据流程，便于联调）。

## 详细设计

见 [docs/设计方案.md](docs/设计方案.md)。
