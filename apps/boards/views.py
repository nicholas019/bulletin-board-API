import bcrypt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.boards.models import Board

from apps.boards.serialiazers import BoardSerializer

# 게시글 리스트와 저장 API
class BoardListCreateView(APIView):
    def get(self, request):
        board = Board.objects.all()
        serializer = BoardSerializer(board, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BoardSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)