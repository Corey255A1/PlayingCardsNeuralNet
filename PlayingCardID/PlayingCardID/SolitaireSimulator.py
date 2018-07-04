from Solitaire import Klondike, MoveDescriptor


klondike = Klondike()

#Discard one for now.. 
klondike.Draw()

while True:
    ValidMoves = klondike.GetValidMovesForDiscard()
    ValidMoves = ValidMoves + klondike.GetValidMovesForColumns()
    ValidMoves = ValidMoves + klondike.GetValidMovesForHome()
    print("----------- SPREAD ".ljust(80,'-'))
    print(klondike.PrettyPrintCards())

    print("\n--------- Valid Moves ".ljust(80,'-'))

    m =0
    for move in ValidMoves:
        strf = klondike.PrettyPrintMoveDescriptor(move)
        print(str(m) + ": " + strf)
        m = m + 1
    print("D to Draw")
    selectedMove = input("Select a move: ")
    if selectedMove == 'Q':
        break
    if selectedMove == 'D':
        klondike.Draw()
    else:
        sm = int(selectedMove)
        klondike.PerformMove(ValidMoves[sm])

    print("-"*80)
