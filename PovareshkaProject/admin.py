from django.contrib import admin
from .models import CourseType
from .models import Course


admin.site.register(CourseType)
admin.site.register(Course)
