#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Artificial Intelligence Lab Skills
Final Project - Macao

Author: Isabela-Maria Negoita
Group: 85
Average hours spent: 8
"""

import random


class Player(object):

    """
    Interface class used to represent a player of the game

    Attributes:
        skip_turn: boolean which indicates whether the player's turn should be skipped
        index: the index of the player
        hand: stores the player's cards

    Methods:
        set_name():
            setter for the player's name
        get_name():
            getter for the player's name
        show_deck():
            print out the cards in a player's deck
    
    """
    def __init__(self, deck, index):
        #give the player a name
        self.set_name()

        #self.force_draw = False
        self.skip_turn = False
        #give the player an index to be easily identifiable
        self.index = index
        #deal the player 5 cards to start the game with
        self.hand = []
        for i in range (5):
            self.hand.append(deck.deal_card())
        
        if isinstance(self, HumanPlayer):
            self.show_deck()

    def set_name(self):
        pass

    def get_name(self):
        return self.name
    
    def show_deck(self):
        hand_str = ""
        for card in self.hand:
            hand_str = hand_str + "[" + card.rank + " of " + card.suit + "]" + " | "
        print("This is your current hand: ", hand_str)

class HumanPlayer(Player):
    """
    Used to represent a human player. Extends the Player class.
    
    Methods:
        set_name():
            asks the human for their name and sets it
        play():
            asks the player for a move and returns it
        """
    
    def set_name(self):
        self.name = input("What is your name? ")

    def play(self, last_card, deck):

        #check if the suit or rank that the player chose matches
        #ask the player for a move and return it

        self.show_deck()

        #check if the player has any move it could make
        canPlay = False
        for card in self.hand:
            if card.suit == last_card.suit or card.rank == last_card.rank:
                canPlay = True
            
        
        if canPlay == True:

            while True:
                try:
                    move = input("\nWhat card would you like to play? Please write it as '/rank/ of /suit/' ")

                    #allow the player to quit whenever
                    if move.lower() == "quit" or move.lower() == "q":
                        return "q"

                    #allow the player to simply draw a card, without putting one down
                    if move.lower() == "pass":
                        print("You've chosen to not put down a card.\n You will now draw one instead.")
                        self.hand.append(deck.deal_card())
                        self.show_deck()
                        return last_card
                    
                    #check if the player says macao when required
                    if (len(self.hand) == 1):
                        if (move.lower() != "macao"):
                            print("Uh oh! You have only one card, why didn't you say MACAO? :(")
                            print("You're gonna have to draw 5 now....")
                            for i in range(5):
                                self.hand.append(deck.deal_card())
                            self.show_deck()

                        else:
                            print("\nGood job, you remembered to say Macao!")

                        move = input("\nWhat card would you like to play? Please write it as '/rank/ of /suit/' ")

                    inputs = move.split(" ")
                    rank = inputs[0]
                    suit = inputs [2]
                    choice = Card(rank, suit)

                    #check if the card is a valid move
                    #check if it matches the one on the table
                    matches = False
                    if choice.suit == last_card.suit:
                        matches = True

                    if choice.rank == last_card.rank:
                        matches = True

                    if choice not in self.hand:
                        raise NotInHandError
                    
                    if matches == False:
                        raise MatchError

                    self.hand.remove(choice)
                    self.show_deck()
                    return choice

                except (ValueError, IndexError):
                    print("\nInvalid input. Please enter a card in the format '/rank/ of /suit/', with appropiate capitalisation.")

                except NotInHandError as e:
                    print(str(e))
                    self.show_deck()

                except MatchError as e:
                    print(str(e))
                    print("Look for a card whose suit is ", last_card.suit, "or whose rank is ", last_card.rank)
        
        else:
            print("You have no moves you can make! You will draw a card.")
            self.hand.append(deck.deal_card())
            self.show_deck()

            return last_card
    
class ComputerPlayer(Player):
    """
    Represents a computer player which performs a random move.
    Extends the Player class.
    
    Methods:
    set_name():
        sets the name of the computer player to "Computer"
    play(): 
        plays a randomly generated valid move
    """

    def set_name(self):
        self.name = "Computer"

    def play(self, last_card, deck):
        print("Waiting for the computer to make a move...")

        if len(self.hand) == 1:
            print("The computer says MACAO!")

        for card in self.hand:
            
            if (card.suit == last_card.suit) or (card.rank == last_card.rank):
               self.hand.remove(card)
               print("The computer has chosen ", card)
               return card
           
        print("The computer has no matching cards. It will draw one.")
        self.hand.append(deck.deal_card())
        return last_card

class Card(object):
    """
    Representation of a play card

    Attributes:
        rank: rank of the card
        suit: suit of the card
    
    Methods:
        __str__(): returns a string representation of the card
        __eq__(): checks if two play cards are the same
    """
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return "[" + self.rank + " of " + self.suit + "]"
    
    def __eq__(self, other):

        if (self.rank == other.rank) and (self.suit == other.suit):
            return True
        return False

class Deck(object):
    """
    Representation of a deck of cards, shuffled, excluding Jokers

    Attributes:
        ranks: all the valid ranks in a regular deck
        suits: all the valid suits in a regular deck
        deck: the deck itself; a list of Card objects
        played_cards: stores the cards that have been played so far, are not in players' hands

    Methods:
        shuffle(): shuffles the deck
        deal_card(): removes a card from the deck and returns it
                    resets the deck once it is empty
        __str__(): returns a string representation of the deck and the cards in it

    """
    
    def __init__(self):
        #we initialise the deck for the game
        #this will represent the cards left on the table to draw from
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.deck = [Card(rank, suit) for rank in ranks for suit in suits]
        self.shuffle()
        self.played_cards = []

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        
        if len(self.deck) != 0:
            return self.deck.pop()
        
        #once the initial deck runs out, take the already played cards, shuffle and reuse them
        random.shuffle(self.played_cards)
        self.deck = self.played_cards
        self.played_cards = []
        return self.deck.pop()
    
    def __str__(self):
        deck_str = " "
        for card in self.deck:
            deck_str = deck_str + "[" + card.rank + " of " + card.suit + "]" + " | "
        return deck_str
 
class NotInHandError(Exception):
    """
    Error raised when a players chooses a card which is not in their deck.
    Extends the Exception class

    Methods:
        __str__(): returns the error message
    """
    def __str__(self):
        return "The card chosen is not in your hand!\nBe mindful of capitalisation :)"
    
class MatchError(Exception):
    """
    Error raised when a player tries to make an illegal move
    Extends the exception class

    Methods:
        __str__(): returns the error message
    """
    def __str__(self):
        return "The card chosen does not match the one on the table!"
    
class Macao(object):
    """
    Representation of a game of Macao

    Attributes:
        playDeck: the card deck of the game
    
    Methods:
        play(): plays through a game of Macao
    """

    def __init__(self):
        self.playDeck = Deck()

    def play(self):

        print("\n", "_"*10, "\n")
        print("\nWelcome to the game of Macao!\n")

        #check if the number of players is between two and five
        while True:
            try:
                playersNum = int(input("How many players will participate in the game? "))

                
                playersNum = int(playersNum)
                if (playersNum >= 2) and (playersNum <= 5):
                    break
                else:
                    raise ValueError
            except ValueError as e:
                print("Error: Please enter a number between 2-5.")

        players = []
        count = 1
        
        #initialise players
        for i in range(playersNum):
            print("\nLet's initialise player ", count, "!")
            while True:
                try:
                    answer = input("For a human player, input 'H'. To play against a computer, input 'C'. ")
                    if answer.upper() == 'C':
                        print("Generating computer player...\n")
                        players.append(ComputerPlayer(self.playDeck, count))
                        break
                    elif answer.upper() == 'H':
                        players.append(HumanPlayer(self.playDeck, count))
                        break
                    else:
                        raise ValueError("Invalid input. Please enter 'H' or 'C'.")
                except ValueError as e:
                    print("Error: ", e)

            count += 1

        force_draw = False
        draw_num = 0
        
        round_number = 1
        player_number = 0
        current_player = players[player_number]
        last_card = self.playDeck.deal_card()
        self.playDeck.played_cards.append(last_card)


        while True:

            print("\n", "_"*10, "\n")
            print("Round ", round_number)
            print("\nIt is ", current_player.name,"'s turn")

            if current_player.skip_turn == True:
                print("A \"4\" was played, therefore this turn will be skipped.")
                current_player.skip_turn = False

                #before you move on to the next player, check if there was a force draw ongoing
                if force_draw == True:
                    print("\nYou have to draw ", draw_num, "cards")
                    for i in range(draw_num):
                        current_player.hand.append(self.playDeck.deal_card())
                    current_player.show_deck()
                    force_draw = False
                    draw_num = 0

                #change over to the next player before we move on
                player_number += 1
                if player_number >= playersNum:
                    player_number = 0
                current_player = players[player_number]
                round_number += 1 
                continue

            #make their move, change the last card
            print("The card on the table is ", last_card, "\n")
            previous_card = last_card
            last_card = current_player.play(last_card, self.playDeck)

            #allow the player to quit
            if isinstance(last_card, str) and last_card == "q":
                print("Quitting current game...")
                return
            
            if last_card not in self.playDeck.played_cards:
                self.playDeck.played_cards.append(last_card)
                
            #check if hand is empty aka winner 
            if len(current_player.hand) == 0:
                print(current_player.name, "has won the game!")
                break

            #check that a move was actually made
            if last_card != previous_card:

                #if A was played by a human player, allow the player to change the suit or rank
                if (isinstance(current_player, HumanPlayer) and last_card.rank == 'A'):
                    print("\nYou've played an A, which grants you the power to change the suit or rank.")
                    while True:
                        change = input("\nWould you like to change the suit or rank? ") 

                        if not (change.lower() == "suit" or change.lower() == "rank"):
                            print("Please choose between \"suit\" or \"rank\". ")
                            continue
                        
                        new = input("\nWhat would you like to change it to? ")
                        #ensure they choose a valid suit or rank
                        while not ( (change == "suit" and new in ['Clubs', 'Diamonds', 'Hearts', 'Spades']) or (change == "rank" and new in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])):
                            print("Please enter a valid suit or rank, depending on what you chose. ")
                            print("Suits are represented by ['Clubs', 'Diamonds', 'Hearts', 'Spades']")
                            print("Ranks are represented by ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']")
                            
                            new = input("\nWhat would you like to change it to? ")
                            continue

                        if change == "rank":
                            new_card = Card(new, previous_card.suit)
                            last_card = new_card
                            break
                        elif change == "suit":
                            new_card = Card(previous_card.rank, new)
                            last_card = new_card
                            break
                        

                #force draw 2 or add to the previous force draw
                elif last_card.rank == '2':
                    draw_num += 2
                    force_draw = True
                    print("A force draw card has been played. The next player will have to draw ", draw_num)

                #force draw 3 or add to the previous force draw
                elif last_card.rank == '3':
                    draw_num += 3
                    force_draw = True
                    print("A force draw card has been chosen. The next player will have to draw ", draw_num)
                
                #if the player didn't play 2 or 3, deal them the force draw cards
                elif force_draw == True:

                    if isinstance(current_player, HumanPlayer):
                        print("\nYou have to draw ", draw_num, "cards")
                        for i in range(draw_num):
                            current_player.hand.append(self.playDeck.deal_card())
                        current_player.show_deck()

                    elif isinstance(current_player, ComputerPlayer):
                        print("\nThe computer has force drawn ", draw_num, "cards")
                        for i in range(draw_num):
                            current_player.hand.append(self.playDeck.deal_card())

                    force_draw = False
                    draw_num = 0


            #switch players
            player_number += 1
            if player_number >= playersNum:
                player_number = 0
            current_player = players[player_number]
            round_number += 1 

            #make the next player skip their turn if a 4 was played
            if last_card != previous_card:
                if last_card.rank == '4':
                    current_player.skip_turn = True



if __name__ == "__main__":
    game = Macao()
    game.play()

    while True:

        answer = (input("\nWould you like to play another game? [yes/no] ")).lower()
        if (answer.lower() == "yes" or answer.lower() == "y"):
            game = Macao()
            game.play()
        elif (answer.lower() == "no" or answer.lower() == "n"):
            break
        else:
            print("Please answer yes or no. ")
    print("\nGoodbye!")
    
    