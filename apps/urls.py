from django.urls import path, include

urlpatterns = [
    path("board/", include('apps.boards.urls'))
]
