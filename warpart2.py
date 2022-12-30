import json
import warLIb as wl
import numpy


def pullCards(dac): 
    arrayWithZeroes = numpy.array([dac])
    zeroArray = numpy.where(arrayWithZeroes == 0) #if there are any zeroes in the deck we find them... 
    zeroLocations = zeroArray[1].tolist()
    zeroLocations.reverse()
    for x in zeroLocations:
        dac.pop(x) #and nuke them.

    return dac
     #now the player has all the cards they had in their deck at the play they have inicated


warFile = open('newUserCardso.json', 'r')#having it load files that I manual appen with 'o' at the end
#just for testing. Will have to code in better file naming and selection later.

data = warFile.read()
allThePlays = json.loads(data)
warFile.close()

warFile2 = open('newCompCardso.json','r')
data2 = warFile2.read()
compsPlays = json.loads(data2)
warFile2.close()


print(f'There were {len(allThePlays.keys())} cards played in the game.')
playerChoice = input('Which play would you like to change? \n')

#will need to do some input validation
deckAtChoice = json.loads(allThePlays[str(playerChoice)])
computerDeck = json.loads(compsPlays[str(playerChoice)])

deckToChange = pullCards(deckAtChoice)
print(f'You have {len(deckToChange)} cards. Which card would you like to play instead of your next card?')
playerChoice = input(f'enter a number between 2 and {len(deckToChange)}')
selectedCard = (deckToChange[int(playerChoice) - 1])
deckToChange.pop(int(playerChoice) - 1)
deckToChange.insert(0,selectedCard)


user = wl.Player(deckToChange,{})

comp = wl.Player(pullCards(computerDeck),{})


theGame = wl.Logistics([], 4, [1,1])  


while len(user.cards) != 0 and len(comp.cards) != 0:
    if len(user.cards) == 0:
        print('you lose')
        break
    elif len(comp.cards) == 0:
        print('you win') 
        break      
    elif user.cards[0] > comp.cards[0]:
        (user, comp, theGame) = wl.youWin(user, comp, theGame) 
        
    elif user.cards[0] < comp.cards[0]:
        (user, comp, theGame) = wl.youLose(user, comp, theGame)
        
    elif user.cards[0] == comp.cards[0]:
        (user, comp, theGame) = wl.warCardPlay(user, comp, theGame)
        
    

wl.logDecks(user, comp,theGame)  
wl.logGame(user.deckAtHand, comp.deckAtHand)
