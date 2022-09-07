from django.urls import path

from apps.boards.views import BoardDetailUpdateDeleteView, BoardListCreateVIew


urlpatterns = [
    path("", BoardListCreateVIew.as_view()),
    path("<int:pk>/", BoardDetailUpdateDeleteView.as_view()),
]
