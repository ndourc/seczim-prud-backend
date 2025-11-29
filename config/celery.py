import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('prudential')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Configure Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'calculate-risk-scores': {
        'task': 'apps.core.tasks.calculate_risk_scores',
        'schedule': 3600.0,  # Every hour
    },
    'send-notifications': {
        'task': 'apps.core.tasks.send_pending_notifications',
        'schedule': 300.0,  # Every 5 minutes
    },
    'update-compliance-indices': {
        'task': 'apps.core.tasks.update_compliance_indices',
        'schedule': 86400.0,  # Daily
    },
    'check-licensing-breaches': {
        'task': 'apps.core.tasks.check_licensing_breaches',
        'schedule': 3600.0,  # Every hour
    },
}

