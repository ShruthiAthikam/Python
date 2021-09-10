#!/usr/bin/env python3

import random

#Function to create a deck of 52 cards and shuffle them
def createDeck():
    deck = []
    ranks = ["Ace","King","Queen","Jack"]
    suits = ["Clubs","Diamonds","Hearts","Spades"]
    for suit in suits:
        for item in ranks:
            card = {}
            card["suit"] = suit 
            card["rank"] = item
            if item == "Ace":
                card["points"] = 11
            else:
                card["points"] = 10
            deck.append(card)
        for i in range(2,11):
            card = {}
            card["suit"] = suit
            card["rank"] = str(i)
            card["points"] = i
            deck.append(card)
    random.shuffle(deck)
    return deck

#Function to create a deck for user or dealer
def playerDeck(deck):
    playerDeck = []
    for i in range(0,2):
        card = pickUpACard(deck)
        playerDeck.append(card)
    return playerDeck

#Function to pick up a random card from the deck and then remove it from the deck
def pickUpACard(deck):
    if len(deck) == 0:
        deck = createDeck()
    card = {}
    card = random.choice(deck)
    deck.remove(card)
    return card

#Function to check the total value of a hand
def checkScore(anyDeck):
    score = 0;
    counter = 0;
    for card in anyDeck:
        score += card["points"]

    #To check the number of Aces in a player's hand
    for card in anyDeck:
            if card["rank"] == "Ace":
                counter += 1
    #If there are more than one Ace in a hand, consider each Ace as 1 until the score becomes <= 21
    if counter > 1:
        while score > 21:
            score -= 10
    #If there is only one Ace in a hand,with score > 21 consider it as 1            
    elif counter == 1 and score > 21:
        for card in anyDeck:
            if card["rank"] == "Ace":              
                score -= 10
    return score
        

#For testing purpose
def main():   
    deck = createDeck()
    dealersDeck = playerDeck(deck)
    usersDeck = playerDeck(deck)
    
    print(dealersDeck)
    print("===================")
    print(usersDeck)
    print("===================")
    print(deck)
    print("===================")
    print(playerDeck(deck))


if __name__ == "__main__":
    main()
    






    

