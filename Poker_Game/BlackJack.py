import random 
import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk
import os

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Build card image mapping
card_image_map = {}
image_folder = r"INPUT PATH TO Cards FILE HERE"

suit_lookup = {'H': 'Hearts', 'S': 'Spades', 'D': 'Diamonds', 'C': 'Clubs'}
for fname in os.listdir(image_folder):
    if fname.endswith(".png"):
        parts = fname.split('_of_')
        if len(parts) == 2:
            rank = parts[0]
            suit_letter = parts[1][0]  # 'H', 'S', 'D', 'C'
            suit = suit_lookup.get(suit_letter)
            if suit:
                card_image_map[(rank, suit)] = os.path.join(image_folder, fname)

root = tk.Tk()
root.title("Blackjack")
root.geometry("800x600")

bg_image = Image.open(r"INPUT PATH TO blackjack_bg.jpg FILE HERE")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

dealer_label = tk.Label(root, text="Dealer's Hand", font=("Arial", 16), bg="darkgreen", fg="white")
dealer_label.pack()

player_label = tk.Label(root, text="Player's Hand", font=("Arial", 16), bg="darkgreen", fg="white")
player_label.pack(side=tk.BOTTOM, padx=9, pady=10)

message_label = tk.Label(root, text="", font=("Arial", 16), bg="darkgreen", fg="white")
message_label.pack()

hit_button = tk.Button(root, text="Hit", font=("Arial", 16), bg="darkgreen", fg="white")
hit_button.pack(side=tk.LEFT, padx=20, pady=20)

stand_button = tk.Button(root, text="Stand", font=("Arial", 16), bg="darkgreen", fg="white")
stand_button.pack(side=tk.RIGHT, padx=20, pady=20)

player_cards_frame = tk.Frame(root, bg="darkgreen")
player_cards_frame.pack(side=tk.BOTTOM, pady=20, anchor="s")

dealer_cards_frame = tk.Frame(root, bg="darkgreen")
dealer_cards_frame.pack(side=tk.TOP, pady=20, anchor="n")

def update_labels():
    for widget in player_cards_frame.winfo_children():
        widget.destroy()
    for widget in dealer_cards_frame.winfo_children():
        widget.destroy()
        #Show Player Cards
    for card in player_hand.cards:
        img = Image.open(card.image_filename())
        img = img.resize((80, 120))
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(player_cards_frame, image=photo, bg="darkgreen")
        lbl.image = photo
        lbl.pack(side=tk.LEFT, padx=5)
        #Show Dealer Cards
    for card in dealer_hand.cards:
        img = Image.open(card.image_filename())
        img = img.resize((80, 120))
        photo = ImageTk.PhotoImage(img)
        lbl = tk.Label(dealer_cards_frame, image=photo, bg="darkgreen")
        lbl.image = photo
        lbl.pack(side=tk.LEFT, padx=5)
        #Update Labels
    player_label.config(text="Player's Hand: " + ', '.join(str(card) for card in player_hand.cards) + " Value: " + str(player_hand.get_value()))
    dealer_label.config(text="Dealer's Hand: " + ', '.join(str(card) for card in dealer_hand.cards) + " Value: " + str(dealer_hand.get_value()))

def new_game():
    global deck, player_hand, dealer_hand
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal(1)[0])
    dealer_hand.add_card(deck.deal(1)[0])
    player_hand.add_card(deck.deal(1)[0])
    dealer_hand.add_card(deck.deal(1)[0])
    hit_button.config(state="normal")
    stand_button.config(state="normal")
    message_label.config(text="")
    update_labels()

new_game_button = tk.Button(root, text="New Game", font=("Arial", 16), command=new_game, bg="darkgreen", fg="white")
new_game_button.pack(side=tk.RIGHT, anchor="se", padx=20, pady=20)

def hit():
    player_hand.add_card(deck.deal(1)[0])
    update_labels()
    root.update()
    if player_hand.get_value() > 21:
        message_label.config(text="You busted! Dealer wins.")
        hit_button.config(state="disabled")
        stand_button.config(state="disabled")
    

def stand():
    # Dealer's turn logic
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal(1)[0])
        update_labels()
        root.update()  # Refresh the GUI

    # Determine Winner (this block should NOT be inside the while loop)
    player_value = player_hand.get_value()
    dealer_value = dealer_hand.get_value()

    if dealer_value > 21:
        message_label.config(text="Dealer busted! You win.")
    elif dealer_value > player_value:
        message_label.config(text="Dealer wins! You lose.")
    elif dealer_value < player_value:
        message_label.config(text="You win!")
    else:
        message_label.config(text="It's a tie! Play again.")

    hit_button.config(state="disabled")
    stand_button.config(state="disabled")
    update_labels()


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
            return f"{self.rank}{suit_symbols[self.suit]}"
    
    def __repr__(self):
            return self.__str__()
    
    def image_filename(self):
         # For face cards, rank is 'A', 'K', etc.; for numbers, it's '2', '3', etc.
        key = (self.rank[0].upper() if self.rank in ['Ace', 'Jack', 'Queen', 'King'] else self.rank, self.suit)
        return card_image_map.get(key, "Cards/back.png")
        

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards
    
class Hand:
    def __init__(self):
        self.cards = []
    def add_card(self, card):
        self.cards.append(card)
    def get_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.rank == 'Ace':
                aces += 1
                value += 11
            else:
                value += int(card.rank)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

hit_button.config(command=hit)
stand_button.config(command=stand)

root.mainloop()


