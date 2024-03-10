from django.db import models
import uuid

class App1Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    col1 = models.TextField()
    col2 = models.IntegerField(blank=True, null=True)
    col3 = models.TextField(blank=True, null=False)
    col4 = models.BooleanField()
    col5 = models.CharField(max_length=100, blank=False, null=True)
    col6 = models.DateTimeField(blank=True, null=True)
    col7 = models.FloatField(blank=True, null=True)
 
    class Meta:
        db_table = "app1_table"
        app_label = "app_1"
 
    def __str__(self) -> str:
        return self.col1