from import_export.instance_loaders import ModelInstanceLoader
from .models import Class
class LectureInstanceLoader(ModelInstanceLoader):
    def get_instance(self, row):
        try:
            params = {}
            field = self.resource.fields['school']
            school_name = field.clean(row)
            field = self.resource.fields['grade_class_id']
            grade_class_string = field.clean(row)
            class_obj = Class.objects.get_class(school_name, grade_class_string)
            if class_obj is None:
                return NameError(school_name + ' ' + grade_class_string + ' not exists in database')
            params['classroom'] = class_obj
            field = self.resource.fields['course']
            params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except self.resource._meta.model.DoesNotExist:
            return None
