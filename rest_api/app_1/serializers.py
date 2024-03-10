from rest_framework import serializers
from .models import App1Table
 
class App1TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = App1Table
        # Return all columns of the table
        fields = "__all__"
       
class App1TableQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = App1Table
        # Return only some columns of the table
        fields = ["col1", "col3", "col6", "col7"]