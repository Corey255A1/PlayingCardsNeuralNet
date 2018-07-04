#Playing Cards
from random import randrange
NUM_OF_SUITS = 4
CARDS_PER_SUIT = 13
NUM_OF_CARDS = NUM_OF_SUITS * CARDS_PER_SUIT
PLACE_HOLDER_CARD = -1
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
class Card:
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
    def __str__(self):
        return str(self.Suit) + " " + str(self.Rank) + " " + str("FaceDown" if self.FaceDown else "FaceUp")
    def __repr__(self):
        return str(self.Suit) + " " + str(self.Rank) + " " + str("FaceDown" if self.FaceDown else "FaceUp")

Deck = []
for s in range(0, NUM_OF_SUITS):
    for r in range(0, CARDS_PER_SUIT):
        Deck.append(Card(s, r))
        
def DrawCard(deck):
    if len(deck)>0:
        cidx = randrange(len(deck))
        return deck.pop(cidx)
    else:
        return None
    
    

#Solitaire Klondike
NUM_OF_COLUMNS = 7
NUM_OF_HOMES = 4
Columns = []
DiscardPile = []
DrawPile = []
Homes = []

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

def Draw():
    if not len(DrawPile) >0:
        for dis in range(0, len(DiscardPile)):
            discard = DiscardPile.pop()
            discard.flip()
            DrawPile.append(discard)
    d = DrawPile.pop()
    d.flip()
    DiscardPile.append(d)
    return d

def PerformMove(movedesc):
    #Get Card/Cards to move
    mCard = []
    if movedesc.FromPileType == MoveDescriptor.DISCARD_PILE:
        mCard.append(DiscardPile.pop())
    elif movedesc.FromPileType == MoveDescriptor.COLUMN_PILE:
        #pop off all of the cards
        for offset in range(movedesc.FromPileOffset, 0, 1):
            mCard.append(Columns[movedesc.FromPileIndex].pop())
        #flip a card if we revealed a card that is face down
        #greater than 1 to ignore placeholder
        if len(Columns[movedesc.FromPileIndex]) > 1:
            if Columns[movedesc.FromPileIndex][-1].FaceDown:
                Columns[movedesc.FromPileIndex][-1].flip()
    elif movedesc.FromPileType == MoveDescriptor.HOME_PILE:
        mCard.append(Homes[movedesc.FromPileIndex].pop())
    
    if movedesc.ToPileType == MoveDescriptor.DISCARD_PILE:
        print("NotValid") 
    elif movedesc.ToPileType == MoveDescriptor.COLUMN_PILE:
        for c in range(0, len(mCard)):
            Columns[movedesc.ToPileIndex].append(mCard.pop())
    elif movedesc.ToPileType == MoveDescriptor.HOME_PILE:
        Homes[movedesc.ToPileIndex].append(mCard.pop()) #Only can be 1 card
        

#Home Bases
#Cards have to match the Ace that was placed
#Aces can be placed in any home initially
for h in range(0, NUM_OF_HOMES):
    Homes.append([])
    Homes[h].append(Card(h, PLACE_HOLDER_CARD, False))
    
#Deal the Cards to the Columns
#Card counts for the column go from 1 to 7 cards
for c in range(0, NUM_OF_COLUMNS):
    Columns.append([])
    Columns[c].append(Card(h, PLACE_HOLDER_CARD, False))
    #print(c)
    for s in range(0, c+1):
        card = DrawCard(Deck)
        #print(" "+str(card))
        Columns[c].append(card)

#Flip all of the first cards
for col in Columns:
    col[-1].flip()
    
dis = DrawCard(Deck)
while not dis == None:
    DrawPile.append(dis)
    dis = DrawCard(Deck)
    
#Discard one for now.. 
Draw()


#Cards can only be placed on the opposite color
#or onto the homebase if it comes sequentially
#Kings can be placed into empty columns, no other card can
#whole stacks can be moved if the bottom card can be played

#Find Valid Moves
def CheckColumnCard(card,  column):
    #Greater than 1 to ignore placeholder card in the column
    if len(column) > 1:
        ccard = column[-1]
        #print("-" + str(ccard))
        if card.Rank == ccard.Rank-1:
            if not card.isSameColor(ccard):
                #print(str(card) +" to " + str(ccard))
                return True
    elif RANKS[card.Rank] == 'K':
        return True
    return False

