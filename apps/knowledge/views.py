from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import KnowledgePoint, Tag


@require_GET
def tag_list(request):
    """GET /api/tags/  所有标签。"""
    tags = list(Tag.objects.values_list("name", flat=True))
    return JsonResponse({"tags": tags})


@require_GET
def search(request):
    """GET /api/knowledge/?tag=二叉树  按标签检索知识点（支持多标签逗号分隔）。"""
    tag_param = request.GET.get("tag", "").strip()
    qs = KnowledgePoint.objects.select_related("document")
    if tag_param:
        names = [t for t in tag_param.split(",") if t]
        qs = qs.filter(tags__name__in=names).distinct()
    data = [
        {
            "id": kp.id,
            "title": kp.title,
            "content": kp.content,
            "tags": [t.name for t in kp.tags.all()],
            "document": kp.document.title,
        }
        for kp in qs.order_by("-created_at")[:50]
    ]
    return JsonResponse({"count": len(data), "results": data})
