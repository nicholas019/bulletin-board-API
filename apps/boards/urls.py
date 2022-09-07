from django.urls import path

from apps.boards.views import BoardDetailUpdateView, BoardListCreateVIew, BoardDeleteView


urlpatterns = [
    path("", BoardListCreateVIew.as_view()),
    path("<int:pk>/", BoardDetailUpdateView.as_view()),
    path("<int:pk>/d/", BoardDeleteView.as_view()),
]
