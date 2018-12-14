'''
A simplified version of blackjack for 1 player
'''

import random
import time
from os import system

card_suits = {'club':'♣', 'heart':'♥', 'spade':'♠', 'diamond':'♦'}

# Classes

class Card():
    '''
    Class determines card with all necessary attributes
    '''
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.symbol = card_suits[self.suit]
        self.closed = False

        if suit in ('club', 'spade'):
            self.color = "\033[30;47m"
        else:
            self.color = "\033[31;47m"
        self.resetcolor = "\033[0;0m"

        self.view = [f"\033[30;47m{self.rank: <5}{self.resetcolor}",
                     f"{self.color}{self.symbol: ^5}{self.resetcolor}",
                     f"\033[30;47m{self.rank: >5}{self.resetcolor}"]

    def print_card(self):
        '''
        Prints the whole card (3 rows, 5 cols)
        '''
        for line in self.view:
            print(line)

    def __str__(self):
        return self.rank + self.symbol

class Deck():
    '''
    Class for blackjack deck that includes 52 cards
    It creates and stores this card in the list
    '''

    def __init__(self):

        self.deck = []
        self.card_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

        for card_no in range(0, 52):
            self.deck.append(Card(list(card_suits.keys())[card_no % 4],
                                  self.card_ranks[card_no % 13]))

        self.shuffle()
        #hello, my name is Igor :)
    def print(self):
        '''
        Prints a list of pairs 'suit + rank'
        '''
        print([str(card) for card in self.deck])

    def shuffle(self):
        '''
        Shuffles all cards in the deck
        '''
        random.shuffle(self.deck)

class Person():
    '''
    Parent class for any player incl. dealer
    '''
    def __init__(self):
        self.deck = []
        self.points = []

    def take_card(self, card):
        '''
        Adds a new card to the player's deck
        '''
        self.deck.append(card)

    def print_deck(self):
        '''
        Prints all player's cards in a row
        '''
        for line in range(0, 3):
            for card in self.deck:
                if card.closed:
                    print("\033[30;47m◊◊◊◊◊\033[0;0m", end=' ')
                else:
                    print(card.view[line], end=' ')
            print('')

    def count(self):
        '''
        Counts all open cards and writes all possible sums into the list
        '''
        self.points.clear()

        not_ace_points = 0
        for card in self.deck:
            if card.rank == 'A' or card.closed:
                continue
            if card.rank.isdigit():
                not_ace_points += int(card.rank)
            else:
                not_ace_points += 10

        aces = len([ace for ace in self.deck if ace.rank == 'A' and not ace.closed])
        print(f"aces = {aces}")
        for var in range(0, aces + 1):
            self.points.append(aces + 10 * var + not_ace_points)

class Player(Person):
    '''
    Class for human player
    '''
    def __init__(self, name='Player', deposit=500):
        Person.__init__(self)
        self.money = deposit
        self.name = name

    def add_money(self, deposit):
        '''
        Adds money after player wins
        '''
        self.money += deposit

    def bet(self, bet_amount):
        '''
        Makes substraction after successful bet
        '''
        self.money -= bet_amount

class Table():
    '''
    Class for storing all required game data
    '''
    def __init__(self, player_, dealer_):
        self.player = player_
        self.dealer = dealer_
        self.bet = 0
        self.coef = 1.0
        self.log = []

    def print(self):
        '''
        Prints players' cards as well as available money and last action
        '''
        system('clear')
        print(f"{self.player.name}'s funds: \033[0;32m${self.player.money}\n\033[0;0m")
        print("Current win coefficient: \033[0;33m{0:.1f}\033[0;0m".format(self.coef))
        print(f"Current bet: \033[0;33m${self.bet}\033[0;0m")
        print(f"\n\033[0;32m{self.player.name}'s cards {self.player.points}\033[0;0m")
        self.player.print_deck()
        print(f"\n\033[0;31mDealer's cards {self.dealer.points}\033[0;0m")
        self.dealer.print_deck()
        print("\n\033[0;33mLast actions:\033[0;0m")
        print(self.log[-3])
        print(self.log[-2])
        print(self.log[-1], end='\n\n')

    def count(self):
        '''
        Starts both players' count methods
        '''
        self.player.count()
        self.dealer.count()

    def addlog(self, log_string):
        '''
        Concats timestamp with new log entry and adds it to the log list
        '''
        self.log.append(time.strftime("[%H:%M:%S] ", time.gmtime()) + log_string)

    def player_wins(self, win_msg):
        '''
        Gives money to player, prints messages and adds new log entry
        '''
        print("\033[0;32m" + win_msg + f" You win ${self.bet * self.coef}!\033[0;0m\n")
        self.player.add_money(self.bet * (self.coef + 1))
        self.addlog(f"{self.player.name} won ${self.bet * self.coef}")

# Functions
def get_answer(request):
    '''
    Asks player for input (1 or 2) and return it
    '''
    answer = ''
    while True:
        answer = input(request)
        if answer not in ['1', '2']:
            print("\033[0;31mWrong option. Please type just '1' or '2'\033[0;0m")
        else:
            return int(answer)

# Game

# Creating starting variable for the game
game_deck = Deck()
dealer = Person()
player = Player(deposit=500)
game_on = 'start'
table = Table(player, dealer)
table.addlog("Game starts")

# Setting up player's name
system('clear')
while True:
    player.name = input("Please enter your name: ").strip()
    if not player.name:
        print("Name should contain at least 1 letter")
    else:
        break

