from rest_framework import serializers
from .models import App2Table
 
class App2TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = App2Table
        # Return all columns of the table
        fields = "__all__"
       
class App2TableQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = App2Table
        # Return only some columns of the table
        fields = ["name1", "name3", "name5"]