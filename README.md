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
###### Also, from now on I will refer to piece's internal name as inname, just so this explanation is shorter
##### Don't forget to also add `(inname)Black.png` and `(inname)White.png` textures into `Textures` folder
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
###### Vector2 is a type that can store 2 floats, for more information you can check out `Morztypes.py`
This has set up _jumping_ moves in these directions:
```python
# P - Piece, m - move
# m
#  mPm
#     m
```
###### There is a difference between _jumping_ and _sliding_ moves, jumping moves jump over anything and are only affected by pieces on the destination, when sliding are, well, sliding, they can be stopped
The position `(0, 0)` of the board is located in the top-left corner.
X goes to the right, and Y goes down

Now, to make more complex behaviour you can try to add _sliding_ moves

To add _sliding_ moves, you can add them to `self.sliding_moves`
```python
class ExamplePiece(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("ExamplePiece")

        self.relative_moves = [
            Vector2(1, 0),
            Vector2(2, 1),
            Vector2(-1, 0),
            Vector2(-2, -1)
        ]

        # VVV New code VVV

        self.sliding_moves = [
            SlidingMove(Vector2(), self.forward * 2)
        ]
        # First argument is starting position, relative to the piece. Vector2() is just Vector2 with both x and y being 0
        # Second argument is direction, self.forward is direction up the board for the piece, depends on the color
```

Or you can add something even more complex, you can try to modify `self.get_moves_bitmap()`

Right now it just looks like this:

```python
def get_moves_bitmap(self, board_size, black_pieces_bitmap, white_pieces_bitmap, black_pieces, white_pieces) -> int:
    bitmap = 0

    bitmap |= self.calculate_jumping_moves(board_size, black_pieces_bitmap, white_pieces_bitmap, self.jumping_moves)

    for sliding_move in self.sliding_moves:
        bitmap |= self.calculate_sliding_move(board_size, black_pieces_bitmap, white_pieces_bitmap, sliding_move)

    return bitmap
```
To safely add anything to it without breaking everything that was here before, you need to pack it up into `super().get_moves_bitmap(arguments)`

Like this:
```python
def get_moves_bitmap(self, board_size, black_pieces_bitmap, white_pieces_bitmap, black_pieces, white_pieces) -> int:
    bitmap = super().get_moves_bitmap(board_size, black_pieces_bitmap, white_pieces_bitmap, black_pieces, white_pieces)

    # Do some of your stuff with bitmap

    return bitmap
```
###### If you don't know, bitmap is an integer, which in this case represents every square on the board with its bits, 1 for True and 0 for False. You can use self.position_to_bit() to not worry about the technical stuff
## Chess Rebound is in development right now