#To Make it easier, suits have to match home
def CheckHomeCard(card,  column):
    if len(column) > 0:
        ccard = column[-1]
        #print("-" + str(ccard))
        if card.Rank == ccard.Rank+1:
            if card.isSameSuit(ccard):
                #print(str(card) +" to " + str(ccard))
                return True
    return False

loopstop = 10
while loopstop>0:
    loopstop = loopstop - 1
    ValidMoves = []
    #Check if discard card can be played 
    print("--------Discard-------")
    if len(DiscardPile)>0:
        dcard = DiscardPile[-1]
        print("CARD--" + str(dcard))
        cidx =0
        for col in Columns:
            #print("C " + str(CheckColumnCard(dcard, col)))
            if CheckColumnCard(dcard, col):
                print("Move " + str(dcard) + " from discard to col " + str(cidx) + " ontop " + str(col[-1]))
                ValidMoves.append(MoveDescriptor(MoveDescriptor.DISCARD_PILE, 0, -1, MoveDescriptor.COLUMN_PILE,  cidx))
            cidx = cidx + 1
        cidx = 0
        for home in Homes:
            if CheckHomeCard(dcard, home):
                print("Move " + str(dcard) + " from discard to home " + str(cidx) + " ontop " + str(home[-1]))
                ValidMoves.append(MoveDescriptor(MoveDescriptor.DISCARD_PILE, 0, -1, MoveDescriptor.HOME_PILE,  cidx))
            cidx = cidx + 1
            #print("H " + str(CheckHomeCard(dcard, home)))

    #It is not enough to just check the top card of each column
    #Have to check all of the face up cards to see if the stack
    #Can be moved
    print("--------Columns-------")
    idx=0
    for col in Columns:
        print("COLUMN " + str(idx))
        if len(col)>1:
            #Using List like Stack going down in reverse
            for cidx in range(-1, -(len(col)), -1):
                ccard = col[cidx]
                if not ccard.FaceDown:
                    print("CARD--" + str(ccard))
                    #Check the top card of all other stacks
                    c2idx = 0
                    for col2 in Columns:
                        if not col == col2:
                            #print("C " + str(CheckColumnCard(ccard, col2)))
                            if CheckColumnCard(ccard, col2):
                                print("Move " + str(ccard) + " from " + str(idx) + " to col " + str(c2idx) + " ontop " + str(col2[-1]))
                                ValidMoves.append(MoveDescriptor(MoveDescriptor.COLUMN_PILE, idx, cidx, MoveDescriptor.COLUMN_PILE,  c2idx))
                        c2idx = c2idx + 1
                    if cidx == -1: #Only Valid for Top card of column, can't move whole stack to home
                        hidx = 0
                        for home in Homes:
                            #print("H " + str(CheckHomeCard(ccard, home)))
                            if CheckHomeCard(ccard, home):
                                print("Move " + str(ccard) + " from " + str(idx) + " to home " + str(hidx) + " ontop " + str(home[-1]))
                                ValidMoves.append(MoveDescriptor(MoveDescriptor.COLUMN_PILE, idx, cidx, MoveDescriptor.HOME_PILE,  hidx))
                            hidx = hidx + 1
                else:
                    break #Break the Loop once we reach facedown card
        idx = idx + 1

    #Can move back from home
    print("-------Home-------")
    idx=0
    for home in Homes:
        #home has placed holder card
        if len(home)>1:
            ccard = home[-1]
            print("CARD--" + str(ccard))
            #Check the top card of all other stacks
            c2idx = 0
            for col2 in Columns:
                #print("C " + str(CheckColumnCard(ccard, col2)))
                if CheckColumnCard(ccard, col2):
                    print("Move " + str(ccard) + " from home " + str(idx) + " to col " + str(c2idx) + " ontop " + str(col2[-1]))
                    ValidMoves.append(MoveDescriptor(MoveDescriptor.HOME_PILE, idx, -1, MoveDescriptor.COLUMN_PILE,  c2idx))
                c2idx = c2idx + 1
        idx = idx + 1
        
    print("---------Valid Moves----------")
    if len(ValidMoves) == 0:
        break
    else:
        for move in ValidMoves:
            strf = 'From: {0} index {1} offset {2}\nTo: {3} index {4}'.format(
            MoveDescriptor.PILE_TO_STRING[move.FromPileType],  
            move.FromPileIndex, 
            move.FromPileOffset, 
            MoveDescriptor.PILE_TO_STRING[move.ToPileType], 
            move.ToPileIndex)
            print(strf)
        PerformMove(ValidMoves[-1])
