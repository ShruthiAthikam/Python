#!/usr/bin/env python3

from objects import Card , Deck , Hand , Session
import db as d
import locale as lc
from decimal import Decimal
from datetime import time,datetime
import tkinter as tk
from tkinter import ttk
import sys

class Blackjack(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent,padding = "10 10 10 10")
        self.parent = parent
        self.pack(fill = tk.BOTH, expand = True)
        self.grid_configure(columnspan = 3)
        self.money = tk.StringVar()
        self.bet = tk.StringVar()
        self.dealerCards = tk.StringVar()
        self.dealerPoints = tk.StringVar()
        self.userCards = tk.StringVar()
        self.userPoints = tk.StringVar()
        self.result = tk.StringVar()
        self.initComponents()
        
        self.startTime = datetime.now()
        d.create_session()
        self.startMoney = Decimal(d.get_last_session().stopMoney).quantize(Decimal("0.00"))
        self.money.set(lc.currency(self.startMoney,grouping = True))
        self.sessionID  = d.get_last_session().sessionID + 1
       

    def initComponents(self):
        ttk.Label(self, text = "Money:").grid(column = 0, row = 0, sticky = tk.E)
        ttk.Entry(self,width = 25, textvariable = self.money,state = "readonly").grid(column = 1,row = 0,sticky = tk.W)
        ttk.Label(self, text = "Bet:").grid(column = 0, row = 1, sticky = tk.E)
        ttk.Entry(self,width = 25, textvariable = self.bet).grid(column = 1,row = 1,sticky = tk.W)       
        ttk.Label(self, text = "DEALER").grid(column = 0, row = 2, sticky = tk.E)
        ttk.Label(self, text = "Cards:").grid(column = 0, row = 3, sticky = tk.E)
        ttk.Entry(self,width = 50, textvariable = self.dealerCards,state = "readonly").grid(column = 1,row = 3,sticky = tk.W,columnspan = 2)
        ttk.Label(self, text = "Points:").grid(column = 0, row = 4, sticky = tk.E)
        ttk.Entry(self,width = 25, textvariable = self.dealerPoints,state = "readonly").grid(column = 1,row = 4,sticky = tk.W)
        ttk.Label(self, text = "YOU").grid(column = 0, row = 5, sticky = tk.E)
        ttk.Label(self, text = "Cards:").grid(column = 0, row = 6, sticky = tk.E)
        ttk.Entry(self,width = 50, textvariable = self.userCards,state = "readonly").grid(column = 1,row = 6,sticky = tk.W,columnspan = 2)
        ttk.Label(self, text = "Points:").grid(column = 0, row = 7, sticky = tk.E)
        ttk.Entry(self,width = 25, textvariable = self.userPoints,state = "readonly").grid(column = 1,row = 7,sticky = tk.W)
        self.makeButtons1()
        ttk.Label(self, text = "RESULT:").grid(column = 0, row = 9, sticky = tk.E)
        ttk.Entry(self,width = 50, textvariable = self.result,state = "readonly").grid(column = 1,row = 9,sticky = tk.W,columnspan = 2)
        self.makeButtons2()
        for child in self.winfo_children():
            child.grid_configure(padx =5, pady =3)

    def makeButtons1(self):
        buttonFrame = ttk.Frame(self)
        buttonFrame.grid(column = 1, row = 8, columnspan = 2 , sticky = tk.W)
        self.hitButton = ttk.Button(buttonFrame,text = "Hit",state = tk.DISABLED,command = self.Hit)
        self.hitButton.grid(column = 0,row = 0,sticky = tk.W)
        self.standButton = ttk.Button(buttonFrame,text = "Stand",state = tk.DISABLED,command = self.Stand)
        self.standButton.grid(column = 1,row = 0,sticky = tk.W)
       

    def makeButtons2(self):
        buttonFrame = ttk.Frame(self)
        buttonFrame.grid(column = 1, row = 10, columnspan = 2 , sticky = tk.W)        
        ttk.Button(buttonFrame,text = "Play",command = self.Play).grid(column = 0,row = 0,sticky = tk.W)
        ttk.Button(buttonFrame,text = "Exit",command = self.Exit).grid(column = 1,row = 0,sticky = tk.W)
        
    def Play(self):
        try:
            self.inputBet = Decimal(self.bet.get()).quantize(Decimal("0.00"))
            if self.inputBet == 0 or self.inputBet < 0:
                self.clearFields()
                self.result.set("You must place a valid bet to play.")
            elif self.inputBet > Decimal((self.money.get()).strip('$')):
                self.clearFields()
                self.result.set("Bet cannot be more than the money you have.")
            else:
                self.result.set("")
                self.startGame()
        except ValueError:
            self.clearFields()
            self.result.set("You must place a valid bet to play.")
        except Exception:
            self.clearFields()
            self.result.set("You must place a valid bet to play.")

    def startGame(self):
        self.deck = Deck()
        self.dealerHand = Hand()
        self.dealerHand.addCard(self.deck.dealCard())
        self.dealerHand.addCard(self.deck.dealCard())
        self.dealerScore = self.dealerHand.points()
        self.dealerCards.set(self.dealerHand.getCard(0).displayCard())
        self.dealerPoints.set(self.dealerHand.getCard(0).points)
        
        self.userHand = Hand()
        self.userHand.addCard(self.deck.dealCard())
        self.userHand.addCard(self.deck.dealCard())
        self.userScore = self.userHand.points()
        self.displayUser()
        
        if self.userScore == 21:
            if self.dealerScore == 21:
                self.displayDealer()
                self.result.set("Its a draw.")           
            else:
                self.displayDealer()
                self.result.set("Hooray! You win!")
                total = Decimal((self.money.get()).strip('$'))+ Decimal("1.5")*self.inputBet
                total = total.quantize(Decimal("0.00"))
                self.money.set(lc.currency(total,grouping = True))
            
        elif self.dealerScore == 21:
            self.displayDealer()
            self.result.set("Sorry. You lose.")
            total = Decimal((self.money.get()).strip('$')) - self.inputBet
            total = total.quantize(Decimal("0.00"))
            self.money.set(lc.currency(total,grouping = True))
        else:
            self.hitButton.config(state="normal")
            self.standButton.config(state="normal")

    def displayDealer(self):
        dummy = ""
        for card in self.dealerHand:
            dummy += card.displayCard() + " "
        self.dealerCards.set(dummy)
        self.dealerScore = self.dealerHand.points()
        self.dealerPoints.set(self.dealerScore)


    def displayUser(self):
        dummy = ""
        for card in self.userHand:
            dummy += card.displayCard() + " "
        self.userCards.set(dummy)
        self.userScore = self.userHand.points()
        self.userPoints.set(self.userScore)

    def Hit(self):
        self.userHand.addCard(self.deck.dealCard())
        self.displayUser()
        self.userScore = self.userHand.points()   
        if self.userScore == 21:
            self.Stand()
            
        elif self.userScore > 21:
            self.displayDealer()
            self.result.set("Sorry. You lose.")
            total = Decimal((self.money.get()).strip('$')) - self.inputBet
            total = total.quantize(Decimal("0.00"))
            self.money.set(lc.currency(total,grouping = True))
            self.hitButton.config(state="disabled")
            self.standButton.config(state="disabled")


    def Stand(self):
        self.displayDealer()
        self.userScore = self.userHand.points()
        self.dealerScore = self.dealerHand.points()
        while self.dealerScore < 17:
            self.dealerHand.addCard(self.deck.dealCard())
            self.displayDealer()
            self.dealerScore = self.dealerHand.points()
        if self.dealerScore > 21 or self.userScore > self.dealerScore:
            self.result.set("Hooray! You win!")
            total = Decimal((self.money.get()).strip('$')) + self.inputBet
            total = total.quantize(Decimal("0.00"))
            self.money.set(lc.currency(total,grouping = True))        
        elif self.dealerScore == self.userScore:
            self.result.set("Its a draw.")
        elif self.dealerScore == 21 or self.userScore < self.dealerScore:
            self.result.set("Sorry. You lose.")
            total = Decimal((self.money.get()).strip('$')) - self.inputBet
            total = total.quantize(Decimal("0.00"))
            self.money.set(lc.currency(total,grouping = True))
        self.hitButton.config(state="disabled")
        self.standButton.config(state="disabled")
              
                       
    def Exit(self):
        self.stopMoney = Decimal((self.money.get()).strip('$')).quantize(Decimal("0.00"))
        self.stopTime = datetime.now()
        d.add_session(Session(self.sessionID,self.startTime,self.startMoney,self.stopTime,self.stopMoney))
        d.close()
        self.parent.destroy()
        sys.exit()

    
    def clearFields(self):
        self.dealerCards.set("")
        self.dealerPoints.set("")
        self.userCards.set("")
        self.userPoints.set("")

def main():
    d.connect()
    output = lc.setlocale(lc.LC_ALL, '')
    if output == 'C':
        lc.setlocale(lc.LC_ALL, 'en_US')
    root = tk.Tk()
    root.title("Blackjack")
    Blackjack(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    
    
