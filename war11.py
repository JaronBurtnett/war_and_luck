#the war function is not showing the tracking of each card laid down as a change in the deck.

#during war change card at index that was just put down to a 0 so that it is a non card. Deck length stays the same for mop up, and then 
#front 0's can be cleaned up as well

import random

import csv
import json

# I can see what you're doing here, creating a deck of cards then pulling out random ones and alternating between the two players.
# The idea is good though you've done it a very messy way.
# First off, the 'dc' variable is pretty much entirely pointless. You're using it to keep track of how many cards are left in the deck, but you could just use the length of the deck list with len(deck).
# The check for 'if dc == 0' is redundant since the for loop will run dc times anyways and then stop.
# Another reason not to use 'dc' is that it makes your code fragile. Say you change the makeup of the deck with more or less cards and forget to update dc to match. Your code will break since it will expect a different number of cards than it actually gets.
# Second,  you're using 'dealt' to keep track of which card is being dealt that round. While not bad a bit messy. Simpler method would be to simply use the pop() method to remove the card from the deck and assign it to the player.
# Third, you're using 'dealDir' to keep track of which player is getting the card. This truthfully isn't the worst method but if you assume that the deck is always even then you can just give each player a random card from the deck and then remove it from the deck.
# I've created 'deckDeal2' as an example of how I would implement this.
def deckDeal(user, comp):
    deck = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,
    9,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,13,13,13,13,14,14,14,14]
    dealDir = 1
    dc = 52
  
    for x in range(dc):
        dc -= 1
        if dc == 0:
            comp.cards.append(deck[0])
            break
        dealt = random.randint(0,dc)
        if dealDir == 1:
            user.cards.append(deck[dealt])
        elif dealDir == 2:
            comp.cards.append(deck[dealt])
        dealDir = dealDir + 1
        if dealDir > 2:
            dealDir = 1     
        deck.remove(deck[dealt])

def deckDeal2(user, comp):
    deck = generateDeck(0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4)

    # Does assume the number of cards in the deck is even.
    while len(deck) > 0:
        user.cards.append(deck.pop(randint(0, len(deck) - 1)))
        comp.cards.append(deck.pop(randint(0, len(deck) - 1)))

# I consider this to be a clean way of generating the deck you want. The 'numberOfCards' is a list of numbers, the position of the number in the list represents the card's value (The first position representing the number of '1's) while the number in that place represents the number of those cards that you want. I consider this to be more readable and easier to understand.
# The 'enumerate' function is a nice way to get the index and value of each item in a list. It's a bit more efficient than using a for loop and keeping track of the index yourself.
def generateDeck(*numberOfCards):
    deck = []
    for cardValue, numberOfCards in enumerate(numberOfCards):
        for i in range(numberOfCards):
            deck.append(cardValue + 1)
    return deck

def logDecks(y,c,t):
    aCounter = len(t.track) +1
    y.deckAtHand[str(aCounter)] = f'{str(y.cards)}\n' #hopefully the new line will make a JSOn more readable iwhen I open it
    c.deckAtHand[str(aCounter)] = f'{str(c.cards)}\n' #if opened in just text editor it just shows the new line characters


def logGame(y,c): #getting the log of hands as json
    logJson = json.dumps(y)
    f = open('newUserCards.json', 'a')
    f.write(logJson)   
    f.close()
    logJson = json.dumps(c)
    f = open('newCompCards.json', 'a')
    f.write(logJson)   
    f.close()

 
def youWin(y,c,t):
    logDecks(y, c, t)
    y.cards.append(y.cards[0])#picking up players card
    y.cards.append(c.cards[0])#picking up opponents captured card
    t.track.append((y.cards[0],c.cards[0]))# tuples listing the 2 cards that were played
    y.cards.pop(0)#getting rid of the now duplcated cards from the front of their 
    c.cards.pop(0)#respective decks
    print('win at play '+ str(len(t.track)))#alert what happened 
    return ((y,c,t))


def youLose(y,c,t):
    logDecks(y, c, t)
    c.cards.append(c.cards[0])#comp picks up it's card
    c.cards.append(y.cards[0])#comp picks up user card
    t.track.append((y.cards[0],c.cards[0])) #logging the cards that were played
    y.cards.pop(0)#removing duplicate card for user
    c.cards.pop(0)#removing duplicate card for comp
    print('loss at play ' + str(len(t.track)))#alert what happened  
    return((y,c,t))

def warCardCheck(y,c,t):#first finding out how high the war counter can go before someone
                        #runs out of cards.
    t.dLens[0] = eny = len(y.cards)
    t.dLens[1] = enc = len(c.cards)
    while eny < 52: # padding them both out to 52 seemed simpler than 
        y.cards.append(0) # doing a for in range(4) append (0)... less
        eny += 1
    while enc < 52:        #typing with just less than greater than, but 
        c.cards.append(0)   #long comment to explain. Padding prevents index 
        enc += 1               #error and lets me check when card becomes 0  
    while y.cards[t.warCounter] == c.cards[t.warCounter] and y.cards[t.warCounter] != 0 and c.cards[t.warCounter] != 0:
        t.warCounter += 4 #increase where we look for the deciding card until they do not match
    return (y,c,t)


