# Bulletin-board-API
원티드 프리온보딩 백엔드 기업 과제

## 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [프로젝트 기술 스택](#프로젝트-기술-스택)
3. [개발 기간](#개발-기간)
4. [팀 구성](#팀-구성)
5. [역할](#역할)
6. [ERD](#ERD)
7. [API 목록](#API-목록)
8. [프로젝트 시작 방법](#프로젝트-시작-방법)


<br>


## 프로젝트 개요
회원가입 로그이 인증 없이 게시판 자체 아이디오 비밀번호르 통해 게시글 작성 가능 게시판 구현



<br>

## 과제 요구사항 분석
### 필수구현사항
### 1. Create : POST /api/board/
- 1개이상의 숫자가 있는 길이가 최소 6자 이상의 비밀번호 및 비밀번호 암호화 진행
  - 비밀번호 정규표현식을 활용하여 re 라이브러리로 유효성 검사 진행
  - brypt 라이브러리를 활용하여 단방향 암호화 진행
- 제목은 20자이하, 본문은 200자 이하로 제한
  - models.py에서 작성할때 CharField를 활용하여 글자수 제한 기능 구현
- 제목과 본문은 이모지를 저장할수 있어야한다.
 - DB생성시 charset을 `utf8mb4`로  및 collate `utf-8mb4_unicode_id`로 설정
 - django의 DB정보처리시 ` "OPTOINS":{"charset":"utf8mb4"} 로 정보 수정 후 `migate` 
 
### 2. List : GET /api/board/
- 모든 사용자는 한 페이지 내에서 모든 게시글을 최신 글 순서로 확인 가능
  - `order_by('-created_at')` 옵션을 활용하여 최신순 정렬 구현
  - password는 serializer에서 `write_only=True` 옵션을 통해 리스트에 조회되지 않도록 구현


### 3. Detail : GET /api/board/<int:pk>
- pk값을 활용하여 상세페이지 조회기능 구현

### 4. Update : PUT/PATCH /api/board/<int:pk>
- 게시글 등록시 등록했던 writer값과, password값을 활용하여 게시글 접근하여 수정기능 구현
- 비밀번호의 경우 request시에 들어온 data를 동일하게 암호화하여 DB에 저장된 암호화된 data와 비교하여 유효성 검사 진행

### 5. Delete : DELETE /api/board/<int:pk>/d
- 처음에 detail+update+delete기능을 동시에 가능한 RetrieveUpdateDestroyAPIView를 활용하여 구현하려고 했으나 
body를 통해 전달된 writer,password값을 유효성 검사를 할수없어 별도의 DestroyAPIView로 따로 API구현
- destroy 메소드를 일부 수정하여 유효성검사 후에 삭제 기능 구현

<br>

## 프로젝트 기술 스택

### Backend
<section>
<img src="https://img.shields.io/badge/Django-092E20?logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?logo=Django&logoColor=white"/>
</section>

### DB
<section>
<img src="https://img.shields.io/badge/MySQL-4479A1?logo=MySQL&logoColor=white"/>
</section>

### Tools
<section>
<img src="https://img.shields.io/badge/GitHub-181717?logo=GitHub&logoColor=white"/>
<img src="https://img.shields.io/badge/Discord-5865F2?logo=Discord&logoColor=white">
<img src="https://img.shields.io/badge/Postman-FF6C37?logo=Postman&logoColor=white">
</section>
<!-- | 백엔드 | DB   |  Tools   |
| ---- | ------ | --- |
|      |        |    | -->


<br>


## 개발 기간
- 2022/09/06~2022/09/07 (총 2일)


<br>


## 팀 구성
| 김현수 | 유혜선 | 임한구 |  최보미  |
| ------ | ------ | ------ | --- |
| [Github](https://github.com/HyeonsooKim) | [Github](https://github.com/Hyes-y)   | [Github](https://github.com/nicholas019/)   |  [Github](https://github.com/BomiChoi)   |


<br>


## ERD
ERD 


<br>


## API 목록
API 명세 주소

<br>


## 프로젝트 시작 방법
1. 로컬에서 실행할 경우
```bash
# 프로젝트 clone(로컬로 내려받기)
git clone -b develop --single-branch ${github 주소}
cd ${디렉터리 명}

# 가상환경 설정
python -m venv ${가상환경명}
source ${가상환경명}/bin/activate
# window (2 ways) 
# 1> ${가상환경명}/Scripts/activate
# 2> activate

# 라이브러리 설치
pip install -r requirements.txt
# 실행
python manage.py runserver
```

<br>
