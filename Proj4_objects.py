#!/usr/bin/env python3
import random
class Card:
    def __init__(self,suit,rank,points):
        self.suit = suit
        self.rank = rank
        self.points = points

    def __str__(self):
        return self.rank + " of " + self.suit

    def displayCard(self):
        return self.rank+self.suit[0]

class Deck:
    def __init__(self):
        self.deck = []
        ranks = ["Ace","King","Queen","Jack"]
        suits = ["Clubs","Diamonds","Hearts","Spades"]
        for suit in suits:
            for rank in ranks:
                if rank == "Ace":
                    self.deck.append(Card(suit,rank,11))
                else:
                    self.deck.append(Card(suit,rank,10))
            for i in range(2,11):
                self.deck.append(Card(suit,str(i),i))
        self.shuffle()


    def dealCard(self):
        randomCard = random.choice(self.deck)
        self.deck.remove(randomCard)
        return randomCard

    def shuffle(self):
        random.shuffle(self.deck)

    def count(self):
        return len(self.deck)

class Hand:
    def __init__(self):
        self.hand = []

    def addCard(self,card):
        self.hand.append(card)

    def getCard(self,index):
        return self.hand[index]


    def count(self):
        return len(self.hand)

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index == len(self.hand)-1:
            raise StopIteration
        self.__index += 1
        card = self.hand[self.__index]
        return card

    def points(self):
        countofAces = 0
        points = 0
        for card in self:
            points += card.points
            if card.rank == "Ace":
                countofAces += 1
        if countofAces > 1:
            while points > 21:
                points -= 10
        elif countofAces == 1 and points > 21:
            points -= 10
        return points

class Session:
    def __init__(self,sessionID, startTime, startMoney, stopTime, stopMoney):
        self.sessionID = sessionID
        self.startTime = startTime
        self.startMoney = startMoney
        self.stopTime = stopTime
        self.stopMoney = stopMoney
        
        
        
def main():
    print("Cards - Tester")
    print()

    # test Deck class
    print("DECK")
    deck = Deck()
    print("Deck created.")
    deck.shuffle()    
    print("Deck shuffled.")
    print("Deck count:", deck.count())
    print()

    # test Hand class
    print("HAND")
    hand = Hand()
    for i in range(4):
        hand.addCard(deck.dealCard())

    for card in hand:
        print(card)
        print(card.displayCard())
    print()

    print("Hand points:", hand.points())
    print("Hand count:", hand.count())
    print("Deck count:", deck.count())

if __name__ == "__main__":
    main()
