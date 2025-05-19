## Side-Stacker Game

### Game rules

This is a connect-four, but the pieces stack on either side of the board instead of bottom-up.
Two players see a board, which is a grid of 7 rows and 7 columns. They take turn adding pieces to a row, on one of the sides. The pieces stack on top of each other, and the game ends when there are no spaces left available, or when a player has four consecutive pieces on a diagonal, column, or row.

For example, the board might look like this:

```
0 [ _ _ _ _ _ _ _ ]
1 [ o x _ _ _ _ o ]
2 [ x _ _ _ _ _ x ]
3 [ x _ _ _ _ _ o ]
4 [ o _ _ _ _ _ _ ]
5 [ _ _ _ _ _ _ _ ]
6 [ _ _ _ _ _ _ _ ]
```

in this case, it is x’s turn. If x plays (2, R), the board will look like this:

```
0 [ _ _ _ _ _ _ _ ]
1 [ o x _ _ _ _ o ]
2 [ x _ _ _ _ x x ]
3 [ x _ _ _ _ _ o ]
4 [ o _ _ _ _ _ _ ]
5 [ _ _ _ _ _ _ _ ]
6 [ _ _ _ _ _ _ _ ]
```

Each player sees the board in their frontend and can place moves that the other player sees, and the game displays “player 1 won” “player 2 lost” when the game is complete.

The implementation includes an AI bot that integrates with the game so players can compete against it.

### Bot difficulty levels

- Easy: the bot makes semi-random moves with basic rules
- Medium: the bot uses basic strategies and machine learning fundamentals
- Hard: the bot uses a complete ML model

### Game modes

- Player vs Player
- Player vs AI Bot
- AI Bot vs AI Bot

The game is stored in the backend using a relational database.

## Project Setup

### API

- Python
- Django Rest Framework
- SQLite3
- PyTorch/Numpy

```
pip install

daphne backend.asgi:application
```

### APP

- Typescript
- React.js
- Vite
- Websocket

```
yarn
yarn dev
```

## Possible Enhancements

- User authentication
- Save/restore game
- Pause game
- Adjust speed for Bot vs Bot mode
- Show last move
- Undo moves
