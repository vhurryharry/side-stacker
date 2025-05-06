from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_game, name="create_game"),
    path("<str:game_id>/join/", views.join_game, name="join_game"),
    path("<str:game_id>/state/", views.get_game_state, name="get_game_state"),
    path("<str:game_id>/move/", views.make_move, name="make_move"),
    path("list/", views.list_available_games, name="list_available_games"),
]
