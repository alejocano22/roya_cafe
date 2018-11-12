from django.contrib import admin
from apps.finca.models import Finca
# Register your models here.


@admin.register(Finca)
class FincaAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('id',)
        return self.readonly_fields
