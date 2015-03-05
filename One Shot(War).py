#One shot
#For 2-8 Players
import cards, games
class One_Shot_Card(cards.Card):
    """A One Shot Card"""
    @property
    def value(self):
        if self.is_face_up:
            v=One_Shot_Card.RANKS.index(self.rank)+1
            return v
        else:
            return None


class One_Shot_Deck(cards.Deck):
    """A One Shot Deck"""
    def populate(self):
        for suit in One_Shot_Card.SUITS:
            for rank in One_Shot_Card.RANKS:
                self.cards.append(One_Shot_Card(rank,suit))
class One_Shot_Hand(cards.Hand):
    """A One Shot Deck"""
    def __init__(self, name):
        super(One_Shot_Hand, self).__init__()
        self.name=name

    def __str__(self):
        rep = self.name+":\t" + super(One_Shot_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total)+ ")"
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
        return t
class One_Shot_Player(One_Shot_Hand):
    """A One Shot Player"""
    def lose(self):
        print(self.name, "loses.")
    def win(self):
        print(self.name, "wins.")
    def tie(self):
        print(self.name, "ties.")

        
class One_Shot_Game(object):
    """A One Shot Game."""
    def __init__(self, names):
        self.players = []
        for name in names:
            player = One_Shot_Player(name)
            self.players.append(player)
        self.deck=One_Shot_Deck()
        self.deck.populate()
        self.deck.shuffle()




    def play(self):
        #deal one card to everyone
        self.deck.deal(self.players, per_hand = 1)
        for player in self.players:
            print(player)

        # compare each player's cards
        if self.players[0].cards[0].value > self.players[1].cards[0].value:
            self.players[1].lose()
            self.players[0].win()
        elif self.players[0].cards[0].value < self.players[1].cards[0].value:
            self.players[0].lose()
            self.players[1].win()
        else:
            self.players[0].tie()
            self.players[1].tie()

        # restart game
        for player in self.players:
            player.clear()
        self.deck = One_Shot_Deck()
        self.deck.populate()
        self.deck.shuffle()


def main():
    print("\t\tWelcome to One Shot!\n")
    names = []
    number = 2
    for i in range(number):
        name = input("Enter player name: ")
        names.append(name)
    print()

    game = One_Shot_Game(names)
    again = None
    while again != 'n':
        game.play()
        again = games.ask_yes_no("\nDo you want to play again?: ")
main()
input("\n\nPress the enter key to exit.")
