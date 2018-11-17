# celery_example/tasks.py
from coffee_rescuer.celery import app
from django.core.mail import send_mail
from celery.schedules import crontab
from apps.usuario.models import actualizar_info_usuario
from django.contrib.auth.models import User
from apps.lote import models


@app.task
def enviar_mail(asunto, contenido, destinatario):
    """
    Este método que se envía a la pila de tareas de celery, se encarga de enviar un correo desde coffeerescuer@gmail.com
    :param asunto: El asunto del correo
    :param contenido: El mensaje del correo
    :param destinatario: La dirección del correo a dónde se enviará el mensaje.
    """
    send_mail(asunto, contenido, 'coffeerescuer@gmail.com', [destinatario], fail_silently=False)


@app.task
def actualizar_detalles_lote():
    """
    Este método que se envía a la pila de tareas de celery, actualiza los detalles de lote de todos los usuarios.
    Actualiza los detalles de lote de todos los usuarios de los usuarios registrados en el sistema
    """
    usuarios = User.objects.all()
    for usuario in usuarios:
        actualizar_info_usuario(usuario.username)


@app.task
def registrar_detalle_lote(id_lote, path_info_sensores):
    """
    Este método que se envía a la pila de tareas de celery, busca agregar, un nuevo detalle de lote.

    :param id_lote: El id del lote al que le añadirá un nuevo detalle de lote
    :param path_info_sensores: La dirección del .json con la información de los sensores
    """
    lote = models.Lote.objects.get(id=id_lote)
    if len(models.DetalleLote.objects.filter(info_sensores=path_info_sensores)) == 0:
        models.DetalleLote.objects.create(lote=lote, info_sensores=path_info_sensores)

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Este método permite ejecutar tareas periódicas usando celery.
    """
    # Calls actualizar_detalles_lote('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, actualizar_detalles_lote.s(), name='add every 10')

    # Executes every day at 1 a.m.
    sender.add_periodic_task(
        crontab(hour=1, minute=0),
        actualizar_detalles_lote.s(),
        name='Actualizar info at 1 am'
    )

    # Executes every day at 4 a.m.
    sender.add_periodic_task(
        crontab(hour=4, minute=0),
        actualizar_detalles_lote.s(),
        name='Actualizar info at 4 am'
    )

    # Executes every day at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        actualizar_detalles_lote.s(),
        name='Actualizar info at 7 30 am'
    )

    # Executes every day at 10 a.m.
    sender.add_periodic_task(
        crontab(hour=10, minute=0),
        actualizar_detalles_lote.s(),
        name='Actualizar info at 10 am'
    )

    # Executes every day at 1 p.m.
    sender.add_periodic_task(
        crontab(hour=13, minute=0),
        actualizar_detalles_lote.s(),
        name='Actualizar info at 1 pm'
    )

    # Executes every day at 4 p.m.
    sender.add_periodic_task(
        crontab(hour=16, minute=0),
        actualizar_detalles_lote.s(),
        name='Actualizar info at 4 pm'
    )

    # Executes every day at 5:30 p.m.
    sender.add_periodic_task(
        crontab(hour=17, minute=30),
        actualizar_detalles_lote.s(),
        name='Actualizar info at 5 30 pm'
    )

    # Executes every day at 10 p.m.
    sender.add_periodic_task(
        crontab(hour=22, minute=0),
        actualizar_detalles_lote.s(),
        name='Actualizar info at 10 pm'
    )
