# Blackjack
# From 1 to 7 players compete against a dealer

import cards, games     

class BJ_Card(cards.Card):
    """ A Blackjack Card. """
    ACE_VALUE = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v

class BJ_Deck(cards.Deck):
    """ A Blackjack Deck. """
    def populate(self):
        for suit in BJ_Card.SUITS: 
            for rank in BJ_Card.RANKS: 
                self.cards.append(BJ_Card(rank, suit))
      

class BJ_Hand(cards.Hand):
    """ A Blackjack Hand. """
    def __init__(self, name):
        super(BJ_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()  
        if self.total:
            rep += "(" + str(self.total) + ")"        
        return rep

    @property     
    def total(self):
        # if a card in the hand has value of None, then total is None
        for card in self.cards:
            if not card.value:
                return None
        
        # add up card values, treat each Ace as 1
        t = 0
        for card in self.cards:
              t += card.value

        # determine if hand contains an Ace
        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True
                
        # if hand contains Ace and total is low enough, treat Ace as 11
        if contains_ace and t <= 11:
            # add only 10 since we've already added 1 for the Ace
            t += 10   
                
        return t

    def is_busted(self):
        return self.total > 21



class Bet(object):
    """ A Blackjack Gamble. """
    # Values
    def __init__(bet, money = 10):
        bankroll  = money

    # Betting options
    def betting(bet,bankroll):
        try:
            if bankroll>  0:
                wager = int(input("\nHow much do you want to wager?: "))
                if wager >  bankroll:
                    int(input("\n You can only wager "+ str(bankroll)+" or less. How much?: "))
                elif wager <  0:
                    int(input("\n You can only wager a positive number. How much?: "))
        except ValueError:
           int(input("\n That's not valid! Choose a number: "))
        return wager
    # Money Conditions
    def gamble(bet):
        if bet.bankroll<= 0:
            print("\nYou are out of money! You're out of the game!")


class BJ_Player(BJ_Hand):
    """ A Blackjack Player. """
    def __init__(self, name,bankroll,playerbet):
        super(BJ_Player, self).__init__(name)
        self.bankroll=bankroll
        self.wager=playerbet

    def is_hitting(self):
        if self.total == 21:
            response = "n"

        else:
            response = games.ask_yes_no("\n" + self.name + ", do you want a hit? (Y/N): ")
        return response == "y"

    def bust(self,wager):
        print(self.name, "busts.")
        self.lose(self.wager)
    def lose(self, wager):
        print(self.name, "loses.")
        self.bankroll=self.bankroll - self.wager
        print("Your bankroll is: ",self.bankroll)
        return self.bankroll

    def win(self, wager):
        print(self.name, "wins.")
        self.bankroll=self.bankroll+self.wager
        print("Your bankroll is: ",self.bankroll)
        return self.bankroll

    def push(self):
        print(self.name, "pushes.")

class BJ_Dealer(BJ_Hand):
    """ A Blackjack Dealer. """
    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "busts.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game(object):
    """ A Blackjack Game. """
    def __init__(self, names):      
        self.players = []
        for name in names:
            bankroll=100
            playerbet=Bet(bankroll).betting(bankroll)
            player = BJ_Player(name,bankroll,playerbet)
            
            self.players.append(player)
        self.dealer = BJ_Dealer("Dealer")

        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()


    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self,player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust(self)
    def __player_broke(self):
        if player is not broke and player.cash <=0:
            player.broke
    def play(self, wager):
        # deal initial 2 cards to everyone
        self.deck.deal(self.players + [self.dealer], per_hand = 2)
        self.dealer.flip_first_card()    # hide dealer's first card
        for player in self.players:
            print(player)
        print(self.dealer)

        # deal additional cards to players
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()    # reveal dealer's first 

        if not self.still_playing:
            # since all players have busted, just show the dealer's hand
            print(self.dealer)
        else:
            # deal additional cards to dealer
            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # everyone still playing wins
                for player in self.still_playing:
                    player.win(wager)                    
            else:
                # compare each player still playing to dealer
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win(wager)
                    elif player.total < self.dealer.total:
                        player.lose(wager)
                    else:
                        player.push()

        # remove everyone's cards
        for player in self.players:
            player.clear()
        self.dealer.clear()
        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

def main():
    print("\t\tWelcome to Blackjack!\n")
    bankroll=0
    wager=0
    names = []
    number = games.ask_number("How many players? (1 - 7): ", low = 1, high = 8)
    for i in range(number):
        name = input("Enter player name: ")
        names.append(name)
    print()
        
    game = BJ_Game(names)

    again = None
    while again != "n":
        game.play(wager)
        again = games.ask_yes_no("\nDo you want to play again?: ")
          
main()
input("\n\nPress the enter key to exit.")



