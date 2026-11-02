import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Document
from .services import extract_knowledge_points


@require_POST
def upload_document(request):
    """POST /api/documents/  上传课程文档。"""
    file = request.FILES.get("file")
    if file is None:
        return JsonResponse({"error": "缺少 file 字段"}, status=400)
    doc = Document.objects.create(title=file.name, file=file)
    return JsonResponse({"id": doc.id, "title": doc.title, "status": doc.status}, status=201)


@require_POST
def extract(request, doc_id: int):
    """POST /api/documents/<id>/extract/  触发大模型抽取。

    框架阶段为同步实现；生产部署时改为投递到消息队列，
    由 K8s Worker Pod 异步执行（见 docs/设计方案.md 部署章节）。
    """
    doc = get_object_or_404(Document, pk=doc_id)
    doc.status = Document.Status.PROCESSING
    doc.save(update_fields=["status"])
    try:
        text = doc.file.read().decode("utf-8", errors="ignore")
        points = extract_knowledge_points(text)
    except Exception as exc:  # noqa: BLE001 —— 框架阶段统一兜底
        doc.status = Document.Status.FAILED
        doc.error_message = str(exc)
        doc.save(update_fields=["status", "error_message"])
        return JsonResponse({"error": str(exc)}, status=500)

    # 延迟导入避免循环依赖
    from apps.knowledge.models import KnowledgePoint, Tag

    for item in points:
        kp = KnowledgePoint.objects.create(
            document=doc, title=item.get("title", ""), content=item.get("content", "")
        )
        for name in item.get("tags", []):
            kp.tags.add(Tag.objects.get_or_create(name=name)[0])

    doc.status = Document.Status.DONE
    doc.save(update_fields=["status"])
    return JsonResponse({"id": doc.id, "status": doc.status, "points": len(points)})


@require_POST
def batch_extract(request):
    """POST /api/documents/batch_extract/  批量触发（body: {"ids": [1,2]}）。"""
    ids = json.loads(request.body or b"{}").get("ids", [])
    return JsonResponse({"queued": list(ids)})
