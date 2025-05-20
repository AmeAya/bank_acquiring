from rest_framework.serializers import ModelSerializer
from .models import *


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
