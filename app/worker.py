from celery import shared_task
from .models import Report
from reportlab.pdfgen import canvas
from io import BytesIO
import json

@shared_task
def generate_html_report(data):
    student_id = data['student_id']
    events = sorted(data['events'], key=lambda x: x['unit'])
    aliases = {event['unit']: f"Q{i+1}" for i, event in enumerate(sorted(set(e['unit'] for e in events)))}
    order = " -> ".join(aliases[event['unit']] for event in events)

    html_content = f"<h2>Student ID: {student_id}</h2><p>Event Order: {order}</p>"
    report = Report.objects.create(task_id=generate_html_report.request.id, student_id=student_id, report_type='HTML', content=html_content)
    return report.id

@shared_task
def generate_pdf_report(data):
    student_id = data['student_id']
    events = sorted(data['events'], key=lambda x: x['unit'])
    aliases = {event['unit']: f"Q{i+1}" for i, event in enumerate(sorted(set(e['unit'] for e in events)))}
    order = " -> ".join(aliases[event['unit']] for event in events)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, f"Student ID: {student_id}")
    p.drawString(100, 730, f"Event Order: {order}")
    p.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    report = Report.objects.create(task_id=generate_pdf_report.request.id, student_id=student_id, report_type='PDF', file=pdf_data)
    return report.id






# 
# 
# 

from celery import Celery, Task, shared_task
from celery.schedules import crontab
from . import models
from .mail import sendMail
import csv
from datetime import date
from sqlalchemy.sql import func
from .database import db


# making celery app in flask application context
def create_celery_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
               return self.run(*args, **kwargs)

    celery_app = Celery(app.name,broker="redis://127.0.0.1:6379/1", backend="redis://127.0.0.1:6379/2",task_cls=FlaskTask,broker_connection_retry_on_startup=True, timezone = 'Asia/Kolkata')
    
    celery_app.conf.beat_schedule = {
        'send-monthly-entertainment-report': {
            'task': 'Scheduled Job',
            # 'schedule': crontab(day_of_month=1, hour=18, minute=0),
            'schedule': 120,
        },

        'daily-reminder': {
            'task': 'Daily Reminder',
            # 'schedule': crontab(hour=18, minute=0),
            'schedule': 120,
        },
    }

    celery_app.set_default()
    return celery_app

# Export job to send the venue data to the admin
@shared_task(name="Export Job")
def export_data(venue_id):

    res = export_venue_data(venue_id=venue_id)
            
    if(res): return [True,'Successfully Exported']
    else : return [False,'Failed to export']



def export_venue_data(venue_id):
    try:
        # Get the Venues to export
        venue = models.Venue.query.get(int(venue_id))

        # Get the admin from database
        admin = models.User.query.get(int(venue.owner))

        file_path = "venue_export.csv"

        # Write the content in the file
        with open(file_path, 'w', newline='') as csv_file:
            fieldnames = ['venue_id', 'venue_name', 'place', 'capacity', 'no. of shows', 'shows'] 
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerow({
                'venue_id': venue.venue_id, 
                'venue_name': venue.venue_name,
                'place': venue.place,
                'capacity': venue.capacity,
                'no. of shows': len(venue.shows),
                'shows': venue.shows
            })

        # Send the email to admin with the csv file in atatchment
        res = sendMail(admin.email,"Venue Exports","The venue info has been exported and attached below in CSV file format.",file_path,"text/csv")
        return res
    except Exception as e:
        print(e)
        return False


