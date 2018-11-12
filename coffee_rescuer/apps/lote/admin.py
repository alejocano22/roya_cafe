from django.contrib import admin
from apps.lote.models import Lote,DetalleLote,Coordenada

# Register your models here.
admin.site.register(DetalleLote)
admin.site.register(Coordenada)


@admin.register(Lote)
class FincaAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('id',)
        return self.readonly_fields
