import bcrypt, json, requests

from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response 
from rest_framework.exceptions import ValidationError

from apps.boards.models import Board
from apps.boards.pagination import PageNumberPagination

from apps.boards.serialiazers import BoardSerializer



# 게시글 리스트와 게시글 저장 API
class BoardListCreateVIew(generics.ListCreateAPIView):
    queryset = Board.objects.all().order_by("-created_at")
    serializer_class = BoardSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        """
        날씨정보를 기록하는 API
        작성 시간으로 한국기준(서울) 날씨기록
        """
        url = "https://api.weatherapi.com/v1/current.json"
        params = {'key': settings.WEATHER_API_Key, 'q': 'korea', 'aqi' :"yes"}
        res = requests.get(url, params=params)
        if not res.ok:
            raise ValidationError('날씨기록API에 오류가 발생하였습니다 잠시후 다시 시도해주세요')

        data = res.json()
        weather = data['current']['condition']['text']
        serializer.save(weather=weather)
        

# 게시글 상세페이지, 업데이트, 삭제 API
class BoardDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        """
        게시글 삭제의 경우 request요청시 body로 writer정보와 password정보를 전달
        전달된 writer정보와 password 정보를 비교하여 최종 삭제를 진행
        """
        data = json.loads(request.body)
        instance = self.get_object()
        if not instance.writer == data["writer"]:
            raise ValidationError( '아이디가 다릅니다.')
        password = data["password"]
        if not bcrypt.checkpw(password.encode('utf-8'), instance.password.encode('utf-8')):
            raise ValidationError( '비밀번호가 맞지 않습니다.')
        
        self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)