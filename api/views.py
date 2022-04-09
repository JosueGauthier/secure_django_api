from functools import wraps


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api import serializers
from api.serializers import CustomerSerializer

from business.models import Customer

# Create your views here.


class CustomerView(APIView):
    #!definition de get request
    def get(self, request, format=None):
        customers = Customer.published.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    #!! definition de post request

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#! check if a customer exist or not

def resource_checker(model):
    def check_entiy(fun):
        @wraps(fun)
        def inner_fun(*args, **kwargs):
            try:
                x=fun(*args, **kwargs)
                return x
            except model.DoesNotExist:
                return Response({'messg':'Not found'},status=status.HTTP_204_NO_CONTENT)
            return inner_fun
        return check_entiy



class CustomerDetailView(APIView):



    #@resource_checker(Customer)
    def get(self, request,pk, format=None):

        if(Customer.objects.filter(pk=pk).exists()):
            customer = Customer.published.get(pk=pk)
        
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        else:
             return Response({'messg':'Not found'},status=status.HTTP_204_NO_CONTENT)
            
        


    #@resource_checker(Customer)
    def put(self, request, pk, format=None):
        customer = Customer.published.get(pk=pk)
        serializer = CustomerSerializer(customer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    #@resource_checker(Customer)
    def delete(self, request, pk, format=None):
        customer = Customer.published.get(pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
