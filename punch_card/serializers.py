from rest_framework import serializers
from punch_card.models import PunchCard


class PunchCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PunchCard
        fields = '__all__'
