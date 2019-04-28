from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Lawyer, School, Class, Course
# Register your models here.
admin.site.register(Lawyer)

class ClassResource(resources.ModelResource):
    class Meta:
        model = Class
class ClassInline(admin.StackedInline):
    model = Class
    extra = 1
    list_display = ('__str__', 'lawyer') 

class SchoolAdmin(admin.ModelAdmin):
    inlines = [ClassInline]
    
class ClassAdmin(ImportExportModelAdmin):
    resource_class = ClassResource
    
admin.site.register(School, SchoolAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Course)