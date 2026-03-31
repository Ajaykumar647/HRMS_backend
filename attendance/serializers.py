from rest_framework import serializers
from .models import Attendance
from employees.models import Employee


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_emp_id = serializers.CharField(source='employee.employee_id', read_only=True)
    employee_department = serializers.CharField(source='employee.department', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'employee_emp_id',
            'employee_department', 'date', 'status', 'marked_at'
        ]
        read_only_fields = ['id', 'marked_at', 'employee_name', 'employee_emp_id', 'employee_department']
        validators = []

    def validate_employee(self, value):
        if not Employee.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Employee does not exist.")
        return value

    def validate_status(self, value):
        if value not in ['Present', 'Absent']:
            raise serializers.ValidationError("Status must be 'Present' or 'Absent'.")
        return value

    def validate(self, attrs):
        employee = attrs.get('employee', self.instance.employee if self.instance else None)
        date = attrs.get('date', self.instance.date if self.instance else None)

        qs = Attendance.objects.filter(employee=employee, date=date)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                'Attendance for this employee on the selected date has already been marked.'
            )
        return attrs
