from django.urls import path

from apps.boards.views import BoardListCreateView


urlpatterns = [
    path("", BoardListCreateView.as_view())
]
