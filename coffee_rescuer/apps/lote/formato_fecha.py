from babel.dates import format_datetime
def dar_formato_fecha(fecha):
    return format_datetime(fecha,format="dd 'de' MMMM 'de' yyyy 'a las' HH:mm:ss",locale='es')
 
