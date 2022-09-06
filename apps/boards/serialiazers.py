from rest_framework import serializers

from apps.boards.models import Board


class BoardSerializer(serializers.Serializer):
    
    class Meta:
        model = Board
        fields = "__all__"
