#Playing Cards
from random import randrange

class Card:
    NUM_OF_SUITS = 4
    CARDS_PER_SUIT = 13
    NUM_OF_CARDS = NUM_OF_SUITS * CARDS_PER_SUIT
    PLACE_HOLDER_CARD = -1
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    SUITS = ['HEARTS','CLUBS','DIAMONDS','SPADES']
    def __init__(self,  suit,  rank, facingdown = True):
        self.Suit = suit
        self.Rank = rank
        self.FaceDown = facingdown
    def isSameSuit(self, card):
        return self.Suit == card.Suit
    def isSameColor(self, card):
        return (card.Suit%2 == self.Suit%2) #RBRB
    def flip(self):
        self.FaceDown = not self.FaceDown
    def facevalue(self):
        if self.Rank == Card.PLACE_HOLDER_CARD:
            return 'X'
        else:
            return '{0}:{1}'.format(Card.RANKS[self.Rank],Card.SUITS[self.Suit])
    def __str__(self):
        return str(self.Suit) + " " + str(self.Rank) + " " + str("FaceDown" if self.FaceDown else "FaceUp")
    def __repr__(self):
        return str(self.Suit) + " " + str(self.Rank) + " " + str("FaceDown" if self.FaceDown else "FaceUp")

  
#Solitaire Klondike
class MoveDescriptor:
    DISCARD_PILE = 0
    COLUMN_PILE = 1
    HOME_PILE = 2
    PILE_TO_STRING = {0:"discard",  1:"column",  2:"home"}
    def __init__(self, from_piletype, from_pileidx,  from_pileoffset,  to_piletype, to_pileidx):
        self.FromPileType = from_piletype
        self.FromPileIndex = from_pileidx
        self.FromPileOffset = from_pileoffset
        self.ToPileType = to_piletype
        self.ToPileIndex = to_pileidx

