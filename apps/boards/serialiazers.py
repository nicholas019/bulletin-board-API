import bcrypt, re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.boards.models import Board


class BoardSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    weather  = serializers.CharField(read_only = True)

    class Meta:
        model = Board
        fields = ("pk", "title", "content", "writer", "password", "weather", "created_at")
        
    # 유효성 검사
    def validate(self, validated_data):
        """
        게시글 작성자명+비밀번호 유효성검사(UPDATE용)
        기능 : 아이디 비교, 비밀번호 비교
        비밀번호 비교는 bcrypt 라이브러리로 전달된 request 데이터를 암호화하여 암호화된 데이터를 비교
        """
        if self.instance:
            password = validated_data["password"]
            if not self.instance.writer == validated_data["writer"]:
                raise ValidationError( '아이디가 다릅니다.')
            if not bcrypt.checkpw(password.encode('utf-8'), self.instance.password.encode('utf-8')):
                raise ValidationError( '비밀번호가 맞지 않습니다.')
        else:
            """
            비밀번호 유효성 검사(CREATE 용)
            조건 : 1개이상의 숫자가 있고 길이가 최소 6자 이상 비밀번호 조합
            """                
            password = validated_data['password']
            REGEX_PASSWORD = "^[a-z0-9_-]{6,}$"
            if not re.match(REGEX_PASSWORD, password):
                raise ValidationError( '비밀번호의 양식이 맞지 않습니다')
        return validated_data

    def create(self, validated_data):
        """
        게시글 저장 
        주요기능 : brcypt 라이브러리로 비밀번호 단방향 암호화 하여 저장
        """
        password = validated_data["password"]
        hash_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        
        return Board.objects.create(
                title    = validated_data["title"],
                content  = validated_data["content"],
                writer   = validated_data["writer"],
                password = hash_pw
                )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        
        instance.save()
        return instance