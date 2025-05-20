from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import *

from hashlib import sha256
from random import randint


class PaymentApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        payment_id = request.GET.get('id')
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response(data=f"Payment id '{payment_id}' is not exists!", status=status.HTTP_400_BAD_REQUEST)
        chance = randint(0, 1)
        if chance == 1:
            payment.is_payed = True
            payment.save()
            return Response(data={'is_payed': True}, status=status.HTTP_200_OK)
        else:
            return Response(data={'is_payed': False}, status=status.HTTP_200_OK)

    def post(self, request):
        required_fields = ('order_id', 'total', 'datetime', 'hash')
        for field in required_fields:
            if field not in request.data:
                return Response(data=f"Field '{field}' is required!", status=status.HTTP_400_BAD_REQUEST)
        data_str = f"{request.data.get('order_id')}_{request.data.get('total')}"
        data_str += f"{request.data.get('datetime').replace(' ', '_')}_qwerty"
        hashed_data = sha256(data_str.encode('utf-8')).hexdigest()
        if hashed_data != request.data.get('hash'):
            return Response(data={"hash": hashed_data, "data": data_str}
                            , status=status.HTTP_400_BAD_REQUEST)
        data = PaymentSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data=f"Payment in progress!", status=status.HTTP_200_OK)
        return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)
