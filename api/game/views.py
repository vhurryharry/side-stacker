from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Game
from .ai import SideStackerModel, get_ai_move, apply_move, check_winner, get_valid_moves, encode_board
import random

# Initialize AI model
model = SideStackerModel()

# Create a new game
@api_view(["POST"])
def create_game(request):
    game_id = str(random.randint(1000, 9999))  # Unique game ID
    player1_name = request.GET.get('player1_name', 'Player 1')
    game = Game(game_id=game_id, player1_name=player1_name, player2_name="AI", current_turn=1)
    game.initialize_game()
    game.save()
    return JsonResponse({"message": "Game created", "game_id": game_id})

# Join an existing game
@api_view(["POST"])
def join_game(request, game_id):
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    game.player2_name = request.GET.get('player2_name', 'Player 2')
    game.save()
    return JsonResponse({"message": f"Game joined as {game.player2_name}"})

# Get the current game state
@api_view(["GET"])
def get_game_state(request, game_id):
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    return JsonResponse({"board": game.board, "current_turn": game.current_turn})

# Make a move (either by player or AI)
@api_view(["POST"])
def make_move(request, game_id):
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    row = int(request.GET.get('row'))
    direction = request.GET.get('direction')
    if (row, direction) not in get_valid_moves(game.board):
        return JsonResponse({"error": "Invalid move"}, status=400)

    # Apply the player's move
    game.apply_move(row, direction, game.current_turn)
    winner = check_winner(game.board)
    if winner:
        return JsonResponse({"message": f"Player {winner} wins!"})

    # Switch turn
    game.current_turn = -game.current_turn
    game.save()

    # AI Move if it's AI's turn
    if game.current_turn == -1:
        ai_move = get_ai_move(game.board)
        game.apply_move(ai_move[0], ai_move[1], game.current_turn)
        game.save()
        winner = check_winner(game.board)
        if winner:
            return JsonResponse({"message": f"Player {winner} wins!"})

    return JsonResponse({"board": game.board})

@api_view(["GET"])
def get_ai_move(board):
    valid_moves = get_valid_moves(board)
    q_values = model(encode_board(board))
    q_values = q_values.detach().numpy().squeeze()

    # Epsilon-greedy choice (random or best)
    if random.random() < 0.1:
        return random.choice(valid_moves)
    else:
        best_move = max(valid_moves, key=lambda move: q_values[move[0] * 2 + (0 if move[1] == 'L' else 1)])
        return best_move
