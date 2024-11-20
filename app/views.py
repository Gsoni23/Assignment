from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from .tasks import generate_html_report, generate_pdf_report
from .models import Report

class HTMLReportView(APIView):
    def post(self, request):
        task = generate_html_report.delay(request.data)
        return Response({"task_id": task.id})

    def get(self, request, task_id):
        task = AsyncResult(task_id)
        if task.status == 'SUCCESS':
            report = Report.objects.get(task_id=task_id)
            return Response({"status": task.status, "html_content": report.content})
        return Response({"status": task.status})

class PDFReportView(APIView):
    def post(self, request):
        task = generate_pdf_report.delay(request.data)
        return Response({"task_id": task.id})

    def get(self, request, task_id):
        task = AsyncResult(task_id)
        if task.status == 'SUCCESS':
            report = Report.objects.get(task_id=task_id)
            response = HttpResponse(report.file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{report.student_id}.pdf"'
            return response
        return Response({"status": task.status})
