# deer_chess

Mongolian Deer Chess with GUI written in Python3 with tkinter.

Deer Chess is a traditional board game from Mongolia, with some rules similar to those of checkers.

The dog tries to achieve checkmate, while the deer tries to capture as many dogs as possible or secure one of the hills.

Currently it is but an experimental GUI for deer chess, and there is no convenient interface like UCI.

# Run the Script

Execute the following command:

```sh
python3 main.py
```

# Play Chess

1. Choose your game mode
2. Click **New game**
3. When it is your turn, make your move by clicking the grid

*It will block the main thread when AI tries to make a move, which may cause some unpleasant behavior of the script, such as getting stuck.*

# Modify the Behavior of AI

Edit **file** ```godeer.py``` **class** ```AutoChess``` **method** ```get_next_move```.

# Requirements and Dependencies

The following Python packages are required to execute the script:

- math
- random
- tkinter
- typing

The following fonts are needed to show the GUI properly:

- Consolas
- Segoe UI Emoji
