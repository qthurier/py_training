# http://www.codeskulptor.org/#user21_TWzHFGxbMw_12.py

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui, random, math

# initialize global variables used in your code
m = 0
M = 100
remaining_guess = int(math.ceil(math.log(M-m+1)/math.log(2)))

# helper function to start and restart the game
def new_game():
    global number, remaining_guess
    number = random.randrange(m, M)
    remaining_guess = int(math.ceil(math.log(M-m+1)/math.log(2)))

# define event handlers for control panel
def input_handler(text_input):
    if str.isdigit(text_input):
        input_guess(int(text_input))    
    else:
        print "Wrong input!"
    
def range100():
    global M
    M = 100
    new_game()
    
def range1000():
    global M
    M = 1000
    new_game()
    
def input_guess(guess):
    global remaining_guess
    remaining_guess -= 1
    print "Remaining guess: ", str(remaining_guess)
    if number == guess:
        print "Correct! Let's play again!"
        new_game()
    elif guess < number:
        print "Higher"
    else:
        print "Lower"
    if remaining_guess == 0:
        print "You loose.. Let's play again!"
        new_game()

    
# create frame
frame = simplegui.create_frame('Guess the number !', 10, 200)

# register event handlers for control elements
inp = frame.add_input('Guess !', input_handler, 65)
but_range100 = frame.add_button('[0; 100]', range100, 70)
but_range1000 = frame.add_button('[0; 1000]', range1000, 70)

# call new_game and start frame
new_game()
frame.start()

# always remember to check your completed program against the grading rubric
