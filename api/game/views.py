from django.http import JsonResponse 
from rest_framework.decorators import api_view
from .models import Game
from .game_utils import get_valid_moves, check_winner
from .ai_move import get_ai_move
from .enums import GameMode, GameStatus, BotDifficulty
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create a new game
@api_view(["POST"])
def create_game(request):
    player1 = request.data.get('playerName', 'Player 1')
    mode = request.data.get('mode', GameMode.PVP)
    difficulty = request.data.get('difficulty', BotDifficulty.MEDIUM)

    if mode not in GameMode.__members__.values():
        return JsonResponse({"error": "Invalid game mode"}, status=400)

    game = Game(
        player1=player1,
        player2="AI" if mode != GameMode.PVP else "",
        mode=mode,
        bot_difficulty=difficulty,
        current_turn=1,
        status=GameStatus.WAITING if mode == GameMode.PVP else GameStatus.IN_PROGRESS,
    )
    game.save()

    return JsonResponse(game.serialize(), status=201)


# Join an existing game
@api_view(["POST"])
def join_game(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    if game.mode != GameMode.PVP or game.player2:
        return JsonResponse({"error": "Cannot join this game"}, status=400)

    game.player2 = request.data.get('playerName', 'Player 2')
    game.status = GameStatus.IN_PROGRESS
    game.save()

    
    if game.mode == GameMode.PVP:
        # Notify both players about the move
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"game_{game_id}",
            {
                "type": "game_update",
                "message": {
                    "type": "player_join",
                    "player2": game.player2
                },
            },
        )

    return JsonResponse(game.serialize(), status=200)

# List available games
@api_view(["GET"])
def list_available_games(request):
    # Get all games that are in the WAITING state and have only one player (player2 is not set)
    available_games = Game.objects.filter(status=GameStatus.WAITING, mode=GameMode.PVP)
    
    # Prepare a list of game IDs and their creator's name
    game_list = [
        {"id": game.id, "creator": game.player1}
        for game in available_games
    ]
    
    return JsonResponse({"games": game_list})

# Get game state
@api_view(["GET"])
def get_game_state(request, game_id):
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    return JsonResponse(game.serialize(), status=200)


# Make a move
@api_view(["POST"])
def make_move(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    row = int(request.data.get('row'))
    direction = request.data.get('direction')
    board = game.get_board()

    # Validate move
    if (row, direction) not in get_valid_moves(board):
        return JsonResponse({"error": "Invalid move"}, status=400)

    # Apply the player's move (player 1 or player 2)
    game.apply_move(row, direction, game.current_turn)
    board = game.get_board()

    winner = check_winner(board)
    is_draw = len(get_valid_moves(board)) == 0
    if winner or is_draw:
        game.status = GameStatus.FINISHED
    else:
        # Switch turn
        game.current_turn = -game.current_turn
    game.save()

    if game.mode == GameMode.PVP:
        # Notify both players about the move
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"game_{game_id}",
            {
                "type": "game_update",
                "message": {
                    "type": "move",
                    "row": row,
                    "direction": direction,
                    "board": board,
                    "currentTurn": game.current_turn,
                    "winner": winner if winner else None,
                    "isDraw": is_draw,
                },
            },
        )

    ai_move = None
    if game.status != GameStatus.FINISHED and game.mode != GameMode.PVP:
        # If it's bot's turn (PvB or BvB), let the bot play
        if game.mode == GameMode.PVB and game.current_turn == -1:  # Player vs Bot, Bot's turn
            ai_move = get_ai_move(board, game.bot_difficulty, game.current_turn)  # Bot's move
            game.apply_move(ai_move[0], ai_move[1], game.current_turn)
        elif game.mode == GameMode.BVB:  # Bot vs Bot, both players are bots
            ai_move = get_ai_move(board, BotDifficulty.HARD, game.current_turn)  # You can modify difficulty for BvB
            game.apply_move(ai_move[0], ai_move[1], game.current_turn)
        
        board = game.get_board()
        winner = check_winner(board)
        print(f"AI Move: {ai_move}, Board after AI move: {board}")
        is_draw = len(get_valid_moves(board)) == 0
        game.current_turn = -game.current_turn

        if winner or is_draw:
            game.status = GameStatus.FINISHED

        game.save()

    # Return the current board state if no one wins yet
    return JsonResponse({
        "game": game.serialize(),
        "aiMove": {
            "row": ai_move[0],
            "direction": ai_move[1],
        } if ai_move else None,
        "winner": winner if winner else None,
        "isDraw": is_draw,
    })
