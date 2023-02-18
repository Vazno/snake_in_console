<h1 align="center">Snake Game</h1>
<h5 align="center">This is a snake game written in python using OOP and threading.</h5>
<p align="center">
    <img src="https://user-images.githubusercontent.com/96925396/219864957-ce4355e7-aa7e-41b8-84bf-344a77d01d6e.PNG">

---

Use the following keys to control the snake:

    up: "w"
    down: "s"
    left: "a"
    right: "d"

## Game Mechanics:

In this game, the snake grows by collecting apples that are randomly placed on the board. The game ends if the snake hits itself.

## Requirements:
`keyboard`
`colorama`

## Running the game:
To run the game, simply run the python file in your terminal:

`python snake_game.py`

## Customization:
You can customize the game by changing the values in the following variables:

    size: tuple containing the number of rows and columns of the game board.
    graphic: object containing the graphics for the snake, apple, empty cell, and border.
    snake_movement_repeat: float representing the speed at which the snake moves.
    apple_spawn_repeat: integer representing the number of seconds between apple spawns.
    fps: integer that holds fps (frames per seconds), which is used in while loop of print_matrix_loop() function, which prints the gameboard.
    show_score: boolean that is used to change the visibilness of scoreboard.
