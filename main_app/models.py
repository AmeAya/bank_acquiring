from django.db import models


class Payment(models.Model):
    order_id = models.IntegerField()
    total = models.IntegerField()
    datetime = models.DateTimeField()
    hash = models.CharField(max_length=64)
    is_payed = models.BooleanField(default=False)
