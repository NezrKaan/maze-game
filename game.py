import random
import os
import time

# Function to clear the screen
def clear_screen():
    os.system('clear')

# Function to display the maze
def display_maze(maze, player_position, enemy_position):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if (x, y) == player_position:
                print('P', end='')
            elif (x, y) == enemy_position:
                print('E', end='')
            else:
                print(cell, end='')
        print()  # Newline for the next row

# Function to move the player or enemy
def move_character(position, direction, maze):
    x, y = position
    moves = {'w': (x, y-1), 's': (x, y+1), 'a': (x-1, y), 'd': (x+1, y)}
    new_position = moves.get(direction, position)
    new_x, new_y = new_position
    if maze[new_y][new_x] == '.':
        return new_position
    return position  # Return the original position if move is not possible

# Function to generate a simple maze using recursive backtracking
def generate_maze(width, height):
    def carve_passages_from(x, y, maze):
        directions = ['w', 'e', 'n', 's']
        random.shuffle(directions)

        for direction in directions:
            dx, dy = {'w': (-1, 0), 'e': (1, 0), 'n': (0, -1), 's': (0, 1)}[direction]
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == '#':
                maze[ny-dy][nx-dx] = '.'
                maze[ny][nx] = '.'
                carve_passages_from(nx, ny, maze)

    maze = [['#' for _ in range(width)] for _ in range(height)]
    start_x, start_y = random.randrange(1, width, 2), random.randrange(1, height, 2)
    maze[start_y][start_x] = '.'
    carve_passages_from(start_x, start_y, maze)
    return maze

# Function to move the enemy randomly
def move_enemy(enemy_position, maze):
    directions = ['w', 'a', 's', 'd']
    random.shuffle(directions)
    for direction in directions:
        new_position = move_character(enemy_position, direction, maze)
        if new_position != enemy_position:
            return new_position
    return enemy_position

# Main game function
def main():
    width, height = 20, 10  # Size of the maze
    player_position = (1, 1)  # Starting position of the player
    enemy_position = (width - 2, height - 2)  # Starting position of the enemy

    maze = generate_maze(width, height)

    while True:
        clear_screen()
        display_maze(maze, player_position, enemy_position)
        print("Use 'w' 'a' 's' 'd' to move. Type 'exit' to quit.")
        move = input("Your move: ").strip().lower()

        if move == 'exit':
            break
        elif move in ['w', 'a', 's', 'd']:
            player_position = move_character(player_position, move, maze)
            if player_position == enemy_position:
                print("You've been caught by the enemy! Game Over.")
                break
        else:
            print("Invalid move. Please enter 'w', 'a', 's', 'd', or 'exit'.")
            time.sleep(1)
            continue

        enemy_position = move_enemy(enemy_position, maze)
        if player_position == enemy_position:
            print("You've been caught by the enemy! Game Over.")
            break

        time.sleep(0.5)  # Add a small delay to make enemy movement visible

if __name__ == "__main__":
    main()
