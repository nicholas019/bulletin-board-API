import bcrypt,json

from rest_framework import generics, status
from rest_framework.response import Response 
from rest_framework.exceptions import ValidationError

from apps.boards.models import Board

from apps.boards.serialiazers import BoardSerializer


# 게시글 리스트와 저장 API
class BoardListCreateVIew(generics.ListCreateAPIView):
    queryset = Board.objects.all().order_by("-created_at")
    serializer_class = BoardSerializer

# 게시글 상세페이지, 업데이트API
class BoardDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = "pk"

# 게시글 삭제
class BoardDeleteView(generics.DestroyAPIView):
    """
    게시글 삭제의 경우 request요청시 body로 writer정보와 password정보를 전달
    전달된 writer정보와 password 정보를 비교하여 최종 삭제를 진행
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
    def destroy(self, request, *args, **kwargs):
        data = json.loads(request.body)
        instance = self.get_object()
        if not instance.writer == data["writer"]:
            raise ValidationError( '아이디가 다릅니다.')
        password = data["password"]
        if not bcrypt.checkpw(password.encode('utf-8'), instance.password.encode('utf-8')):
            raise ValidationError( '비밀번호가 맞지 않습니다.')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
