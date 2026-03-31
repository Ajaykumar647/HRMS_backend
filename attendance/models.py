from django.db import models
from employees.models import Employee


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date', 'employee__full_name']
        db_table = 'attendance'

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.status}"
