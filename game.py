# Jay Villani - jhv7rr

# My game is a mix between the classic game breakout and pinball
# My 4 optional features are moving enemies, collectibles, a checkpoint (or save point), and multiple levels

import pygame
import gamebox
import random as r

# Camera setup
camera_x = 800
camera_y = 600
camera = gamebox.Camera(camera_x, camera_y)

# variables that will be used across multiple functions
player_ready = None
level1screen = None
level2screen = None
level3screen = None
checkpoint_reached = None
score = None
j = None
k = None
c = None
up_arrow = None
ball = None
paddle = None
balls = 0 # want this to carry over across levels so set it to zero here
board = None
background = None
boundary = None
left_angled_bumpers = None
right_angled_bumpers = None
diagonal_bumpers = None
left_angled_bumper2 = None
right_angled_bumper2 = None
square_bumpers = None
moving_bumpers = None
targets = None
target_dict = None
coins = None
coin_1 = None
coin_2 = None
coin_3 = None
coin_4 = None
gameover = None
level1 = None
level2 = None
level3 = None

# Start Screen
def start_screen(keys):
    """displays the start screen and sets up level 1 when the space bar is pressed"""
    global player_ready
    camera.clear('white')
    welcome = gamebox.from_image(367, camera_y/2, 'start_screen.png')
    welcome.scale_by(.65)
    camera.draw(welcome)
    if pygame.K_SPACE in keys:
        player_ready = True
        setup(1)

# Level 1 Screen
def level1_screen(keys):
    """displays the level 1 screen and starts level 1 when '1' is pressed"""
    global level1screen
    camera.clear('white')
    level1image = gamebox.from_image(367, camera_y/2, 'level1screen.png')
    level1image.scale_by(.65)
    camera.draw(level1image)
    if pygame.K_1 in keys:
        level1screen = False

# Level 2 Screen
def level2_screen(keys):
    """displays the level 2 screen and starts level 2 when '2' is pressed"""
    global level2screen
    camera.clear('white')
    level2image = gamebox.from_image(367, camera_y / 2, 'level2screen.png')
    level2image.scale_by(.65)
    camera.draw(level2image)
    if pygame.K_2 in keys:
        level2screen = False

# Level 3 Screen
def level3_screen(keys):
    """displays the level 3 screen and starts level 3 when '3' is pressed"""
    global level3screen
    camera.clear('white')
    level3image = gamebox.from_image(367, camera_y / 2, 'level3screen.png')
    level3image.scale_by(.65)
    camera.draw(level3image)
    if pygame.K_3 in keys:
        level3screen = False

# Game Over Screen
# displayed when no balls are left and the user hasn't surpassed the checkpoint
def game_over(keys):
    """displays the game over screen (with the player's score) and takes the player back to the start screen if
     's' is pressed"""
    global level1, level2, level3, balls, player_ready
    camera.clear('white')
    gameoverimage = gamebox.from_image(367, camera_y / 2, 'gameoverimage.png')
    gameoverimage.scale_by(.65)
    camera.draw(gameoverimage)

    # display which level and score the player achieved
    if level1:
        l = "LEVEL 1, "
    elif level2:
        l = "LEVEL 2 - "
    else:
        l = "LEVEL 3 - "
    s = str(score)
    player_score = gamebox.from_text(410, 245, l + s, 30, 'red')
    camera.draw(player_score)

    # if the player presses 's,' take them back to the start screen
    if pygame.K_s in keys:
        balls = 0
        player_ready = False # when this is false, the start screen is shown

# Game over for when the up arrow is pressed too many times
def game_over_cheater(keys):
    """displays the game over screen and takes the player back to the start screen if
     's' is pressed"""
    global balls, player_ready
    camera.clear('white')
    gameoverimage = gamebox.from_image(367, camera_y / 2, 'gameovercheater.png')
    gameoverimage.scale_by(.65)
    camera.draw(gameoverimage)

    if pygame.K_s in keys:
        balls = 0
        player_ready = False

