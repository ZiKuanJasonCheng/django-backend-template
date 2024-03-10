from django.db import models

class App2Table(models.Model):
    name1 = models.TextField(primary_key=True)
    name2 = models.IntegerField(blank=True, null=True)
    name3 = models.TextField(blank=True, null=False)
    name4 = models.CharField(max_length=50, blank=False, null=True)
    name5 = models.BooleanField()
 
    class Meta:
        db_table = "app2_table"
        app_label = "app_2"
 
    def __str__(self) -> str:
        return self.name1
    