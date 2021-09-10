#!/usr/bin/env python3

from objects import Card , Deck , Hand
import db as d
import locale as lc
from decimal import Decimal
from datetime import time,datetime


#Displays the Welcome message
def display():
    print()
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    

#Function to validate and read Bet amount
def readBet(money):
    while True:
        try:
            isValid = False
            while not isValid:
                bet = Decimal(float(input("Bet amount: ")))
                bet = bet.quantize(Decimal("0.00"))
                #bet = round(float(input("Bet amount: ")),2)
                print()
                if bet > money and bet <= 1000:
                    print("Bet amount cannot be greater than the money you have.")
                    print()
                    isValid = False
                elif bet < 5:
                    print("Bet amount cannot be less than 5.")
                    print()
                    isValid = False
                elif bet > 1000:
                    print("Bet amount cannot be greater than 1000.")
                    print()
                    isValid = False
                else:
                    isValid = True
            return bet
        except ValueError:
            print("Invalid bet amount. Please try again.")
            print()


#Function to validate and read additional chips
def readAdditionalChips(money):    
    while True:
        try:
            isValid = False
            while not isValid:
                chips = Decimal(float(input("Chips:  ")))
                chips = chips.quantize(Decimal("0.00"))
                #chips = round(float(input("Chips:  ")),2)
                print()
                if money+chips < 5:
                    print("Chips do not reach the minimum bet amount. Add more chips.")
                    print()
                    isValid = False              
                else:
                    isValid = True
            return chips
        except ValueError:
            print("Invalid chips. Please try again.")
            print()

#Function to display cards in a hand
def displayCards(hand):
    for card in hand:
        print(card)

#Function to display the result of a game
def result(dealerHand,dealerPoints,userPoints,message,money):
    print("DEALER'S CARDS:")
    displayCards(dealerHand)
    print()
    print("YOUR POINTS: {}".format(userPoints))
    print("DEALER'S POINTS: {}".format(dealerPoints))
    print()
    print(message)    
    print("Money: " + str(lc.currency(money,grouping = True)))
    d.writeMoney(money)
    deck = Deck()
    print()

#Function to display the result of a game when player goes for 'stand'
def output(message,money):
    print(message)
    print("Money: " + str(lc.currency(money,grouping = True)))
    d.writeMoney(money)
    print()
    deck = Deck()

def main():
    a = lc.setlocale(lc.LC_ALL,"")
    if a == "C":
        lc.setlocale(lc.LC_ALL,"us")
    display()
    startTime = datetime.now()
    print("Start time: " ,startTime.strftime("%I:%M:%S %p"))
    
    choice = "y"
    while choice.lower() == "y":
        #Reading money from the file
        print()
        money = Decimal(d.readMoney())
        money = money.quantize(Decimal("0.00"))
        #money = round(float(d.readMoney()),2)
        print("Money: " + str(lc.currency(money,grouping = True)))
        if money < 5:
            print()
            ans = input("Money is below the limited bet amount (5). Do you want to buy more chips. (y/n) ")
            if ans.lower() == "y":
                money = money + readAdditionalChips(money)
                money = money.quantize(Decimal("0.00"))
                #money = round(money + readAdditionalChips(money),2)
                d.writeMoney(money)
                print("Money: " + str(lc.currency(money,grouping = True)))
            else:
                break

        #calling the function to read valid bet amount from user   
        bet = readBet(money)

        #Creating cards deck and decks for player and dealer and displaying them
        deck = Deck()
        dealerHand = Hand()
        dealerHand.addCard(deck.dealCard())
        dealerHand.addCard(deck.dealCard())
        userHand = Hand()
        userHand.addCard(deck.dealCard())
        userHand.addCard(deck.dealCard())
        print("DEALER'S SHOW CARD:")
        print(dealerHand.getCard(0))
        print()
        print("YOUR CARDS:")
        displayCards(userHand)
        print()
        userPoints = userHand.points()
        dealerPoints = dealerHand.points()

        #Checking for natural blackjacks for both dealer and player
        if userPoints == 21:
            if dealerPoints == 21:
                result(dealerHand,21,21,"You and the dealer both have a natural blackjack. Its a draw.",money)
                choice = input("Play again? y/n:  ")
                continue
            
            else:
                money = money + Decimal("1.5")*bet
                money = money.quantize(Decimal("0.00"))
                result(dealerHand,dealerPoints,21,"Congratulations!!Natural Blackjack! You won!!",money)
                choice = input("Play again? y/n:  ")
                continue
            
        elif dealerPoints == 21: 
            money = money - bet
            money = money.quantize(Decimal("0.00"))
            result(dealerHand,21,userPoints,"Sorry. You lose. Dealer has a natural Blackjack.",money)
            choice = input("Play again? y/n:  ")
            continue
                  
        flag = False
        flag1 = False
        userChoice = input("Hit or Stand? (hit/stand): ")

        #User has the options of hit/stand
        while userChoice.lower() == "hit":
            userHand.addCard(deck.dealCard())
            print()
            print("YOUR CARDS:")
            displayCards(userHand)
            print()
            userPoints = userHand.points()
            dealerPoints = dealerHand.points()

            #Checking for user score = 21 
            if userPoints == 21:
                print("You have reached 21 points.")
                flag1 = True                
                break

            #Checking for user bust over 21                   
            elif userPoints > 21:
                money = money - bet
                money = money.quantize(Decimal("0.00"))
                result(dealerHand,dealerPoints,userPoints,"Bust!Sorry.You lose",money)
                choice = input("Play again? y/n:  ")              
                flag = True
                break
         
            else:
                userChoice = input("Hit or Stand? (hit/stand): ")
                
        if flag:
            continue

        #User opting for stand
        if userChoice.lower() == "stand" or flag1:
            flag1 = False    
            print()
            print("DEALER'S CARDS:")
            displayCards(dealerHand)
            print()
            userPoints = userHand.points()
            dealerPoints = dealerHand.points()

            #Ensuring the dealer's hand has a total of 17
            while dealerPoints < 17:
                print("Dealer's hand has total points less than 17.")
                dealerHand.addCard(deck.dealCard())
                print("DEALER CARDS:")
                displayCards(dealerHand)
                print()
                dealerPoints = dealerHand.points()
            print("YOUR POINTS: " + str(userPoints))
            print("DEALER'S POINTS: " + str(dealerPoints))
            print()

            #Checking for different cases of user and dealer scores
            if dealerPoints > 21 or userPoints > dealerPoints:
                money = money+bet
                money = money.quantize(Decimal("0.00"))
                output("Congratulations!!You won!!",money)
                choice = input("Play again? y/n:  ")
                continue          

            elif userPoints == dealerPoints: 
                money = money.quantize(Decimal("0.00"))
                output("Its a draw.",money)
                choice = input("Play again? y/n:  ")
                continue
            
            elif dealerPoints == 21 or userPoints < dealerPoints: 
                money = money-bet
                money = money.quantize(Decimal("0.00"))
                output("Sorry.You lose",money)
                choice = input("Play again? y/n:  ")
                continue 

            
        
        choice = input("Play again? y/n:  ")
        deck = Deck()     

    print()
    endTime = datetime.now()
    print("Stop time: " ,endTime.strftime("%I:%M:%S %p"))
    elapsedTime = endTime - startTime
    minutes = elapsedTime.seconds//60
    seconds = elapsedTime.seconds%60
    hours = minutes//60
    minutes = minutes%60
    duration = time(hours,minutes,seconds)
    print("Elapsed time: ", duration)
    print("Come back soon!")
    print("Bye!")
    


if __name__ == "__main__":
    main()

            

