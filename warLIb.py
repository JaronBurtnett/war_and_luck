import json
import random

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

def logDecks(y,c,t):
    aCounter = len(t.track) +1
    y.deckAtHand[str(aCounter)] = f'{str(y.cards)}\n' #hopefully the new line will make a JSOn more readable iwhen I open it
    c.deckAtHand[str(aCounter)] = f'{str(c.cards)}\n' #if opened in just text editor it just shows the new line characters




''' have the program look in the folder. if it sees newUserCards.json already there it
will append something to the name like 'second play' or something like that.'''


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

   
class Player:
    def __init__(self, cards, deckAtHand = None):
        self.cards = cards #cards they currently have
        self.deckAtHand = deckAtHand #what their deck looked like at each previous play

class Logistics:
    def __init__(self, track, warCounter, dLens): 
        self.track = track
        self.warCounter = warCounter
        self.dLens = dLens #so I can return decks to riginal lengths before appending with war cards
       