# Diagonal Bumper Function
# The ball doesn't bounce correctly off of objects that are simply rotated to look like diagonals
# so this functions creates a combination of single pixels that make up a diagonal shape
def create_diagonal_45(starting_x, starting_y, ending_x, size, color):
    """creates 45 degree angle bumper going downwards from starting x to ending x"""
    diagonal = []
    for i in range(abs(int(starting_x - ending_x))):
        if starting_x < ending_x: # this diagonal will go down and to the right
            pixel = gamebox.from_color(starting_x + i, starting_y + i, color, 1, size)
        else: # this diagonal will go down and to the lef
            pixel = gamebox.from_color(starting_x - i, starting_y + i, color, 1, size)
        diagonal.append(pixel)
    return diagonal

# Set Up
# used for all three levels as the base
def setup(level):
    """sets all of the needed variables, starts the level corresponding to the given level argument"""
    global level1, level2, level3, level1screen, gameover, checkpoint_reached
    global boundary, left_angled_bumpers, right_angled_bumpers, diagonal_bumpers, square_bumpers, moving_bumpers
    global targets, target_dict, coins, coin_1, coin_2, score, j, k, c, up_arrow, ball, paddle, balls, board, background

    # input tells function which level we are in
    if level == 1:
        level1 = True
    if level == 2:
        level2 = True
    if level == 3:
        level3 = True

    level1screen = True
    gameover = False
    score = 0
    j = 0
    k = 0
    c = 0
    up_arrow = 0

    # on the first level the player gets 3 balls, only 1 additional on subsequent levels
    if level == 1:
        balls += 3
    else:
        balls += 1

    # ball
    ball = gamebox.from_circle(r.randrange(300, 511, 70), 120, 'dark blue', 4) # places the ball randomly at 300, 370, 440, or 510
    ball.speedx = r.randrange(0, 3, 2) - 1 # gives the ball a random speed of either -1 and 1
    ball.speedy = 1

    # paddle
    paddle = gamebox.from_color(camera_x / 2, 565, 'black', 60, 20)

    # checkpoint accomplished text
    checkpoint_reached = gamebox.from_text(400, 300, 'CHECKPOINT REACHED', 40, 'black') # used in level 2

    # head of the board
    backbox = gamebox.from_image(camera_x / 2, 0, 'backbox_lvl_1.png')
    backbox.scale_by(.30)
    backbox.top = camera.top

    # board
    board = gamebox.from_image(camera_x / 2, 0, 'board.png')
    board.scale_by(.55)
    board.top = backbox.bottom - 20

    background = [backbox, board]

    # boundary
    boundary_left = gamebox.from_color(board.left + 20, camera_y/2, 'black', 17, 410)
    boundary_right = gamebox.from_color(board.right - 20, camera_y/2, 'black', 17, 410)
    boundary_top = gamebox.from_color(camera_x/2, 0, 'black', boundary_right.left - boundary_left.right + 31, 17)
    boundary_top.bottom = boundary_left.top + 15
    boundary = [boundary_left, boundary_right, boundary_top]

    # diagonal bumpers
    exit_bumper_left = create_diagonal_45(board.left + 13, boundary_left.bottom - 12, board.left + 45, 26, 'black')
    exit_bumper_right = create_diagonal_45(board.right - 13, boundary_right.bottom - 12, board.right - 45, 26, 'black')
    right_angled_bumper_1 = create_diagonal_45(camera_x / 2 + 10, 250, camera_x / 2 + 50, 15, 'yellow')
    left_angled_bumper_1 = create_diagonal_45(camera_x / 2 - 10, 250, camera_x / 2 - 50, 15, 'yellow')

    # separate lists for different angled bumpers because they have a different effect on the ball
    left_angled_bumpers = [exit_bumper_right, left_angled_bumper_1]
    right_angled_bumpers = [exit_bumper_left, right_angled_bumper_1]
    # we can put all of the diagonals in the same list to draw them later: this is a list of lists
    diagonal_bumpers = [exit_bumper_left, exit_bumper_right, right_angled_bumper_1, left_angled_bumper_1]

    # square bumpers
    square_bumper1 = gamebox.from_color(camera_x/3 - 20, camera_y/2, 'red', 30, 30)
    square_bumper2 = gamebox.from_color(camera_x * (2/3) + 20, camera_y/2, 'red', 30, 30)
    square_bumpers = [square_bumper1, square_bumper2]

    # OPTIONAL FEATURES 1. Moving Enemies
    # bumpers that perpetually move side to side or up and down
    moving_bumper_1 = gamebox.from_color(camera_x/3 + 60, 400, 'black', 50, 15)
    moving_bumper_2 = gamebox.from_color(camera_x * (2/3) - 60, 400, 'black', 50, 15)
    moving_bumper_3 = gamebox.from_color(camera_x/2 + 45, 185, 'black', 75, 15)
    moving_bumpers = [moving_bumper_1, moving_bumper_2, moving_bumper_3]

    # targets
    target50_1 = gamebox.from_image(250, 200, 'target50_1.png')
    target50_2 = gamebox.from_image(550, 200, 'target50_1.png')
    target100_1 = gamebox.from_image(400, 210, 'target100_1.png')
    targets = [target50_1, target50_2, target100_1]
    for each in targets:
        each.scale_by(.1)

    # make a dictionary with 'targets' indices as keys and their corresponding points values as values
    # makes it easier to call the correct point values later
    target_dict = {0: 50, 1: 50, 2: 100}

    # OPTIONAL FEATURES 2. Collectibles
    # coins that give the user an extra ball
    coin_1 = gamebox.from_image(camera_x/2, 250, 'gold_coin.png')
    coin_2 = gamebox.from_image(boundary_left.right + 10, boundary_top.bottom + 10, 'gold_coin.png')
    coins = [coin_1, coin_2]
    for each in coins:
        each.scale_by(.1)

