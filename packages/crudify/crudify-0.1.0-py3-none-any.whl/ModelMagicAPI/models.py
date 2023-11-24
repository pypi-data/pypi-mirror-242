from django.db import models

# Create your models here.
class TestModel(models.Model):
    name = models.CharField(max_length=500)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.name
