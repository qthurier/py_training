# http://www.codeskulptor.org/#user24_vA3B66qw8d_10.py

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
VEL_RATE = 1

ball_pos = []
ball_vel = []
paddle1_pos, paddle2_pos = 0, 0
paddle1_vel, paddle2_vel = 0, 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [(WIDTH+BALL_RADIUS)/2, (HEIGHT+BALL_RADIUS)/2]
    # randomization of the velocity at the beginning
    # screen is updated 60 times a second
    h_vel=random.randrange(120, 240)/60
    v_vel=random.randrange(60, 80)/60
    # randomization of the vertical direction
    # we draw a uniform Bernouilli
    if random.randrange(0, 2) == 0:
        v_dir=1
    else:
        v_dir=-1
    # horizontal direction depends on the parameter direction
    if direction=='RIGHT':
        ball_vel=[h_vel,v_dir*v_vel]
    else:
        ball_vel=[-h_vel,v_dir*v_vel]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints  
    # reset the scores
    score1, score2 = 0, 0
    # randomization of the horizontal direction
    # we draw a uniform Bernouilli
    if random.randrange(0, 2) == 0:
        direction='RIGHT'
    else:
        direction='LEFT'
    # launch the ball
    spawn_ball(direction)
    # put the paddle on the middle
    paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")      
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # update paddle's vertical position
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    # turn paddle as polygons
    A1 = (0, paddle1_pos)
    B1 = (PAD_WIDTH, paddle1_pos)
    C1 = (0, paddle1_pos + PAD_HEIGHT)
    D1 = (PAD_WIDTH, paddle1_pos + PAD_HEIGHT)
    A2 = (WIDTH - PAD_WIDTH, paddle2_pos)
    B2 = (WIDTH - PAD_WIDTH + PAD_WIDTH, paddle2_pos)
    C2 = (WIDTH - PAD_WIDTH , paddle2_pos + PAD_HEIGHT)
    D2 = (WIDTH - PAD_WIDTH + PAD_WIDTH, paddle2_pos + PAD_HEIGHT)
    
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 5, 'Orange', 'Yellow')
    # management of the collisions
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:# here the ball touch the left gutter
        if A1[1] <= ball_pos[1] <= C1[1]:
            ball_vel[0] = - 1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else :
            # right player gets one point
            score2+=1
            # left player's service
            spawn_ball('RIGHT')
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - 1 - BALL_RADIUS:# here the ball touch the right gutter  
        if A2[1] <= ball_pos[1] <= C2[1]:
            ball_vel[0] = - 1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else :
            # left player gets one point
            score1+=1
            # right player's service
            spawn_ball('LEFT')
    # here the ball touch the top or the bottom
    elif (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS):
        # bounce
        ball_vel[1] = - ball_vel[1]

    # draw paddles
    c.draw_polygon([A1, B1, C1, D1], 12, 'Grey')
    c.draw_polygon([A2, B2, C2, D2], 12, 'Grey')
    
    #keep paddle on the screen    
    if A1[1] <= 0:
        paddle1_vel = 0
        paddle1_pos = 0
    if C1[1] >= HEIGHT:
        paddle1_vel = 0
        paddle1_pos = HEIGHT - PAD_HEIGHT
    if A2[1] <= 0:
        paddle2_vel = 0
        paddle2_pos = 0
    if C2[1] >= HEIGHT:
        paddle2_vel = 0
        paddle2_pos = HEIGHT - PAD_HEIGHT
        
    # draw scores
    c.draw_text(str(score1), (WIDTH/2 - 42, 20), 20, 'White')
    c.draw_text(str(score2), (WIDTH/2 + 30, 20), 20, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = -3
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 3
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = -3
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 3
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def restart():
    global score1, score2
    score1, score2 = 0, 0
    # randomization of the horizontal direction
    # we draw a uniform Bernouilli
    if random.randrange(0, 2) == 0:
        direction='RIGHT'
    else:
        direction='LEFT'
    # launch the ball
    spawn_ball(direction)
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('restart', restart, 70)

# start frame
new_game()
frame.start()

