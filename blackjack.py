# http://www.codeskulptor.org/#user25_exwYwvJvLN_36.py

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
pos_player = [150, 350]
pos_dealer = [150, 150]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
               
# define hand class
class Hand:
    def __init__(self):
        self.cards_list = []

    def __str__(self):
        return str([str(card) for card in self.cards_list])

    def add_card(self, card):
        self.cards_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust 
        value = sum([VALUES[card.get_rank()] for card in self.cards_list])
        if 'A' in [card.get_rank() for card in self.cards_list] and value + 10 <= 21:
            value += 10
        return value
   
    def draw(self, canvas, pos):
        i = 0
        for card in self.cards_list:
            card.draw(canvas, [pos[0] + CARD_SIZE[0]*i, pos[1]])
            i += 1
       
# define deck class 
class Deck:
    def __init__(self):
        self.cards_list = []
        for suit in SUITS:
            self.cards_list.extend([Card(suit, rank) for rank in RANKS])      

    def shuffle(self):
        random.shuffle(self.cards_list)

    def deal_card(self):
        return self.cards_list.pop()
    
    def __str__(self):
        return str([str(card) for card in self.cards_list])

#define event handlers for buttons
def deal():
    global outcome, in_play, score, deck, dealer_hand, player_hand
    if in_play == True:
        score -= 1
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    print "player : " + str(player_hand)
    print "dealer : " + str(dealer_hand)   
    in_play = True

def hit():
    global outcome, in_play, score
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())   
        if player_hand.get_value() > 21:
            outcome = "You have busted"
            in_play = False
            score -= 1
        print "player : " + str(player_hand)
        print "dealer : " + str(dealer_hand)
        print outcome        
       
def stand():
    global outcome, in_play, score
    if in_play:
        if player_hand.get_value() > 21:
            outcome = "You have busted"
            in_play = False
            score -= 1
        else:
            while(dealer_hand.get_value() < 17):
                dealer_hand.add_card(deck.deal_card())
            if dealer_hand.get_value() > 21:  
                outcome = "Dealer has busted"
                in_play = False
                score +=1
            else:
                if dealer_hand.get_value() >= player_hand.get_value():
                    outcome = "Dealer wins"
                    in_play = False
                    score -= 1
                else:
                    outcome = "You win"
                    in_play = False
                    score +=1
        print "player : " + str(player_hand)
        print "dealer : " + str(dealer_hand) 
        print outcome

# draw handler    
def draw(canvas):
    player_hand.draw(canvas, pos_player)
    dealer_hand.draw(canvas, pos_dealer)
    canvas.draw_text('Score : ' + str(score), (520, 30), 15, 'Black')
    canvas.draw_text('Blackjack', (20, 30), 25, 'Red')
    canvas.draw_text('Dealer :', (40, 200), 22, 'Black')
    canvas.draw_text('Player :', (40, 400), 22, 'Black')
    if in_play:
        canvas.draw_text('Hit or stand ?', (165, 305), 22, 'Black')
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos_dealer[0] + CARD_BACK_CENTER[0], pos_dealer[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    else:
        canvas.draw_text('New deal?', (165, 305), 22, 'Black')
        canvas.draw_text(outcome, (305, 305), 22, 'Black')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

