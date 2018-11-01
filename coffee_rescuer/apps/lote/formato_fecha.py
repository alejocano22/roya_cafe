from babel.dates import format_datetime


def dar_formato_fecha(fecha):
    """
    Este método permite dar formato a una fecha con "dd 'de' MMMM 'de' yyyy 'a las' HH:mm:ss" en la sintaxis de babel.
    Inicialmente el objetivo es estandarizar el formato de fecha que será enviada a través del correo y que se le
    mostrará al usuario en la parte visual.
    :param fecha: La fecha a formatear en tipo datetime
    :return: Un str con la fecha en el formato  "dd 'de' MMMM 'de' yyyy 'a las' HH:mm:ss" en la sintaxis de babel
    """
    return format_datetime(fecha,format="dd 'de' MMMM 'de' yyyy 'a las' HH:mm:ss",locale='es')
 
