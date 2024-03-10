from django.shortcuts import render
from .models import App2Table
from .serializers import App2TableSerializer, App2TableQuerySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action

# Implement APIs using ModelViewSet
class App2ViewSet(ModelViewSet):
    queryset = App2Table.objects.all()
    serializer = App2TableSerializer
    query_serializer = App2TableQuerySerializer
    
    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get overview of APIs"
    )
    @action(detail=True, methods=['get'])
    def swagger_api_overview(self, request, *args, **krgs):
        api_urls = {
            "Add an item": "/create",
            "Get (an) item(s)": "/get/",
            "Update an item": "/update",
            "Delete an item": "/delete",
        }
        return Response(api_urls)


    @swagger_auto_schema(
        operation_description="Create a new item",
        #request_body=App2TableSerializer,
        #responses={201: App2TableSerializer()}
    )
    @action(detail=True, methods=['post'])
    def swagger_create_doc(self, request, *args, **krgs):
        if request.data.get('name1') is None:
            return Response({"message": "name1 is required"}, status=status.HTTP_400_BAD_REQUEST)
    
        item = self.serializer(data=request.data)
    
        # Check if the requested document already exists in the table
        if self.queryset.filter(name1=request.data['name1']).exists():
            return Response({"message": "Data already exists in the table."}, status=status.HTTP_400_BAD_REQUEST)
    
        # If all attributes of the item is valid, insert it into the table
        if item.is_valid():
            item.save()
            return Response(item.data, status=status.HTTP_201_CREATED)
        else:
            return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Get items by conditions",
        #responses={200: App2TableSerializer()}
    )
    @action(detail=True, methods=['get'])
    def swagger_get_docs(self, request, *args, **krgs):
        # If there are input parameters from the URL, get data by conditions with respect to parameters
        if request.query_params:
            results = self.queryset.filter(**request.query_params.dict()).values()
        # If no input parameters are provided, get all data
        else:
            results = self.queryset.values()
        
        # Check if there are any results or otherwise return an error
        if results:
            return Response(results, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No requested items are found."}, status=status.HTTP_404_NOT_FOUND)
    
    
    @swagger_auto_schema(
        operation_description="Update an item given name1",
        #request_body=App2TableSerializer,
    )
    @action(detail=True, methods=['post'])
    def swagger_update_doc(self, request, *args, **krgs):
        if request.data.get('name1') is None:
            return Response({"message": "name1 is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        item = self.queryset.filter(name1=request.data['name1'])
        
        # Check if value of name1 exists so that we can update the target item
        if item.exists():
            updated_item = App2Table(item.first(), data=request.data, partial=True)
            # If all attributes of the item is valid, update it into the table
            if updated_item.is_valid():
                updated_item.save()
                return Response({"message": "The target item is updated"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(updated_item.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "No target item is found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    @swagger_auto_schema(
        operation_description="Delete an item"
    )
    @action(detail=True, methods=['delete'])
    def swagger_delete_doc(self, request, *args, **krgs):
        if request.data.get('name1') is None:
            return Response({"message": "name1 is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        item = self.queryset.filter(name1=request.data['name1'])
        
        # Check if target item exists so that we can delete it
        if item.exists():
            item.delete()
            return Response({"message": "Successfully deleted"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": "No requested item is found"}, status=status.HTTP_404_NOT_FOUND)