from random import shuffle
from time import sleep
import PySimpleGUI as sg


class Card:
    suits = ["spades",
             "hearts",
             "diamonds",
             "clubs"]

    values = [None, "1", "2", "3",
              "4", "5", "6", "7",
              "8", "9", "10",
              "jack", "queen",
              "king", "ace"]

    def __init__(self, v, s):
        """suit + value are ints"""
        self.value = v
        self.suit = s

    def __lt__(self, c2):
        if self.value < c2.value:
            return True
        if self.value == c2.value:
            if self.suit < c2.suit:
                return True
            else:
                return False
        return False

    def __gt__(self, c2):
        if self.value > c2.value:
            return True
        if self.value == c2.value:
            if self.suit > c2.suit:
                return True
            else:
                return False
        return False

    def __repr__(self):
        v = self.values[self.value] +\
            " of " + \
            self.suits[self.suit]
        return v


class Deck:
    def __init__(self):
        self.cards = []
        for i in range(2, 15):
            for j in range(4):
                self.cards\
                    .append(Card(i,
                                 j))
        shuffle(self.cards)

    def rm_card(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.wins = 0
        self.card = None
        self.name = name


class Game:
    def __init__(self):
        sg.theme('SystemDefault')

        window = sg.Window('Game setup', [
            [sg.Text("Player 1's name:"), sg.InputText()],
            [sg.Text("Player 2's name"), sg.InputText()],
            [sg.Button("Start game!"), sg.Button("Cancel") ]
        ])

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                return
            break;
    
        window.close()

        self.deck = Deck()
        self.p1 = Player(values[0])
        self.p2 = Player(values[1])

    def wins(self, winner, p1c, p2c):
        self.window['-header-'].update(value=f"{winner} wins this round!")

        if p1c > p2c:
            self.window['-name1-'].update(value=f"{self.p1.name} 👑")
        else:
            self.window['-name2-'].update(value=f"{self.p2.name} 👑")


    def reset(self):
        self.window['-card1-'].update(filename="cards/card_back_1.png")
        self.window['-card2-'].update(filename="cards/card_back_2.png")
        self.window['-header-'].update(value="WAR!")
        self.window['-action-'].update(text="Fight")
        self.window['-name1-'].update(value=f"{self.p1.name}")
        self.window['-name2-'].update(value=f"{self.p2.name}")

    def draw(self, p1n, p1c, p2n, p2c):
        d = "{} drew {}; {} drew {}".format(p1n, p1c, p2n, p2c)
        
        self.window['-card1-'].update(filename="cards/" + str(p1c).replace(" ", "_") + ".png")
        self.window['-card2-'].update(filename="cards/" + str(p2c).replace(" ", "_") + ".png")
        self.window['-header-'].update(value="GO!")
        self.window['-action-'].update(text="Next round")
        print(d)
        

    def play_game(self):
        cards = self.deck.cards


        p1ColumnLayout = [
            [ sg.Text(self.p1.name, key="-name1-", justification="center", font=('Helvetica', 20)) ],
            [ sg.Image("cards/card_back_1.png", key="-card1-") ],
        ]

        p2ColumnLayout = [
            [ sg.Text(self.p2.name, key="-name2-", justification="center", font=('Helvetica', 20)) ],
            [ sg.Image("cards/card_back_2.png", key="-card2-") ],
        ]

        gameLayout = [
            [ sg.Text('WAR!', justification='center', size=(20, 1), key='-header-', font=('Helvetica', 40)) ],
            [
                sg.Column(p1ColumnLayout, element_justification="center"),
                sg.Column(p2ColumnLayout, element_justification="center")
            ],
            [ sg.Button("Fight!", key='-action-', font=('Helvetica', 20)), sg.Button("End game", font=('Helvetica', 12), button_color="red") ]
        ]

        self.window = sg.Window('War!', gameLayout, element_justification='c')


        while len(cards) >= 2:
            while True:
                event, values = self.window.read()
                if event == sg.WIN_CLOSED or event == 'End game': # if user closes window or clicks cancel
                    # Quitting game
                    self.window.close()

                    win = self.winner(self.p1, self.p2)
                    return
                    
                break;
            
            p1c = self.deck.rm_card()
            p2c = self.deck.rm_card()
            p1n = self.p1.name
            p2n = self.p2.name
            self.draw(p1n,
                      p1c,
                      p2n,
                      p2c)
            if p1c > p2c:
                self.p1.wins += 1
                self.wins(self.p1.name, p1c, p2c)
            else:
                self.p2.wins += 1
                self.wins(self.p2.name, p1c, p2c)

            while True:
                event, values = self.window.read()
                if event == sg.WIN_CLOSED or event == 'End game': # if user closes window or clicks cancel
                    # Quitting game
                    self.window.close()

                    win = self.winner(self.p1, self.p2)
                    return
                    
                break;
            self.reset()

    def winner(self, p1, p2):
        winnerName = "It's a tie??"
        if p1.wins > p2.wins:
            winnerName = p1.name
        elif p1.wins < p2.wins:
            winnerName = p2.name


        winnerColumnLayout = [
            [ sg.Text("The winner is...", font=('Helvetica', 20), justification="center") ],
            [ sg.Text(winnerName, font=('Helvetica', 40), justification="center") ],
            [
                sg.Text(str(p1.wins), font=('Helvetica', 32), justification="center"),
                sg.Text('vs', font=('Helvetica', 16), justification="center"),
                sg.Text(str(p2.wins), font=('Helvetica', 32), justification="center")
            ],
            [ sg.Text("Thanks for playing!", font=('Helvetica', 12), justification="center") ]
        ]
            

        winnerWindow = sg.Window('Winner!', [[sg.Column(winnerColumnLayout, element_justification="center")]])

        while True:
            event, values = winnerWindow.read()
            if event == sg.WIN_CLOSED or event == 'End game': # if user closes window or clicks cancel
                # Quitting game
                winnerWindow.close()
                return
                
            break;

game = Game()
game.play_game()