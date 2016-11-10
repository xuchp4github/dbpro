from django.contrib import admin

# Register your models here.

from .models import Photo
 
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image',)
    
admin.site.register(Photo, PhotoAdmin)