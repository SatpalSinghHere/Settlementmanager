from django.contrib import admin
from .models import *

# Register your models here.
class BuildingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Building._meta.get_fields() 
    if field.name != "id" 
    if field.name != "building_description"
    if field.name != "shopitem" 
    ]

admin.site.register(Building, BuildingAdmin)
admin.site.register(Character)
admin.site.register(Settlement)
admin.site.register(Event)
admin.site.register(Funds)
admin.site.register(Population_change)



