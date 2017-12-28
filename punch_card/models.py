from django.db import models
from employee.models import Employee


class PunchCard(models.Model):
    hit_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    description = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'PunchCard'
        verbose_name_plural = 'PunchCards'
