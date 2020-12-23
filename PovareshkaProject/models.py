from django.contrib.auth.models import User
from django.db import models


class CourseType(models.Model):
    name = models.CharField(max_length=20)
    type_name = models.CharField(max_length=10)
    details_title = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'тип блюда'
        verbose_name_plural = 'типы блюд'

    def __str__(self):
        return self.name


class Course(models.Model):
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    ingredients = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    receipt = models.TextField(blank=True)

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'

    def __str__(self):
        return self.name
