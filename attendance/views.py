from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = Attendance.objects.select_related('employee').all()

        # Filter by employee id (pk)
        employee_id = self.request.query_params.get('employee')
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        # Filter by date
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)

        # Filter by status
        attendance_status = self.request.query_params.get('status')
        if attendance_status:
            queryset = queryset.filter(status=attendance_status)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': self._flatten_errors(serializer.errors)},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'error': self._flatten_errors(serializer.errors)},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {'message': 'Attendance record deleted successfully.'},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {'error': 'Attendance record not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def _flatten_errors(self, errors):
        messages = []
        for field, msgs in errors.items():
            if isinstance(msgs, list):
                for msg in msgs:
                    messages.append(str(msg))
            elif isinstance(msgs, dict):
                for sub_field, sub_msgs in msgs.items():
                    for msg in sub_msgs:
                        messages.append(str(msg))
            else:
                messages.append(str(msgs))
        return ' | '.join(messages)
