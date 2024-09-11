import keyboard
import time
import random

snake_body_coordinates = [(5, 0)]
directions = {
    "d": (0, 1),   # down
    "u": (0, -1),  # up
    "l": (-1, 0),  # left
    "r": (1, 0)    # right
}

last_direction = ["r"]  # Start with right
snake_speed = 0.5  # Snake's speed in seconds
move_timer = 0

def modify_snake(direction):
    """Modify the snake's movement"""
    x1, y1 = directions[direction]
    x2, y2 = snake_body_coordinates[-1]
    x3, y3 = (x1 + x2, y1 + y2)
    
    # Check for collision
    if (x3, y3) not in snake_body_coordinates[1:] and 0 <= x3 <= 9 and 0 <= y3 <= 9:
        snake_body_coordinates.append((x3, y3))
        snake_body_coordinates.pop(0)  
        return True
    return False

flag = True
while flag:
    board = [["." for _ in range(10)] for _ in range(10)]
    
    for i in snake_body_coordinates:
        x, y = i
        board[y][x] = "X"
    
    print("\033[H\033[J", end="")  # Képernyő törlése
    [print(*i) for i in board]
    print(snake_body_coordinates)
    
    # Handle arrow keys using the keyboard module
    if keyboard.is_pressed("left") and last_direction[-1] != "r":  # Left only if not moving right
        last_direction.append("l")
    elif keyboard.is_pressed("right") and last_direction[-1] != "l":  # Right only if not moving left
        last_direction.append("r")
    elif keyboard.is_pressed("up") and last_direction[-1] != "d":  # Up only if not moving down
        last_direction.append("u")
    elif keyboard.is_pressed("down") and last_direction[-1] != "u":  # Down only if not moving up
        last_direction.append("d")
    
    direction = last_direction[-1]
    
    # Update the snake's position based on the timer
    current_time = time.time()
    if current_time - move_timer >= snake_speed:  # Only move snake every `snake_speed` seconds
        if not modify_snake(direction):
            print("The snake collided! Game over.")
            flag = False
        move_timer = current_time  # Reset the timer for the next movement

    time.sleep(0.05)  # Small delay for better keypress detection



"""
import random

new_snake_body_coordinates = []

for i in snake_body_coordinates:

	new_snake_body_coordinates.extend([(i[0], i[1] +1), (i[0], i[1] -1), (i[0]+1, i[1] ), (i[0]-1, i[1]), (i[0], i[1])])


all_table_coordinates = []


for x in range(10):
	for y in range(10):
		
		all_table_coordinates.append((x,y))



potential_apple_position = list(set(all_table_coordinates) - set(new_snake_body_coordinates))

new_apple_position = random.choice(potential_apple_position)

return new_apple_position 




"""
