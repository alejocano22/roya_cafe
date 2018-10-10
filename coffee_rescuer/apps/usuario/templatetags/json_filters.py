from django.core.serializers import serialize
from django.db.models.query import QuerySet
import json
from django.template import Library

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object)


def info_finca(object):
    return serialize('json', object,fields=["id", "nombre","promedio_estado_lotes"])


register.filter('jsonify', jsonify)
register.filter('info_finca', info_finca)