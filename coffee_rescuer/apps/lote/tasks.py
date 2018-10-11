#celery_example/tasks.py
from coffee_rescuer.celery import app
from django.core.mail import send_mail
from celery.schedules import crontab 

def enviar_mail(asunto, contenido, destinatario):
    send_mail(asunto, contenido, 'coffeerescuer@gmail.com', [destinatario], fail_silently=False)



@app.task 
def actualizar_detalles_lote():
	print("radamel")

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls actualizar_detalles_lote('hello') every 10 seconds.
    sender.add_periodic_task(10.0, actualizar_detalles_lote.s(), name='add every 10')

    # Executes every day at 1 a.m.
    sender.add_periodic_task(
        crontab(hour=1, minute=0),
        actualizar_detalles_lote.s(),
    )
    
    # Executes every day at 4 a.m.
    sender.add_periodic_task(
        crontab(hour=4, minute=0),
        actualizar_detalles_lote.s(),
    )
    
    # Executes every day at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        actualizar_detalles_lote.s(),
    )
    
    # Executes every day at 10 a.m.
    sender.add_periodic_task(
        crontab(hour=10, minute=0),
        actualizar_detalles_lote.s(),
    )
    
    # Executes every day at 1 p.m.
    sender.add_periodic_task(
        crontab(hour=1, minute=0),
        actualizar_detalles_lote.s(),
    )
    
    # Executes every day at 4 p.m.
    sender.add_periodic_task(
        crontab(hour=16, minute=0),
        actualizar_detalles_lote.s(),
    )
    
    # Executes every day at 6 p.m.
    sender.add_periodic_task(
        crontab(hour=18, minute=0),
        actualizar_detalles_lote.s(),
    )
    
    # Executes every day at 10 p.m.
    sender.add_periodic_task(
        crontab(hour=22, minute=0),
        actualizar_detalles_lote.s(),
    )
