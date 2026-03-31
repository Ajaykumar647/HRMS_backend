from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
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
        validators = [
            UniqueTogetherValidator(
                queryset=Attendance.objects.all(),
                fields=['employee', 'date'],
                message='Attendance for this employee on the selected date has already been marked.',
            )
        ]

    def validate_employee(self, value):
        if not Employee.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Employee does not exist.")
        return value

    def validate_status(self, value):
        if value not in ['Present', 'Absent']:
            raise serializers.ValidationError("Status must be 'Present' or 'Absent'.")
        return value

    def validate(self, attrs):
        employee = attrs.get('employee')
        date = attrs.get('date')
        instance = self.instance

        if instance is None:
            if Attendance.objects.filter(employee=employee, date=date).exists():
                raise serializers.ValidationError({
                    'non_field_errors': f"Attendance for this employee on {date} has already been marked."
                })
        return attrs
