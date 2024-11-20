from django.db import models

class Report(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    student_id = models.CharField(max_length=255)
    report_type = models.CharField(max_length=10)  # 'HTML' or 'PDF'
    content = models.TextField(null=True, blank=True)  # For HTML
    file = models.BinaryField(null=True, blank=True)  # For PDFs
    created_at = models.DateTimeField(auto_now_add=True)
