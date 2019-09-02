from import_export.instance_loaders import ModelInstanceLoader
import pdb
class LectureInstanceLoader(ModelInstanceLoader):
    def get_instance(self, row):
        try:
            params = {}
            for key in self.resource.get_import_id_fields():
                field = self.resource.fields[key]
                params[field.attribute] = field.clean(row)
            if params:
                return self.get_queryset().get(**params)
            else:
                return None
        except self.resource._meta.model.DoesNotExist:
            return None
        except Exception as e:
            return None
            # pdb.set_trace()
