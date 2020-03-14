from classes.deck import Deck
from classes.hand import Hand
from math import floor
import os
import pdb

def print_cards(hands, is_dealer):
	to_print = []

	i = 0
	j = 1
	k = 2

	hand_counter = 1

	for hand in hands:
		for card in hand:
			to_print.insert(i, f'{str(card.value)}# ' if card.value == 10 else f'{str(card.value)}## ')
			to_print.insert(j, f'#{card.suit}# ')
			to_print.insert(k, f'#{str(card.value)} ' if card.value == 10 else f'##{str(card.value)} ')
			i += 1
			j += 2
			k += 3
		# if hand_counter < len(hands):
		# 	for x in (i,j,k):
		# 		to_print.insert(x, '|')
		# 		hand_counter += 1

	if is_dealer:
		for x in (1, 3, 5):
			to_print[x] = '###'

	for x in (i, j, k):
		to_print.insert(x, '\n')

	print(''.join(to_print))

def get_command():
	while True:
		inp = input('You can (h)it, (s)tay or (d)ouble down: ').lower().rstrip()
		if inp in ('h', 's', 'd'):
			return inp[0]

def print_screen(dealer_hand, player_hand, total, bet, is_dealer):
	os.system('cls' if os.name == 'nt' else 'clear')
	print(f'Your total: {total}$')
	print(f'Your bet: {bet}$')
	print("Dealer's hand:")
	print_cards(dealer_hand, is_dealer)
	if not is_dealer:
		print('Dealer has {}'.format(dealer_hand[0].score()))
	print('\nYour hand:')
	print_cards(player_hand, False)
	if not is_dealer:
		print('You have {}'.format(player_hand[0].score()))
	print('')

def get_bet():
	while True:
		try:
			bet = int(input('Place bet: '))
		except KeyboardInterrupt:
			break
		except:
			continue
		else:
			return bet

def place_bet(total):
	os.system('cls' if os.name == 'nt' else 'clear')
	print(f'You have {total}$')
	while True:
		bet = get_bet()
		if bet > total:
			input('Insufficient funds!')
		else:
			return bet

player_money = 100

player_hand = [Hand()]
dealer_hand = [Hand()]

deck = Deck()
full_deck_size = 52

while player_money > 0:

	bet = place_bet(player_money)
	player_money -= bet

	if len(deck) / full_deck_size < 0.3: # if deck is running low on cards
		del deck                         # delete old deck
		deck = Deck()                    # open a new one
		input('Deck reshuffled')

	for x in range(2):
		dealer_hand[0].append(deck.pop())
		player_hand[0].append(deck.pop())

	print_screen(dealer_hand, player_hand, player_money, bet, is_dealer=True)

	p_score = player_hand[0].score()
	d_score = dealer_hand[0].score()

	if p_score < 21 and d_score != 21:
		while True:
			command = get_command()
			if command == 's':
				break
			elif command == 'h':
				player_hand[0].append(deck.pop())
				print_screen(dealer_hand, player_hand, player_money, bet, is_dealer=True)
			elif command == 'd':
				if player_money - bet < 0:
					print("You don't have enough funds to double down!")
				else:
					player_hand[0].append(deck.pop())
					player_money -= bet
					bet = bet * 2
					break
			if player_hand[0].score() > 20:
				break

		p_score = player_hand[0].score()

		if p_score < 22:
			while dealer_hand[0].score() < 17:
				print_screen(dealer_hand, player_hand, player_money, bet, is_dealer=False)
				input('Dealer hits...')
				dealer_hand[0].append(deck.pop())

			print_screen(dealer_hand, player_hand, player_money, bet, is_dealer=False)

			if p_score < dealer_hand[0].score() < 22:
				input('You lose!')
			elif p_score == dealer_hand[0].score():
				input('Draw!')
				player_money += bet
			else:
				input('You win!')
				player_money += bet * 2
		else:
			print_screen(dealer_hand, player_hand, player_money, bet, is_dealer=False)
			input('You lose!')

	elif p_score == 21 and d_score != 21:
		print_screen(dealer_hand, player_hand, player_money, bet, is_dealer=False)
		input('You win!')
		player_money += floor(bet * 2.5)
	elif p_score == 21 and d_score == 21:
		print_screen(dealer_hand, player_hand, player_money, bet, is_dealer=False)
		input('Draw!')
		player_money += bet
	else:
		print_screen(dealer_hand, player_hand, player_money, bet, is_dealer=False)
		input('You lose!')

	dealer_hand[0].clear()
	player_hand[0].clear()

input('Game over!')
