from django.contrib import admin
from .models import Lawyer, School, Class, Course
# Register your models here.
admin.site.register(Lawyer)

class ClassInline(admin.StackedInline):
    model = Class
    extra = 1
    list_display = ('__str__', 'lawyer') 

class SchoolAdmin(admin.ModelAdmin):
    inlines = [ClassInline]
    

admin.site.register(School, SchoolAdmin)
admin.site.register(Class)
admin.site.register(Course)