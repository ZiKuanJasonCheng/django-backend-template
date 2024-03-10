from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import App1Table
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import App1TableSerializer, App1TableQuerySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action


@swagger_auto_schema(
    methods=["get"],
    operation_id="api_overview",
    operation_description="Get overview of our APIs",
    tags=["app_1"],
)
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        "Add an item": "/create",
        "Get (an) item(s)": "/get/",
        "Update an item": "/update",
        "Delete an item": "/delete",
    }
    return Response(api_urls)


@swagger_auto_schema(
    methods=["post"],
    operation_id="create_item",
    operation_description="Create a new item",
    tags=["app_1"],
    request_body=App1TableSerializer,
    #responses={201: App1TableSerializer()}
)
@api_view(['POST'])
def create(request):
    if request.data.get('col1') is None:
        return Response({"message": "col1 is required"}, status=status.HTTP_400_BAD_REQUEST)
   
    item = App1TableSerializer(data=request.data)
   
    # Check if the requested document already exists in the table
    if App1Table.objects.filter(col1=request.data['col1']).exists():
        return Response({"message": "Data already exists in the table."}, status=status.HTTP_400_BAD_REQUEST)
   
    # If all attributes of the item is valid, insert it into the table
    if item.is_valid():
        item.save()
        return Response(item.data, status=status.HTTP_201_CREATED)
    else:
        return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=["get"],
    operation_id="get_item",
    operation_description="Get items by filters",
    tags=["app_1"],
    query_serializer=App1TableQuerySerializer,
    #responses={200: App1TableQuerySerializer()}
)
@api_view(['GET'])
def get(request):
    # If there are input parameters from the URL, get data by conditions with respect to parameters
    if request.query_params:
        results = App1Table.objects.filter(**request.query_params.dict()).values()
    # If no input parameters are provided, get all data
    else:
        results = App1Table.objects.all().values()
    
    # Check if there are any results or otherwise return an error
    if results:
        return Response(results, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No requested items are found."}, status=status.HTTP_404_NOT_FOUND)
 
 
@swagger_auto_schema(
    methods=["post"],
    operation_id="update_item",
    operation_description="Update an item given col1",
    tags=["app_1"],
    request_body=App1TableSerializer,
)
@api_view(['POST'])
def update(request):
    if request.data.get('col1') is None:
        return Response({"message": "col1 is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    item = App1Table.objects.filter(col1=request.data['col1'])
    
    # Check if value of col1 exists so that we can update the target item
    if item.exists():
        updated_item = App1Table(item.first(), data=request.data, partial=True)
        # If all attributes of the item is valid, update it into the table
        if updated_item.is_valid():
            updated_item.save()
            return Response({"message": "The target item is updated"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(updated_item.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "No target item is found"}, status=status.HTTP_404_NOT_FOUND)
 

@swagger_auto_schema(
    methods=["delete"],
    operation_id="delete_item",
    operation_description="Delete an item",
    tags=["app_1"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['col1'],
        properties={
            'col1': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)
@api_view(['DELETE'])
def delete(request):
    if request.data.get('col1') is None:
        return Response({"message": "col1 is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    item = App1Table.objects.filter(col1=request.data['col1'])
    
    # Check if target item exists so that we can delete it
    if item.exists():
        item.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"message": "No requested item is found"}, status=status.HTTP_404_NOT_FOUND)
