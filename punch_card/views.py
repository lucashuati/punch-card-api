from punch_card.models import PunchCard
from punch_card.serializers import PunchCardSerializer
from rest_framework import generics


class PunchCardList(generics.ListCreateAPIView):
    queryset = PunchCard.objects.all()
    serializer_class = PunchCardSerializer


class PunchCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PunchCard.objects.all()
    serializer_class = PunchCardSerializer