# Used exclusively for level 2
# adds on to the base of setup
def set_up2(level):
    """adds additional variables (gameboxes) from 'setup' to create level 2"""
    global level2screen, background, left_angled_bumper2, right_angled_bumper2, diagonal_bumpers, left_angled_bumpers
    global right_angled_bumpers, square_bumpers, moving_bumpers, targets, target_dict, coin_1, coin_2, coin_3, coin_4
    global coins, boundary
    level2screen = True
    setup(level)

    # change the backbox to level 2
    backbox2 = gamebox.from_image(camera_x / 2, 0, 'backbox_lvl_2.png')
    backbox2.scale_by(.30)
    backbox2.top = camera.top
    background.append(backbox2)

    # new diagonal bumpers
    left_angled_bumper2 = create_diagonal_45(camera_x / 2 - 110, 320, camera_x / 2 - 150, 15, 'blue')
    left_angled_bumpers.append(left_angled_bumper2)
    diagonal_bumpers.append(left_angled_bumper2)
    right_angled_bumper2 = create_diagonal_45(camera_x / 2 + 110, 320, camera_x / 2 + 150, 15, 'blue')
    right_angled_bumpers.append(right_angled_bumper2)
    diagonal_bumpers.append(right_angled_bumper2)

    # new square bumper
    square_bumper3 = gamebox.from_color(camera_x/2, 400, 'red', 40, 25)
    square_bumpers.append(square_bumper3)

    # new moving bumper
    moving_bumper_4 = gamebox.from_color(camera_x/2 - 45, 325, 'black', 75, 15)
    moving_bumpers.append(moving_bumper_4)

    # new target
    target200_1 = gamebox.from_image(400, 300, 'target200_1.png')
    target200_1.scale_by(.1)
    targets.append(target200_1)
    target_dict[3] = 200 # add the points to the target dictionary

    # new coins
    coin_3 = gamebox.from_image(camera_x/2, 380, 'gold_coin.png')
    coin_4 = gamebox.from_image(boundary[1].left - 10, boundary[2].bottom + 10, 'gold_coin.png')
    for each in [coin_3, coin_4]:
        coins.append(each)
    for each in [coin_1, coin_2]: # remove old coins
        coins.remove(each)
    for each in coins:
        each.scale_by(.1)

