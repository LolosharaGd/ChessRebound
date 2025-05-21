# Chess Rebound
This is my another attempt at making a python pygame chess engine

# How to add a new piece
To add a new piece, you need to go to `custon_pieces.py` file and add a new class, like this

```python
class ExamplePiece(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("ExamplePiece")
```
Don't forget to change all `ExamplePiece` to your piece's internal name
###### Also, from now on I will refer to piece's internal name as inname, just so this explanation is shorter
The piece is created, now to actually make it do anything you can first set up primitive jumping moves
```python
class ExamplePiece(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("ExamplePiece")

        # VVV New code here VVV

        self.relative_moves = [
            Vector2(1, 0),
            Vector2(2, 1),
            Vector2(-1, 0),
            Vector2(-2, -1)
        ]
```
This has set up _jumping_ moves in these directions:
###### There is a difference between _jumping_ and _sliding_ moves, jumping moves jump over anything and are only affected by pieces on the destination, when sliding are, well, sliding, they can be stopped
```python
# P - Piece, m - move
# m
#  mPm
#     m
```

## Chess Rebound is in development right now