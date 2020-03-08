from classes.card import Card
from random import shuffle

class Deck():
    '''
    Deck class
    '''
    def __init__(self):
        '''
        Initialize and shuffle deck
        '''
        self.deck = []
        for suit in ['♦', '♠', '♥', '♣']:
            for value in (list(range(2, 11)) + ['J', 'Q', 'K', 'A']):
                self.deck.append(Card(value=value, suit=suit))
        shuffle(self.deck)

    def __len__(self):
        '''
        Get deck size
        '''
        return len(self.deck)

    def __str__(self):
        '''
        String representation of Deck class (prints all cards in a Deck)
        '''
        string = ''
        for card in self.deck:
            string += card.suit + ' ' + str(card.value) + '\n'
        string = string[:-1]
        return string

    def pop(self):
        '''
        Get a card from deck
        '''
        return self.deck.pop()