# Used for level 3
# adds on to set_up2
def set_up3(level):
    """adds additional variables (gameboxes) from 'set_up2' to create level 3"""
    global level3screen, background, left_angled_bumper2, right_angled_bumper2, left_angled_bumpers, right_angled_bumpers
    global diagonal_bumpers, moving_bumpers, boundary, targets, target_dict, coins, coin_3, coin_4
    level3screen = True
    set_up2(level)

    # change the backbox to level 3
    backbox3 = gamebox.from_image(camera_x / 2, 0, 'backbox_lvl_3.png')
    backbox3.scale_by(.30)
    backbox3.top = camera.top
    background.append(backbox3)

    # remove blue diagonal bumpers
    for each in [left_angled_bumper2, right_angled_bumper2]:
        diagonal_bumpers.remove(each)
    right_angled_bumpers.remove(right_angled_bumper2)
    left_angled_bumpers.remove(left_angled_bumper2)

    # new moving bumpers
    vertical_moving_bumper1 = gamebox.from_color(camera_x/2 - 90, 325, 'orange', 10, 50)
    vertical_moving_bumper2 = gamebox.from_color(camera_x/2 + 90, 325, 'orange', 10, 50)
    moving_bumper5 = gamebox.from_color(boundary[0].right + 22, 500, 'black', 20, 20)
    moving_bumper6 = gamebox.from_color(boundary[0].right + 20, boundary[2].bottom + 40, 'black', 30, 10)
    moving_bumper7 = gamebox.from_color(boundary[0].right + 20, boundary[2].bottom + 10, 'black', 30, 10)
    for each in [vertical_moving_bumper1, vertical_moving_bumper2, moving_bumper5, moving_bumper6, moving_bumper7]:
        moving_bumpers.append(each)

    # move the 50 targets down and make them smaller
    targets[0] = gamebox.from_image(250, 230, 'target50_1.png')
    targets[1] = gamebox.from_image(550, 230, 'target50_1.png')
    for each in [targets[0], targets[1]]:
        each.scale_by(.075)

    # new target
    target_500_1 = gamebox.from_image(boundary[0].right + 20, boundary[2].bottom + 25, 'target500_1.png')
    target_500_1.scale_by(.1)
    targets.append(target_500_1)
    target_dict[4] = 500 # add points value to dictionary

    # new coins
    coin_5 = gamebox.from_image(camera_x / 3 - 20, 275, 'gold_coin.png')
    coin_6 = gamebox.from_image(camera_x * (2 / 3) + 20, 275, 'gold_coin.png')
    for each in [coin_5, coin_6]:  # add new coins
        coins.append(each)
    for each in [coin_3, coin_4]:  # remove old coins
        coins.remove(each)
    for each in coins:
        each.scale_by(.1)

# Stationary Objects
def draw_stationary_objects1():
    """draws all of the stationary objects on the game board"""
    global background, boundary, diagonal_bumpers, square_bumpers, targets, coins
    camera.clear('black')
    for each in background:
        camera.draw(each)
    for each in boundary:
        camera.draw(each)
    for each in diagonal_bumpers:  # have to loop through a list of lists
        for i in range(len(each)):
            camera.draw(each[i])
    for each in square_bumpers:
        camera.draw(each)
    for each in targets:
        camera.draw(each)
    for each in coins:
        camera.draw(each)