def warCardPlay(y,c,t):
    (y,c,t) = warCardCheck(y,c,t)
    warSpoils = []# need to give cards to war winner after cleaning up their deck
    if y.cards[t.warCounter] > c.cards[t.warCounter]:
        logDecks(y, c, t)#war mopUp hasn't run. Will have wrong deck if left here without deleting
        for index in range(t.warCounter+1):         #cards that get logged, at least in log here. mopup can take care of deck
            logDecks(y, c, t) 
            warSpoils.append(y.cards[index])#picking up all user cards first
            warSpoils.append(c.cards[index])
            t.track.append((y.cards[index], c.cards[index]))#tracking the play Don't think I utilize this data yet. 
            y.cards[index] = 0
            c.cards[index] = 0
        (y,c,t) = warMopUp(y,c,t)
        y.cards = distSpoils(y.cards, warSpoils)
        print('war win at play ' + str(len(t.track))) 
    elif y.cards[t.warCounter] < c.cards[t.warCounter]:
        for index in range(t.warCounter+1):
            logDecks(y, c, t)
            warSpoils.append(c.cards[index])
            warSpoils.append(y.cards[index])
            t.track.append((y.cards[index], c.cards[index]))
            y.cards[index] = 0
            c.cards[index] = 0
        (y,c,t) = warMopUp(y,c,t)
        c.cards = distSpoils(c.cards, warSpoils)
        print('war loss at play ' + str(len(t.track)))
    elif y.cards[t.warCounter] == 0 and t.dLens[0] > t.dLens[1]: #t.dLens is a a tuple index 0 is len(user's deck) index 1 is len(computers hand)
        del c.cards[t.dLens[1]:53]
        for i in c.cards:
            y.cards.append(i)
    elif c.cards[t.warCounter] == 0 and t.dLens[0] < t.dLens[1]:
        del y.cards[t.dLens[0]:53]
        for i in y.cards:
            c.cards.append(i)
    return((y,c,t))

def warMopUp(y,c,t): #this will be used to wrap up wars and return any counters to base value
    del y.cards[t.dLens[0]:53]#works because leny as index is one more since indexes start at 0
    del c.cards[t.dLens[1]:53] #returning the hands to pre added 0's
    del y.cards[:t.warCounter+1]
    del c.cards[:t.warCounter+1]
    t.warCounter = 4 # for wars that don't end the game t.warCounter needs to return to 4 for the next war
    return (y,c,t)

def distSpoils(v,w):#victor and war spoils
    for i in w:
        v.append(i)
    return v



def writeGame(t):
    wf = open('war_file.csv', 'a')
    wfWriter = csv.writer(wf)
    wfWriter.writerow(t.track)
    wf.close()

   
class Player:
    def __init__(self, cards, deckAtHand):
        self.cards = cards #cards they currently have
        self.deckAtHand = deckAtHand #what their deck looked like at each previous play

class Logistics:
    def __init__(self, track, warCounter, dLens): 
        self.track = track
        self.warCounter = warCounter
        self.dLens = dLens #so I can return decks to riginal lengths before appending with war cards
       


user = Player([],{})
comp = Player([], {})
theGame = Logistics([], 4, [1,1])  

deckDeal(user, comp) #distributing the entire deck list between the user and the computer
#print(user.cards)
#print(comp.cards)
#not using this function right now for testing

#user.cards = [5, 8, 4, 6, 2] #use to test scenarios comment out deal function
#comp.cards = [5, 4, 3, 12, 8, 4, 2, 14, 14, 11, 9, 13, 14, 2, 8, 14, 12, 11, 7, 13, 10, 13, 12, 6, 6, 11, 6, 4, 3, 10, 9, 5, 5, 8, 7, 2, 3, 12, 7, 10, 3, 11, 9, 9, 7, 13, 10] #use to test scenarios

while len(user.cards) != 0 and len(comp.cards) != 0:
    # Since the loop will be breaking when one of the decks is empty, I don't need to check for that here. I moved it to outside of the loop.
    # if len(user.cards) == 0:
    #     print('you lose')
    #     break
    # elif len(comp.cards) == 0:
    #     print('you win') 
    #     break   

    playerCard = user.cards.pop()
    compCard = comp.cards.pop()
    pool = [playerCard, compCard]

    while True:
        print(str(playerCard) + ' ' + str(compCard))
        if playerCard > compCard:
            print('you win')
            user.cards.extend(pool)
            break
        elif playerCard < compCard:
            print('you lose')
            comp.cards.extend(pool)
            break
        elif playerCard == compCard:
            if len(user.cards) == 0:
                print('you lose')
                comp.cards.extend(pool)
                break
            elif len(comp.cards) == 0:
                print('you win')
                user.cards.extend(pool)
                break
            else:
                for _ in range(3):
                    if len(user.cards) > 1: # Ensures the last card in the deck is not added to the pool
                        pool.append(user.cards.pop())
                    if len(comp.cards) > 1:
                        pool.append(comp.cards.pop())
                playerCard = user.cards.pop()
                compCard = comp.cards.pop()
        
# You're attempt here was pretty good. Honestly this was a challenge for me to figure out a cleaner way. I'm just going to put what I came up with and let you think about it.
    # elif user.cards[0] > comp.cards[0]:
    #     (user, comp, theGame) = youWin(user, comp, theGame) 
        
    # elif user.cards[0] < comp.cards[0]:
    #     (user, comp, theGame) = youLose(user, comp, theGame)
        
    # elif user.cards[0] == comp.cards[0]:
    #     (user, comp, theGame) = warCardPlay(user, comp, theGame)

if len(user.cards) == 0:
    print('you lose the game...')
elif len(comp.cards) == 0:
    print('you win the game!')
    
#writeGame(theGame)
#logDecks(user, comp,theGame) #just needed tp show the final outcome of who has no cards and the other with the whole deck. 
#logGame(user.deckAtHand, comp.deckAtHand)
#theSwap = chooseCard(theGame)
#theGame = divideTracking(theGame)
#theGame = repositionCards(theGame, theSwap)

'''I am going to do the part that lets you pick and change a play in another module'''

    
    
    



