"""
大模型调用封装：知识点抽取 + 自动打 tag。

设计要点：
- 只依赖 OpenAI 兼容接口：默认调用云 API，把 LLM_API_BASE 指向本地推理服务
  （Ollama / vLLM）即可切换为本地模型，业务代码不变；
- 未配置 API Key 时返回 mock 数据，方便开发联调；
- 生产环境中本模块由异步 Worker（Celery / K8s Job）调用，
  避免 HTTP 请求阻塞在大模型的长响应上。
"""
import json
import os

import requests

PROMPT_TEMPLATE = """你是一名计算机课程助教。请从下面的课程文档中提取知识点，
每个知识点给出：title（不超过20字）、content（50字以内摘要）、tags（3~5个标签）。
以 JSON 数组输出，不要输出其他内容。

课程文档：
{content}
"""


def extract_knowledge_points(text: str) -> list[dict]:
    """输入文档文本，输出结构化知识点列表。"""
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        return _mock(text)

    resp = requests.post(
        f"{os.environ.get('LLM_API_BASE', 'https://api.openai.com/v1')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": os.environ.get("LLM_MODEL", "gpt-4o-mini"),
            "messages": [
                {"role": "system", "content": "你输出严格的 JSON。"},
                {"role": "user", "content": PROMPT_TEMPLATE.format(content=text[:6000])},
            ],
        },
        timeout=120,
    )
    resp.raise_for_status()
    return json.loads(resp.json()["choices"][0]["message"]["content"])


def _mock(text: str) -> list[dict]:
    """无 API Key 时的联调数据。"""
    first_line = text.strip().splitlines()[0][:20] if text.strip() else "示例知识点"
    return [
        {
            "title": first_line or "示例知识点",
            "content": "这是未配置大模型 API 时的占位摘要。",
            "tags": ["示例标签", "计算机基础"],
        }
    ]
