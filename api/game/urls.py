from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_game, name='create_game'),
    path('join/<str:game_id>/', views.join_game, name='join_game'),
    path('game_state/<str:game_id>/', views.get_game_state, name='get_game_state'),
    path('make_move/<str:game_id>/', views.make_move, name='make_move'),
]
