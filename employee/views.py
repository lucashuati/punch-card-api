from employee.models import Employee
from employee.serializers import EmployeeSerializer, AcumulateTimeSerializer
from punch_card.models import PunchCard
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from datetime import date
from .utils import get_acumulate


class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetail(APIView):
    """
    Retrieve, update or delete a employee instance.
    """

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Employee = self.get_object(pk)
        Employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetAcumulate(APIView):
    def get_data_params(self, params):
        ALLOWED_PARAMS = ['start_date', 'end_date']
        data_params = {
            'errors': [],
            'data': {
                'start_date': date.min,
                'end_date': date.max
            }
        }
        for key, value in params.items():
            if key in ALLOWED_PARAMS:
                try:
                    year, month, day = value.split('-')
                    data_params['data'][key] = date(int(year), int(month), int(day))
                except Exception as e:
                    print(type(e))
                    data_params['errors'].append('{} is not a valid format. Use YYYY-MM-DD format'.format(key))
            else:
                data_params['errors'].append('{} is not a valid parameter.'.format(key))

        return data_params

    def get(self, request, pk, format=None):
        params = self.get_data_params(request.GET)

        if params['errors']:
            return Response(params['errors'], status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.get(pk=pk)

        punch_cards = PunchCard.objects.filter(
            employee=employee
        ).filter(
            hit_time__gte=params['data']['start_date'],
            hit_time__lte=params['data']['end_date'],
        ).order_by(
            'hit_time'
        )

        acumulate = {
            'start_date': params['data']['start_date'] if params['data']['start_date'] != date.min else None,
            'end_date': params['data']['end_date'] if params['data']['end_date'] != date.max else None,
            'acumulate': get_acumulate(punch_cards)
        }
        return Response(acumulate)
