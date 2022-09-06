import bcrypt, re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.boards.models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("pk", "title", "content", "writer", "password","created_at")
        
    def validate(self, attrs):
        """
        비밀번호 유효성 검사
        조건 : 1개이상의 숫자와 1개 이상의 문자가 들어가는 최소 6자 이상 비밀번호 조합
        """
        password = attrs['password']
        REGEX_PASSWORD = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$"
        if not re.match(REGEX_PASSWORD, password):
            raise ValidationError( '비밀번호의 양식이 맞지 않습니다')
        return attrs

    def create(self, validated_date):
        """
        게시글 저장 
        주요기능 : brcypt 라이브러리로 비밀번호 단방향 암호화 하여 저장
        """
        password = validated_date["password"]
        hash_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        
        return Board.objects.create(
                title    = validated_date["title"],
                content  = validated_date["content"],
                writer   = validated_date["writer"],
                password = hash_pw
                )