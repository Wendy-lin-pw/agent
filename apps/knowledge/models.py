from django.db import models

from apps.documents.models import Document


class Tag(models.Model):
    """知识点标签，如「二叉树」「时间复杂度」。"""

    name = models.CharField("标签名", max_length=50, unique=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        ordering = ["name"]

    def __str__(self):
        return self.name


class KnowledgePoint(models.Model):
    """由大模型从文档中抽取的知识点。"""

    document = models.ForeignKey(
        Document, verbose_name="来源文档", on_delete=models.CASCADE, related_name="points"
    )
    title = models.CharField("知识点标题", max_length=100)
    content = models.TextField("内容摘要", blank=True, default="")
    tags = models.ManyToManyField(Tag, verbose_name="标签", blank=True, related_name="points")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "知识点"
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return self.title
