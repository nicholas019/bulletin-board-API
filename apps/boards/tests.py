import bcrypt

from rest_framework import status
from rest_framework.test import APITestCase

from apps.boards.models import Board


class TestBoard(APITestCase):
    '''
        게시판 TEST Code
    '''
    # Test시작전 필요한 임시 데이터 생성
    def setUp(self):
        password = "123123"
        self.hash_pw= bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

        self.board = Board.objects.create(
            id       = 1,
            title    = "게시판 제목 11",
            content  = "게시판 본문 11",
            writer   = "홍길동",
            password = self.hash_pw,
            weather  = "Partly cloudy",
            
        )
        self.board_url = "/api/board/"

    # Test를 위해 생성했던 임시 데이터 삭제
    def tearDown(self):
        Board.objects.all().delete()

    # 게시판 리스트 조회 성공
    def test_list_success(self):
        self.response = self.client.get(self.board_url, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    # 게시판 상세페이지 조회 성공
    def test_detail__success(self):
        self.response = self.client.get(f'{self.board_url}1/', format='json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    # 게시판 글 작성 성공
    def test_create_success(self):
        data = {
            "title"   : "게시판  제목 2",
            "content" : "게시판  내용 2",
            "writer"  : "김길동",
            "password": "123123",
        }

        self.response = self.client.post(self.board_url, data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    # 게시판 글 작성 실패(비밀번호 조건 부합)
    def test_create_fail(self):
        data = {
            "title"   : "게시판 제목 2",
            "content" : "게시판 내용 2",
            "writer"  : "김길동",
            "password": "111",  # 최소 6자, 숫자 1개 포함
        }

        self.response = self.client.post(self.board_url, data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    # 게시판 글 업데이트성공
    def test_update_success(self):
        data = {
            "title"   : "게시판 수정 제목 2",
            "content" : "게시판 수정 내용 2",
            "writer"  : "홍길동",
            "password": "123123",
        }

        self.response = self.client.put(f'{self.board_url}1/', data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    # 게시판 글 업데이트실패(비밀번호 오류)
    def test_update_fail(self):

        data = {
            "title"   : "게시판 수정 제목 2",
            "content" : "게시판 수정 내용 2",
            "writer"  : "홍길동",
            "password": "123111", # 비밀번호 123123
        }

        self.response = self.client.put(f'{self.board_url}1/', data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.response.json(), {'non_field_errors': ['비밀번호가 맞지 않습니다.']})

    # 게시판 작성글 삭제 성공
    def test_delete_success(self):
        data = {
            "writer"  : "홍길동",
            "password": "123123"
        }

        self.response = self.client.delete(f'{self.board_url}1/', data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    # 게시판 작성글 삭제 실패 (비밀번호 오류)
    def test_delete_fail(self):
        data = {
            "writer"  : "홍길동",
            "password": "123111" # 비밀번호 123123
        }

        self.response = self.client.delete(f'{self.board_url}1/', data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.response.json(),  ['비밀번호가 맞지 않습니다.'])
