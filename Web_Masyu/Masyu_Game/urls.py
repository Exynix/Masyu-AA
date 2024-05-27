from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_file, name="upload_file"),
    path('game/<int:board_id>/', views.game_board_view, name='game_board_view'),
    path('add_line/', views.add_line, name='add_line'),
]