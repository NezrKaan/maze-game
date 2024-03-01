import curses
from random import randint

# Initialize the screen
curses.initscr()
curses.start_color()  # Initialize colors
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Food color pair
curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Snake color pair

win = curses.newwin(20, 60, 0, 0)  # Create a new window: height, width, start_y, start_x
win.keypad(1)  # Accept keypad input
curses.noecho()  # Prevent input from displaying in the screen
curses.curs_set(0)  # Hide the cursor
win.border(0)  # Draw a border around the screen
win.nodelay(1)  # Make `win.getch()` non-blocking

# Snake and food
snake = [(4, 10), (4, 9), (4, 8)]  # Initial snake co-ordinates
food = (10, 20)  # First food co-ordinates
win.addch(food[0], food[1], '#', curses.color_pair(1))  # Print the food with red color

# Game logic
score = 0
ESC = 27
key = curses.KEY_RIGHT

while True:
    win.addstr(0, 2, 'Score: ' + str(score) + ' ')  # Print the score
    win.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120)  # Increase the speed of the snake as it gets longer

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        key = prev_key

    # Calculate the next coordinates for the snake head
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    snake.insert(0, (y, x))  # Append O(n) (consider deque for better performance)

    # Check if we hit the border or ourselves
    if y == 0 or y == 19 or x == 0 or x == 59 or snake[0] in snake[1:]:
        break

    # Check if snake gets the food
    if snake[0] == food:
        score += 1
        food = ()
        while food == ():
            food = (randint(1, 18), randint(1, 58))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '#', curses.color_pair(1))
    else:
        # Move snake
        last = snake.pop()
        win.addch(last[0], last[1], ' ')

    # Ensure the snake's head is always purple
    win.addch(snake[0][0], snake[0][1], '*', curses.color_pair(2))

    # Refresh the screen
    win.refresh()

# End the game
curses.endwin()
print(f"Made by NezrKaan 
Final score = {score}")