while game_on != 'finish':
    system('clear')
    bet = 0

    # Asking for player's bet
    while True:
        try:
            bet = int(input(f"Your current account is ${player.money}. " +
                            "Please make your bet (min. $50): "))
        except ValueError:
            print("An error occured. Please try again")
            continue
        else:
            if bet < 50:
                print("Bet must be at least $50")
                continue
            elif bet > player.money:
                print("You have no such amount of money. Please lower your bet")
                continue
            else:
                player.bet(bet)
                table.bet = bet
                table.addlog(f"{player.name} makes ${bet} bet")
                break

    # Giving cards for both player and dealer (hiding dealer's 2nd card)
    if game_on == 'start':
        table.coef = 1
        player.take_card(game_deck.deck.pop())
        player.take_card(game_deck.deck.pop())
        dealer.take_card(game_deck.deck.pop())
        dealer.take_card(game_deck.deck.pop())
        dealer.deck[1].closed = True
        table.addlog("Players get their cards")
        table.count()
        table.print()
        game_on = 'player'

    # Player's turn
    if game_on == 'player':
        while True:
            # Checking player's points
            if len(player.deck) > 2:
                if 21 in player.points:
                    table.addlog(f"{player.name} has got 21 points. Dealer's turn")
                    game_on = 'dealer'
                    table.print()
                    break
                elif min(player.points) > 21:
                    table.addlog(f"BUSTED! {player.name} loses his bet: ${table.bet}")
                    game_on = 'replay'
                    table.print()
                    print(f"\033[0;31mBUSTED! You lose your bet: ${table.bet}\n\033[0;0m")
                    break

            # Giving a choice to player
            if len(player.deck) == 2 and player.deck[0] == player.deck[1] == 'A':
                table.coef = 1.5
                table.player_wins("It's a Golden Point!")
                game_on = 'replay'
                break
            elif len(player.deck) == 2 and 21 in player.points:
                table.coef = 1.5
                if 10 in dealer.points or 11 in dealer.points:
                    if get_answer("You have Blackjack but dealer also can have it." +
                                  "Take your win 1:1 (1) or stay to have a chance to get 1.5:1 (2): ") == 1:
                        table.coef = 1.0
                        table.player_wins("It's Blackjack!")
                        game_on = 'replay'
                        break
                    else:
                        table.addlog(f"{player.name} has a BJ but waits for dealer")
                        game_on = 'dealer'
                        break
                else:
                    table.player_wins("It's Blackjack!")
                    game_on = 'replay'
                    break
            else:
                if get_answer("Please choose your action: Take another card (1) or stay (2): ") == 1:
                    player.take_card(game_deck.deck.pop())
                    table.count()
                    table.addlog(f"{player.name} takes another card: {player.deck[-1]}")
                    table.print()
                    continue
                else:
                    game_on = 'dealer'
                    table.addlog(f"{player.name} chooses to stay")
                    break

    # Dealer's turn
    if game_on == 'dealer':
        while True:
        # Checking dealer's points
            if len(dealer.deck) == 2 and dealer.deck[0] == dealer.deck[1] == 'A' and dealer.deck[1].closed == False:
                table.addlog(f"Dealer has Golden point and {player.name} loses his bet: ${table.bet}")
                game_on = 'replay'
                table.print()
                print(f"\033[0;31mDealer has Golden point and you lose your bet: ${table.bet}\n\033[0;0m")
                break

            if min(dealer.points) > 21:
                table.player_wins("BUSTED! Dealer exceeds 21!")
                game_on = 'replay'
                break

            player_max = max([point for point in player.points if point < 22])
            dealer_max = max([point for point in dealer.points if point < 22])
            if dealer_max >= 17:
                if player_max == dealer_max:
                    player.add_money(table.bet)
                    table.addlog(f"Draw. Players return their bets")
                    game_on = 'replay'
                    table.print()
                    print(f"\033[0;33mDraw!\033[0;0m\n")
                    break
                elif player_max > dealer_max:
                    table.player_wins(f"Your cards are better!")
                    game_on = 'replay'
                    break
                elif player_max < dealer_max:
                    table.addlog(f"{player.name} has less points and loses his bet: ${table.bet}")
                    game_on = 'replay'
                    table.print()
                    print(f"\033[0;31mYou have less points and lose your bet: ${table.bet}\n\033[0;0m")
                    break

        # Dealer's card processing
            if dealer.deck[1].closed == True:
                time.sleep(1)
                dealer.deck[1].closed = False
                table.addlog(f"Dealer opens his card and it's {dealer.deck[-1]}")
                table.count()
                table.print()
                continue
            else:
                time.sleep(1)
                dealer.take_card(game_deck.deck.pop())
                table.count()
                table.addlog(f"Dealer takes card and it's {dealer.deck[-1]}")
                table.print()

    if game_on == 'replay':
        if player.money < 50:
            print("\nYou lose all your money and can't make another bet. The game is over\n")
            break
        else:
            if get_answer("Would you like to try again (1) or finish the game (2)? ") == 1:
                dealer.deck[1].closed = False
                game_deck.deck = game_deck.deck + player.deck + dealer.deck
                player.deck.clear()
                dealer.deck.clear()
                game_deck.shuffle()
                game_on = 'start'
                table.addlog(f"{player.name} starts a new round")
                continue
            else:
                print("\nThanks for the game! Bye!\n")
                break

    break


#max.take_card(game_deck.deck.pop())
#max.deck[1].closed = True
#max.print_deck()
#max.count()
#print(max.points)
