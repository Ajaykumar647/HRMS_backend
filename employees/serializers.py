from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_employee_id(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Employee ID cannot be blank.")
        return value

    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Full name cannot be blank.")
        return value

    def validate_department(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Department cannot be blank.")
        return value

    def validate_email(self, value):
        value = value.strip().lower()
        if not value:
            raise serializers.ValidationError("Email cannot be blank.")
        return value

    def validate(self, attrs):
        # Check for duplicate on create
        instance = self.instance
        if instance is None:
            if Employee.objects.filter(employee_id=attrs.get('employee_id')).exists():
                raise serializers.ValidationError({'employee_id': 'An employee with this Employee ID already exists.'})
            if Employee.objects.filter(email=attrs.get('email')).exists():
                raise serializers.ValidationError({'email': 'An employee with this email already exists.'})
        return attrs
