from classes.card import Card

class Hand():
    '''
    Hand class
    '''
    def __init__(self):
        '''
        Init w/ empty hand
        '''
        self.hand = []

    def append(self, card):
        '''
        Add a card to a hand
        '''
        self.hand.append(card)

    def clear(self):
        '''
        Clears Hand
        '''
        self.hand.clear()

    def __str__(self):
        '''
        String representation of Hand class (prints all cards in a Hand)
        '''
        string = ''
        for card in self.hand:
            string += f'({card.suit}, {str(card.value)}), '
        string = string[:-2]
        return string

    def __getitem__(self, i):
        return self.hand[i]

    def score(self):
        '''
        Count hand score
        '''
        aces = 0
        total = 0
        for card in self.hand:
            if type(card.value) == str:
                if card.value == 'A':
                    total += 11
                    aces += 1
                else:
                    total +=10
            else:
                total += card.value
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total