# Moving Objects
def draw_moving_objects(keys, level):
    """draws the moving objects on the game board, sets paddle controls"""
    global paddle, ball, j, moving_bumpers, board, targets, k, up_arrow

    if level == 1: # each level has a different paddle sensitivity
        if pygame.K_RIGHT in keys:
            if paddle.speedx < 0:
                paddle.speedx += 3
            else:
                paddle.speedx += 1
        if pygame.K_LEFT in keys:
            if paddle.speedx > 0:
                paddle.speedx -= 3
            else:
                paddle.speedx -= 1
        if pygame.K_DOWN in keys:
            paddle.speedx = 0
    elif level == 2:
        if pygame.K_RIGHT in keys:
            if paddle.speedx < 0:
                paddle.speedx += 6
            else:
                paddle.speedx += 2
        if pygame.K_LEFT in keys:
            if paddle.speedx > 0:
                paddle.speedx -= 6
            else:
                paddle.speedx -= 2
        if pygame.K_DOWN in keys:
            paddle.speedx = 0
    elif level == 3:
        if pygame.K_RIGHT in keys:
            if paddle.speedx < 0:
                paddle.speedx += 7
            else:
                paddle.speedx += 7/3
        if pygame.K_LEFT in keys:
            if paddle.speedx > 0:
                paddle.speedx -= 7
            else:
                paddle.speedx -= 7/3
        if pygame.K_DOWN in keys:
            paddle.speedx = 0

    # up arrow bounces ball off
    if pygame.K_UP in keys:
        ball.speedx = 1
        ball.speedy = -2
        up_arrow += 1

    # makes sure paddle stays in bounds
    if paddle.left < board.left:
        paddle.speedx = 2
    if paddle.right > board.right:
        paddle.speedx = -2

    paddle.move_speed()

    # OPTIONAL FEATURES 1. Moving Enemies
    for i in range(len(moving_bumpers)):
        if i < 4: # the first 4 bumpers move side to side
            if (j // 90) % 2 == 0: # this gives a period of 3 seconds where this is true, then 3 seconds false, then true
                if i % 2 != 0: # 2 of the four will start by moving right
                    moving_bumpers[i].x += 1 # we will move the bumper 1 pixel per tick or 90 pixels in 3 seconds
                else:
                    moving_bumpers[i].x -= 1 # move it back left
            else:
                if i % 2 != 0: # the other two will start by moving left
                    moving_bumpers[i].x -= 1 # move it left
                else:
                    moving_bumpers[i].x += 1 # move it back right
        elif i < 6: # the 5th, 6th items in moving bumpers move up and down
            if (j // 150) % 2 == 0: # period of 5 seconds
                moving_bumpers[i].y -= 1 # we want to first move the bumper upwards
            else:
                moving_bumpers[i].y += 1 # then back down
        elif i < 7: # the 7th item moves side to side at the bottom of the screen at a fast rate
            if (j // 100) % 2 == 0: # period of a little over 3 seconds
                moving_bumpers[i].x += ((boundary[1].left - 22) - (boundary[0].right + 22))/100 # total distance covered / time
            else:
                moving_bumpers[i].x -= ((boundary[1].left - 22) - (boundary[0].right + 22))/100

    camera.draw(paddle)
    for each in moving_bumpers:
        camera.draw(each)

# draw ball and all of its interactions with objects
def draw_ball_interactions(level):
    """draws the ball and sets all the interactions it has with other objects on the game board"""
    global ball, balls, paddle, moving_bumpers, boundary, right_angled_bumpers, left_angled_bumpers, square_bumpers
    global targets, score, target_dict, player_ready, j, coins, gameover

    # speeds of the ball get changed by move_to_stop_overlapping, so if we capture the speed before that, we have it
    # available for use
    local_speedx = ball.speedx
    local_speedy = ball.speedy

    ball.speedy += .1 # gravity
    ball.move_speed()

    # interaction with paddle
    ball.move_to_stop_overlapping(paddle)
    if ball.bottom_touches(paddle) or ball.left_touches(paddle) or ball.right_touches(paddle):
        ball.speedx = local_speedx + (paddle.speedx / (level + 4)) # we add a little bit of the paddle's speed to the ball, a lesser fraction as the paddle speed increases between levels
        ball.speedy = - 6.5 # paddle will cause a consistent upward force on the ball

    # interaction with moving bumpers
    for each in moving_bumpers:
        ball.move_to_stop_overlapping(each)
        if ball.bottom_touches(each):
            ball.speedy = -local_speedy * .9
            ball.speedx = local_speedx
        if ball.top_touches(each):
            ball.speedy = -local_speedy * .75 # slow it down so the ball doesn't kick down really fast
            ball.speedx = local_speedx
        if ball.left_touches(each):
            ball.speedx = -local_speedx * .9
            ball.x += 1 # makes sure ball doesn't ride along the side
        if ball.right_touches(each):
            ball.speedx = -local_speedx * .9
            ball.x -= 1

    # interaction with boundaries
    for each in boundary:
        ball.move_to_stop_overlapping(each)
    for i in range(2):
        if ball.touches(boundary[i]): # sides of the boundary
            ball.speedx = -local_speedx * .75  # slow it down in the x direction a little
            # no change in y because we already have gravity
    if ball.touches(boundary[2]):  # top of the boundary
        ball.speedy = - local_speedy * .75

    # interaction with diagonal bumpers
    # have to go through left/right separately because of their angles
    for each in right_angled_bumpers:
        for i in range(len(each)):
            ball.move_to_stop_overlapping(each[i])
            if ball.bottom_touches(each[i]) or ball.left_touches(each[i]):
                ball.speedy = -local_speedy * .85
                if local_speedx > 0:  # because it is angled right, if the ball is coming from the left, it
                    # continues that way
                    ball.speedx = local_speedx
                else:
                    ball.speedx = - local_speedx # otherwise it gets shot back in the opposite direction
            if ball.top_touches(each[i]) or ball.right_touches(each[i]): # now we are looking at collisions from underneath
                ball.speedy = -local_speedy * .85
                if local_speedx < 0: # if the ball is moving to the left
                    ball.speedx = local_speedx # since the underside is angled left it continues that way
                else:
                    ball.speedx = -local_speedx

    for each in left_angled_bumpers:
        for i in range(len(each)):
            ball.move_to_stop_overlapping(each[i])
            if ball.bottom_touches(each[i]) or ball.right_touches(each[i]):
                ball.speedy = -local_speedy * .85
                if local_speedx < 0: # if the ball is moving left
                    ball.speedx = local_speedx # since top is angled left it continues that way
                else:
                    ball.speedx = -local_speedx
            if ball.top_touches(each[i]) or ball.left_touches(each[i]):
                ball.speedy = -local_speedy * .85
                if local_speedx > 0: # if the ball is moving right
                    ball.speedx = local_speedx # since the underside is angled right it continues that way
                else:
                    ball.speedx = -local_speedx

    # interaction with square bumpers
    for each in square_bumpers:
        ball.move_to_stop_overlapping(each)
        if ball.bottom_touches(each) or ball.top_touches(each):
            ball.speedy = -local_speedy*.75
            ball.speedx = local_speedx
            if local_speedx > 0: # move the ball left or right based on incoming direction of ball
                ball.x += 1 # makes sure ball doesn't get stuck on top of a bumper
            else:
                ball.x -= 1
        if ball.left_touches(each):
            ball.speedx = -local_speedx*.75
            ball.speedy = local_speedy
            ball.x += 1 # makes sure ball doesn't get stuck on the side
        if ball.right_touches(each):
            ball.speedx = -local_speedx * .75
            ball.speedy = local_speedy
            ball.x -= 1  # makes sure ball doesn't get stuck on the side

    # interaction with targets
    for i in range(len(targets)):
        if i == 4: # for the 500 point bumper
            if ball.touches(targets[i]):
                score += target_dict[i]
                ball.move_to_stop_overlapping(targets[i])
                ball.speedx = -local_speedx * 1.5 # want it to kick off extra fast
                ball.x += 2 # makes sure ball doesn't rack up too many points on it
        if ball.bottom_touches(targets[i]) or ball.top_touches(targets[i]):
            score += target_dict[i]
            ball.move_to_stop_overlapping(targets[i])
            ball.speedy = -local_speedy
            ball.speedx = local_speedx
            if local_speedx > 0: # if the ball is moving right move it right + 2
                ball.x += 2 # makes sure ball doesn't get stuck on top
            else:
                ball.x -= 2
        if ball.left_touches(targets[i]):
            score += target_dict[i]
            ball.move_to_stop_overlapping(targets[i])
            ball.speedy = local_speedy
            ball.speedx = -local_speedx
            ball.x += 1 # makes sure ball doesn't get stuck to side
        if ball.right_touches(targets[i]):
            score += target_dict[i]
            ball.move_to_stop_overlapping(targets[i])
            ball.speedy = local_speedy
            ball.speedx = -local_speedx
            ball.x -= 1

    ball.move_speed()

    # OPTIONAL FEATURES 2. Collectibles
    for each in coins:
        if ball.touches(each):
            balls += 1 # if the ball touches a coin, the user gets an extra ball and the coin is removed
            coins.remove(each) # stop drawing the coin

    if ball.top > camera.bottom: # if the ball falls below the bottom of the screen
        balls -= 1 # subtract 1 from the balls total
        if balls > 0: # if there are still balls left we will redraw a new one
            ball = gamebox.from_circle(r.randrange(300, 501, 70), 120, 'dark blue', 4)
            ball.speedx = r.randrange(0, 3, 2) - 1 # gives the ball a random speed between -1 and 1
        else: # if there are no balls left gameover
            gameover = True

    camera.draw(ball)

# Score and Balls
def draw_score_and_balls_left():
    """displays the score and balls left numbers on the scoreboard"""
    global balls, score, c, level2, checkpoint_reached
    balls_left = gamebox.from_text(565, 65, str(balls), 20, 'red')
    scoreboard = gamebox.from_text(395, 68, str(score), 20, 'red')

    # draw balls left and score text
    text = [balls_left, scoreboard]
    for each in text:
        camera.draw(each)

    # display checkpoint accomplished text for 3 seconds if the score is above 400 in level 2
    if level2 and c < 90: # 90 ticks is 3 seconds
        if score > 399:
            camera.draw(checkpoint_reached)
            c += 1

# Level 1 Tick
def tick_level_1(keys):
    """runs level 1"""
    global score, j, level1screen, level1, up_arrow, gameover

    if gameover:
        game_over(keys) # display gameover screen

    elif level1screen:
        level1_screen(keys) # display level 1 screen

    else: # play the level
        j += 1
        draw_stationary_objects1()
        draw_moving_objects(keys, 1)
        draw_ball_interactions(1)
        draw_score_and_balls_left()

    if score > 399: # move on to level 2
        set_up2(2)
        level1 = False

    # end the game if the up arrow is hit too many time
    if up_arrow > 15: # 15 may seem high but the counter is sensitive if you hold down the up arrow
        game_over_cheater(keys)


# OPTIONAL FEATURE 3. Multiple Levels
# Level 2 Tick
def tick_level_2(keys):
    """runs level 2"""
    global level2screen, j, score, gameover, level2, balls, up_arrow

    if gameover:
        # OPTIONAL FEATURE 4. Save Points
        if score > 399: # if the player has a certain number of points they can start over on level 2
            balls = 0
            set_up2(2)
        else:
            game_over(keys)

    elif level2screen:
        level2_screen(keys)

    else:
        j += 1
        draw_stationary_objects1()
        draw_moving_objects(keys, 2)
        draw_ball_interactions(2)
        draw_score_and_balls_left()

    if score > 599: # move on to level 3
        set_up3(3)
        level2 = False

    if up_arrow > 15:
        game_over_cheater(keys)

# Level 3 Tick
def tick_level_3(keys):
    """runs level 3"""
    global score, j, k, level3screen, level1, balls, up_arrow, gameover

    if gameover:
        game_over(keys)

    elif level3screen:
        level3_screen(keys)

    else:
        j += 1
        k += 1
        draw_stationary_objects1()
        draw_moving_objects(keys, 3)
        draw_ball_interactions(3)
        draw_score_and_balls_left()

    if up_arrow > 15:
        game_over_cheater(keys)

# Entire Tick Function
def tick(keys):
    """runs the entire game"""
    global player_ready, level1

    if player_ready:
        if level1:
            tick_level_1(keys)
        elif level2:
            tick_level_2(keys)
        elif level3:
            tick_level_3(keys)

    # if player ready is false display the start screen
    else:
        start_screen(keys)

    camera.display() # display everything that is drawn

# call the tick function 30 times per second
gamebox.timer_loop(30, tick)





