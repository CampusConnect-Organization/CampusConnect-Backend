from django.db import models

# Create your models here.
class Result(models.Model):
    symbol_number = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    season = models.CharField(max_length=10)
    result = models.JSONField()

    def __str__(self):
        return f"{self.symbol_number}'s {self.year}({self.season}) Result"