import tkinter as tk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import random
from math import floor
from models import CardMap


class Hand():
    def __init__(self) -> None:
        self.hand = []

    def getCard(self, index: int):
        return self.hand[index]

    def numCards(self):
        return len(self.hand)

    def drawCard(self, card: int):
        if len(self.hand) < 5:
            self.hand.append(card)
        else:
            raise Exception('Tried to draw more than 5 cards!')

    def returnCard(self) -> int:
        if len(self.hand) > 0:
            card = self.hand.pop()
            return card
        else:
            showinfo(
                '', 'The deck is already full, try drawing some cards!')

    def emptyHand(self):
        self.hand.clear()


class Deck():
    def __init__(self) -> None:
        self.cardStack = list(range(0, 52))

    def getCard(self, index: int):
        return self.cardStack[index]

    def numCards(self):
        return len(self.cardStack)

    def shuffle(self) -> bool:
        if len(self.cardStack) == 52:
            random.shuffle(self.cardStack)
            return True
        return False

    def drawCard(self) -> int:
        if len(self.cardStack) > 47:
            card = self.cardStack.pop()
            return card
        else:
            showinfo(
                '', 'You have already drawn your hand, please hit return before drawing again')

    def returnCard(self, card: int):
        if len(self.cardStack) < 52:
            self.cardStack.append(card)
        else:
            raise Exception('Tried to return card when deck is full!')


class Table():
    def __init__(self, window: tk.Tk) -> None:
        self.deck = Deck()
        self.hand = Hand()
        self.window = window

    def numDeckCards(self) -> int:
        return self.deck.numCards()

    def numHandCards(self) -> int:
        return self.hand.numCards()

    def getDeckCard(self, index: int) -> int:
        if index < self.deck.numCards():
            return self.deck.getCard(index)
        else:
            raise Exception(
                f'Cant access card at index {index}, out of range. Deck only has {self.deck.numCards()} cards.')

    def getHandCard(self, index: int) -> int:
        if index < self.hand.numCards():
            return self.hand.getCard(index)
        else:
            raise Exception(
                f'Cant access card at index {index}, out of range. Hand only has {self.hand.numCards()} cards.')

    def shuffleDeck(self) -> str:
        return self.deck.shuffle()

    def drawHand(self):
        for i in range(0, 5):
            card = self.deck.drawCard()
            self.hand.drawCard(card)

    def returnHand(self):
        for i in range(0, 5):
            card = self.hand.returnCard()
            self.deck.returnCard(card)


class Button(tk.Button):
    def __init__(self, window: tk.Tk, text: str, command):
        super().__init__(window, text=text)
        self['command'] = command


class CardImage(ImageTk.PhotoImage):
    def __init__(self, imageFileName: str, width: int, height: int):
        super().__init__(Image.open(imageFileName).resize((width, height)))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.deckCardImages: list[CardImage] = []
        self.handCardImages: list[CardImage] = []
        self.table = Table(self)

        # set window properties
        self.title('Playing Cards')
        self.geometry('1000x800')
        self.columnconfigure(
            list(range(0, 13)), weight=1)
        self.rowconfigure(list(range(0, 8)), weight=1)

        # setup frames
        self.fr_available_cards = tk.Frame(self, bg='red')
        self.fr_available_cards.grid(
            row=0, column=0, rowspan=1, columnspan=13, sticky='nsew',
        )
        self.fr_user_hand = tk.Frame(self, bg='blue')
        self.fr_user_hand.grid(
            row=1, column=0, rowspan=7, columnspan=10, sticky='nsew',
        )
        self.fr_buttons = tk.Frame(self, bg='green')
        self.fr_buttons.grid(
            row=1, column=10, rowspan=7, columnspan=3, sticky='nsew',
        )

        # initialize deck
        self.buildDeck()

        # create shuffle button
        self.btn_shuffle = Button(self, 'Shuffle', self.shuffle_clicked)
        self.btn_shuffle.grid(row=4, column=11, rowspan=1,
                              columnspan=1, sticky='nsew', padx=10, pady=10)

        # create draw button
        self.btn_draw = Button(self, 'Draw', self.draw_clicked)
        self.btn_draw.grid(row=5, column=11, rowspan=1,
                           columnspan=1, sticky='nsew', padx=10, pady=10)

        # create return button
        self.btn_return = Button(self, 'Return', self.return_clicked)
        self.btn_return.grid(row=6, column=11, rowspan=1,
                             columnspan=1, sticky='nsew', padx=10, pady=10)

    def shuffle_clicked(self):
        deckShuffled = self.table.shuffleDeck()
        if deckShuffled:
            self.buildDeck()
        else:
            showinfo('', 'Please return your hand before shuffling')

    def draw_clicked(self):
        self.table.drawHand()
        self.buildDeck()
        self.buildHand()

    def return_clicked(self):
        self.table.returnHand()
        self.buildDeck()
        self.buildHand()

    def buildDeck(self):
        self.deckCardImages.clear()
        numDeckCards = self.table.numDeckCards()

        # build image stack for the deck
        for i in range(0, numDeckCards):
            cardIndex = self.table.getDeckCard(i)
            fileName = CardMap.getCardFileName(cardIndex)
            self.deckCardImages.append(CardImage(fileName, 50, 80))

        # create deck layout
        for i in range(0, numDeckCards):
            column_number = i % 13
            row_number = floor(i / 13)
            lbl_image = tk.Label(
                self.fr_available_cards, image=self.deckCardImages[i], width=50, height=80)
            lbl_image.grid(row=row_number, column=column_number, rowspan=1,
                           columnspan=1, sticky='nsew', padx=10, pady=10)

    def buildHand(self):
        self.handCardImages.clear()
        numHandCards = self.table.numHandCards()

        # build image stack for the hand
        for i in range(0, numHandCards):
            cardIndex = self.table.getHandCard(i)
            fileName = CardMap.getCardFileName(cardIndex)
            self.handCardImages.append(CardImage(fileName, 120, 200))

        # create hand layout
        for i in range(0, numHandCards):
            lbl_image = tk.Label(
                self.fr_user_hand, image=self.handCardImages[i], width=120, height=200)
            lbl_image.grid(row=7, column=i, rowspan=1,
                           columnspan=1, sticky='nsew', padx=10, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
