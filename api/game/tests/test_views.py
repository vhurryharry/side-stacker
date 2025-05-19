# Placeholder for view tests
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from game.models import Game
from game.enums import GameMode, GameStatus

class GameViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_game(self):
        response = self.client.post(reverse('create_game'), {'playerName': 'Alice', 'mode': GameMode.PVP})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['player1'], 'Alice')

    def test_list_available_games(self):
        Game.objects.create(player1='Alice', mode=GameMode.PVP, status=GameStatus.WAITING)
        response = self.client.get(reverse('list_available_games'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('games', data)

    def test_join_game(self):
        game = Game.objects.create(player1='Alice', mode=GameMode.PVP, status=GameStatus.WAITING)
        response = self.client.post(reverse('join_game', args=[game.id]), {'playerName': 'Bob'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['player2'], 'Bob')

    def test_get_game_state(self):
        game = Game.objects.create(player1='Alice', mode=GameMode.PVP, status=GameStatus.WAITING)
        response = self.client.get(reverse('get_game_state', args=[game.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['player1'], 'Alice')
