from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffee_rescuer.settings')

app = Celery('proj') #Nota 1
app.config_from_object('django.conf:settings', namespace='CELERY') #Nota 2
app.autodiscover_tasks() #Nota 3
app.conf.update(
    BROKER_URL = 'redis://192.168.10.115:3600/0'
)





# app.conf.timezone ='America/Bogota'
# app.conf.beat_schedule = {
#     'every_monday_morning': {
#         'task': 'apps.lote.tasks.every_monday_morning',
#         'schedule': 30.0,
#         'args': (),
#     },
# }
