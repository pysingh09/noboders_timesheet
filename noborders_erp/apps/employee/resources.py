from import_export import resources
from .models import Attendance


class AttendanceResource(resources.ModelResource):
    class Meta:
        model = Attendance