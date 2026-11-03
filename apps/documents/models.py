from django.db import models


class Document(models.Model):
    """教师或学生上传的课程文档。"""

    class Status(models.TextChoices):
        PENDING = "pending", "待处理"
        PROCESSING = "processing", "抽取中"
        DONE = "done", "已完成"
        FAILED = "failed", "失败"

    title = models.CharField("标题", max_length=200)
    file = models.FileField("文件", upload_to="documents/%Y/%m/")
    status = models.CharField(
        "状态", max_length=20, choices=Status.choices, default=Status.PENDING
    )
    error_message = models.TextField("失败原因", blank=True, default="")
    uploaded_at = models.DateTimeField("上传时间", auto_now_add=True)

    class Meta:
        verbose_name = "课程文档"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
