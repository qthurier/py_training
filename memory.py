# http://www.codeskulptor.org/#user24_4ru05ORJLT_20.py

# implementation of card game - Memory

import simplegui
import random

deck, exposed = [], []
click1, click2, turns, state = -1, -1, 0, 0

# helper function to initialize globals
def new_game():
    global deck, exposed, state, turns
    state, turns = 0, 0
    deck = range(8)
    deck.extend(deck)
    random.shuffle(deck)
    exposed = [False for x in range(len(deck))]  
    label.set_text("Turns = " + str(turns))
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, click1, click2, turns
    position = pos[0] // 50
    if not exposed[position]:
        exposed[position] = True
        if state == 0:
            click1 = position
            state = 1   
        elif state == 1:
            click2 = position
            state = 2    
            turns += 1
            label.set_text("Turns = " + str(turns))
        else:
            if deck[click1] == deck[click2]:
                exposed[click1], exposed[click2] = True, True
            else:
                exposed[click1], exposed[click2] = False, False
            click1, click2 = position, -1
            state = 1      
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(deck)):
        canvas.draw_text(str(deck[i]), (i*50 + 15, 60), 40, 'White')
    for i in range(len(exposed)):
        if not exposed[i]:
            canvas.draw_polygon([(i*50, 0), (i*50, 99), (i*50+49, 99), (i*50+49, 0)], 1, 'White', 'Green')       



# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
