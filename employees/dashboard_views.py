from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Q
from employees.models import Employee
from attendance.models import Attendance


class DashboardView(APIView):
    def get(self, request):
        today = timezone.now().date()

        total_employees = Employee.objects.count()
        present_today = Attendance.objects.filter(date=today, status='Present').count()
        absent_today = Attendance.objects.filter(date=today, status='Absent').count()

        # Total present days per employee
        employee_stats = Employee.objects.annotate(
            total_present=Count('attendance', filter=Q(attendance__status='Present')),
            total_absent=Count('attendance', filter=Q(attendance__status='Absent')),
        ).values('id', 'employee_id', 'full_name', 'department', 'total_present', 'total_absent')

        return Response({
            'summary': {
                'total_employees': total_employees,
                'present_today': present_today,
                'absent_today': absent_today,
                'not_marked_today': total_employees - present_today - absent_today,
            },
            'employee_stats': list(employee_stats),
        })