class Klondike:
    NUM_OF_COLUMNS = 7
    NUM_OF_HOMES = 4

    def __init__(self):
        #-------- SETUP UP THE PLAYING AREA --------
        self.Columns = []
        self.DiscardPile = []
        self.DrawPile = []
        self.Homes = []
        initdeck = []
        for s in range(0, Card.NUM_OF_SUITS):
            for r in range(0, Card.CARDS_PER_SUIT):
                initdeck.append(Card(s, r))

        def drawCard(deck):
            dis = None
            if len(deck)>0:
                cidx = randrange(len(deck))
                dis = deck.pop(cidx)
            return dis
        #Home Bases
        #Cards have to match the Ace that was placed
        #Aces can be placed in any home initially
        for h in range(0, Klondike.NUM_OF_HOMES):
            self.Homes.append([])
            self.Homes[h].append(Card(h, Card.PLACE_HOLDER_CARD, False))
    
        #Deal the Cards to the Columns
        #Card counts for the column go from 1 to 7 cards
        for c in range(0, Klondike.NUM_OF_COLUMNS):
            self.Columns.append([])
            self.Columns[c].append(Card(h, Card.PLACE_HOLDER_CARD, False))
            #print(c)
            for s in range(0, c+1):
                card = drawCard(initdeck)
                #print(" "+str(card))
                self.Columns[c].append(card)

        #Flip all of the first cards
        for col in self.Columns:
            col[-1].flip()
   
        #"Shuffle" the cards
        dis = drawCard(initdeck)
        while not dis == None:
            self.DrawPile.append(dis)
            dis = drawCard(initdeck)


    def Draw(self):
        if not len(self.DrawPile) >0:
            for dis in range(0, len(self.DiscardPile)):
                discard = self.DiscardPile.pop()
                discard.flip()
                self.DrawPile.append(discard)
        d = self.DrawPile.pop()
        d.flip()
        self.DiscardPile.append(d)
        return d

    def PerformMove(self,movedesc):
        #Get Card/Cards to move
        mCard = []
        if movedesc.FromPileType == MoveDescriptor.DISCARD_PILE:
            mCard.append(self.DiscardPile.pop())
        elif movedesc.FromPileType == MoveDescriptor.COLUMN_PILE:
            #pop off all of the cards
            for offset in range(movedesc.FromPileOffset, 0, 1):
                mCard.append(self.Columns[movedesc.FromPileIndex].pop())
            #flip a card if we revealed a card that is face down
            #greater than 1 to ignore placeholder
            if len(self.Columns[movedesc.FromPileIndex]) > 1:
                if self.Columns[movedesc.FromPileIndex][-1].FaceDown:
                    self.Columns[movedesc.FromPileIndex][-1].flip()
        elif movedesc.FromPileType == MoveDescriptor.HOME_PILE:
            mCard.append(self.Homes[movedesc.FromPileIndex].pop())
    
        if movedesc.ToPileType == MoveDescriptor.DISCARD_PILE:
            print("NotValid") 
        elif movedesc.ToPileType == MoveDescriptor.COLUMN_PILE:
            for c in range(0, len(mCard)):
                self.Columns[movedesc.ToPileIndex].append(mCard.pop())
        elif movedesc.ToPileType == MoveDescriptor.HOME_PILE:
            self.Homes[movedesc.ToPileIndex].append(mCard.pop()) #Only can be 1 card

    #Cards can only be placed on the opposite color
    #or onto the homebase if it comes sequentially
    #Kings can be placed into empty columns, no other card can
    #whole stacks can be moved if the bottom card can be played

    #Find Valid Moves
    def CheckColumnCard(self, card, column):
        #Greater than 1 to ignore placeholder card in the column
        if len(column) > 1:
            ccard = column[-1]
            #print("-" + str(ccard))
            if card.Rank == ccard.Rank-1:
                if not card.isSameColor(ccard):
                    #print(str(card) +" to " + str(ccard))
                    return True
        elif Card.RANKS[card.Rank] == 'K':
            return True
        return False

    #To Make it easier, suits have to match home
    def CheckHomeCard(self, card,  column):
        if len(column) > 0:
            ccard = column[-1]
            #print("-" + str(ccard))
            if card.Rank == ccard.Rank+1:
                if card.isSameSuit(ccard):
                    #print(str(card) +" to " + str(ccard))
                    return True
        return False

    def GetValidMovesForDiscard(self):
        ValidMoves = []
        #Check if discard card can be played 
        #print("--------Discard-------")
        if len(self.DiscardPile)>0:
            dcard = self.DiscardPile[-1]
            #print("--CARD--" + str(dcard))
            cidx =0
            for col in self.Columns:
                if self.CheckColumnCard(dcard, col):
                    #print("Move " + str(dcard) + " from discard to col " + str(cidx) + " ontop " + str(col[-1]))
                    ValidMoves.append(MoveDescriptor(MoveDescriptor.DISCARD_PILE, 0, -1, MoveDescriptor.COLUMN_PILE,  cidx))
                cidx = cidx + 1
            cidx = 0
            for home in self.Homes:
                if self.CheckHomeCard(dcard, home):
                    #print("Move " + str(dcard) + " from discard to home " + str(cidx) + " ontop " + str(home[-1]))
                    ValidMoves.append(MoveDescriptor(MoveDescriptor.DISCARD_PILE, 0, -1, MoveDescriptor.HOME_PILE,  cidx))
                cidx = cidx + 1
        return ValidMoves

    #It is not enough to just check the top card of each column
    #Have to check all of the face up cards to see if the stack
    #Can be moved
    def GetValidMovesForColumns(self):
        ValidMoves = []
        #print("--------Columns-------")
        idx=0
        for col in self.Columns:
            #print("COLUMN " + str(idx))
            if len(col)>1:
                #Using List like Stack going down in reverse
                for cidx in range(-1, -(len(col)), -1):
                    ccard = col[cidx]
                    if not ccard.FaceDown:
                        #print("--CARD--" + str(ccard))
                        #Check the top card of all other stacks
                        c2idx = 0
                        for col2 in self.Columns:
                            if not col == col2:
                                if self.CheckColumnCard(ccard, col2):
                                    #print("Move " + str(ccard) + " from " + str(idx) + " to col " + str(c2idx) + " ontop " + str(col2[-1]))
                                    ValidMoves.append(MoveDescriptor(MoveDescriptor.COLUMN_PILE, idx, cidx, MoveDescriptor.COLUMN_PILE,  c2idx))
                            c2idx = c2idx + 1
                        if cidx == -1: #Only Valid for Top card of column, can't move whole stack to home
                            hidx = 0
                            for home in self.Homes:
                                if self.CheckHomeCard(ccard, home):
                                    #print("Move " + str(ccard) + " from " + str(idx) + " to home " + str(hidx) + " ontop " + str(home[-1]))
                                    ValidMoves.append(MoveDescriptor(MoveDescriptor.COLUMN_PILE, idx, cidx, MoveDescriptor.HOME_PILE,  hidx))
                                hidx = hidx + 1
                    else:
                        break #Break the Loop once we reach facedown card
            idx = idx + 1
        return ValidMoves

    def GetValidMovesForHome(self):
        ValidMoves = []
        #Can move back from home
        #print("-------Home-------")
        idx=0
        for home in self.Homes:
            #home has placed holder card
            if len(home)>1:
                ccard = home[-1]
                #print("--CARD--" + str(ccard))
                #Check the top card of all other stacks
                c2idx = 0
                for col2 in self.Columns:
                    if self.CheckColumnCard(ccard, col2):
                        #print("Move " + str(ccard) + " from home " + str(idx) + " to col " + str(c2idx) + " ontop " + str(col2[-1]))
                        ValidMoves.append(MoveDescriptor(MoveDescriptor.HOME_PILE, idx, -1, MoveDescriptor.COLUMN_PILE,  c2idx))
                    c2idx = c2idx + 1
            idx = idx + 1
        return ValidMoves

    def PrettyPrintMoveDescriptor(self,move):
        fcard = ''
        if move.FromPileType == MoveDescriptor.COLUMN_PILE:
            fcard = self.Columns[move.FromPileIndex][move.FromPileOffset].facevalue()
        elif move.FromPileType == MoveDescriptor.DISCARD_PILE:
            fcard = self.DiscardPile[move.FromPileOffset].facevalue()
        elif move.FromPileType == MoveDescriptor.HOME_PILE:
            fcard = self.Homes[move.FromPileIndex][move.FromPileOffset].facevalue()

        tcard = ''
        if move.ToPileType == MoveDescriptor.COLUMN_PILE:
            tcard = self.Columns[move.ToPileIndex][-1].facevalue()
        elif move.ToPileType == MoveDescriptor.HOME_PILE:
            tcard = self.Homes[move.ToPileIndex][-1].facevalue()

        strf = 'From: {0} card {1} -- To: {2} card {3}'.format(
            MoveDescriptor.PILE_TO_STRING[move.FromPileType], 
            fcard, 
            MoveDescriptor.PILE_TO_STRING[move.ToPileType], 
            tcard)
        return strf


    def PrettyPrintCards(self):
        discard = self.DiscardPile[-1].facevalue() if len(self.DiscardPile) > 0 else 'X'
        toprow = 'DRAW_PILE_COUNT[{0}]: DISCARD_CARD [{1}]       HOMES [{2}] [{3}] [{4}] [{5}]\n'.format(
           str(len(self.DrawPile)),
           discard,
           self.Homes[0][-1].facevalue(),
           self.Homes[1][-1].facevalue(),
           self.Homes[2][-1].facevalue(),
           self.Homes[3][-1].facevalue())

        maxcollength = 0
        for c in self.Columns:
            if len(c) > maxcollength:
                maxcollength = len(c)
        
        rowstring = ''
        #Skip Dummy card
        for idx in range(1,maxcollength):
            crow = ''
            for c in self.Columns:
                if idx < len(c):
                    card = c[idx]
                    if card.FaceDown:
                        crow = crow + '[D]'.ljust(12,' ')
                    else:
                        crow = crow + c[idx].facevalue().ljust(12,' ')
                else:
                    crow = crow + ' '*12
            rowstring = rowstring + crow + '\n'

        cardmat = toprow + '\n\n' + rowstring

        return cardmat