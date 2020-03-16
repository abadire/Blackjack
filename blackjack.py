from classes.deck import Deck
from classes.hand import Hand

from classes.hand import Card

from math import floor
import os
import pdb

def print_cards(hands, is_dealer):
	to_print = []

	i = 0 # i, j, k add offset due to inserts' shifts
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
			if card == hand[-1] and hand != hands[-1]:
				for x in (i,j,k):
					to_print.insert(x, '| ')
				i += 1
				j += 2
				k += 3

	if is_dealer:
		for x in (1, 3, 5):
			to_print[x] = '###'

	for x in (i, j, k):
		to_print.insert(x, '\n')

	print(''.join(to_print))

def get_command(hand, total, bet):
	while True:
		if len(hand) == 2 and hand[0].value == hand[1].value and total >= bet:
			inp = input('You can (h)it, (s)tay, (d)ouble down or (sp)lit: ').lower().rstrip()
			if inp in ('h', 's', 'd', 'sp'):
				break
		elif total >= bet:
			inp = input('You can (h)it, (s)tay or (d)ouble down: ').lower().rstrip()
			if inp in ('h', 's', 'd'):
				break
		else:
			inp = input('You can (h)it or (s)tay: ').lower().rstrip()
			if inp in ('h', 's'):
				break
	return inp

def print_screen(dealer_hand, player_hand, total, bets, bid, is_dealer, idx=0):
	os.system('cls' if os.name == 'nt' else 'clear')
	print(f'Your total: {total}$')
	print(f'Your bid: {bid}$')
	if len(player_hand) > 1:
		for i, hand in enumerate(player_hand):
			print(f'Your {i+1} hand bet: {bets[i]}$')
	else:
		print(f'Your bet: {bets[idx]}$')
	print("\nDealer's hand:")
	print_cards(dealer_hand, is_dealer)
	if not is_dealer:
		print('Dealer has {}'.format(dealer_hand[0].score()))
	if len(player_hand) == 1:
		print('\nYour hand:')
	else:
		print('\nYour hands:')
		for ind, hand in enumerate(player_hand, 1):
			print(f'{ind}'.center(len(hand) * 3 + len(hand), ' '), end='  ') # Calculates and prints padding for hand numbers
		print('')
	print_cards(player_hand, False)
	if not is_dealer:
		if len(player_hand) > 1:
			for i, hand in enumerate(player_hand, 1):
				print(f'Your {i} hand has {hand.score()}')
		else:
			print('You have {}'.format(player_hand[0].score()))
	elif len(player_hand) > 1:
		print(f'You are playing hand {idx+1}:')
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

deck = Deck()
full_deck_size = 52

while player_money > 0:
	player_hand = [Hand()]
	dealer_hand = [Hand()]
	bets = []
	bid = place_bet(player_money)
	bets.append(bid)
	player_money -= bets[0]

	if len(deck) / full_deck_size < 0.3: # if deck is running low on cards
		del deck                         # delete old deck
		deck = Deck()                    # open a new one
		input('Deck reshuffled')

	for x in range(2):
		dealer_hand[0].append(deck.pop())
		player_hand[0].append(deck.pop())
	# player_hand[0].append(Card('A', 'B'))
	# player_hand[0].append(Card('A', 'C'))

	p_score = player_hand[0].score()
	d_score = dealer_hand[0].score()

	if p_score < 21 and d_score != 21:
		scores = []
		for idx, hand in enumerate(player_hand):
			if len(hand) == 1:
				hand.append(deck.pop())
			while True:
				if hand.score() > 20:
					break
				print_screen(dealer_hand, player_hand, player_money, bets, bid, is_dealer=True, idx=idx)
				command = get_command(hand, player_money, bets[0])
				if command == 's':
					break
				elif command == 'h':
					hand.append(deck.pop())
				elif command == 'd':
					hand.append(deck.pop())
					player_money -= bid
					bets[idx] += bid
					break
				elif command == 'sp':
					player_money -= bid
					bets.append(bid)
					player_hand.append(hand.pop())
					hand.append(deck.pop())

			scores.append(hand.score())

		scores_bool = [score < 22 for score in scores]

		if any(scores_bool):
			while dealer_hand[0].score() < 17:
				print_screen(dealer_hand, player_hand, player_money, bets, bid, is_dealer=False)
				input('Dealer hits... Press ENTER')
				dealer_hand[0].append(deck.pop())
		else:
			print_screen(dealer_hand, player_hand, player_money, bets, bid, is_dealer=True)
			input('You lose!')
			continue

		print_screen(dealer_hand, player_hand, player_money, bets, bid, is_dealer=False)
		d_score = dealer_hand[0].score()
		for idx, (score, bet) in enumerate(zip(scores, bets)):
			if d_score < 22:
				if score < d_score or score > 21:
					print('You lose!' if len(player_hand) == 1 else f'Your {idx+1} hand lose!')
				elif score == d_score:
					print('Draw!' if len(player_hand) == 1 else f'Your {idx+1} hand draw!')
					player_money += bet
				elif score > d_score:
					print('You win!' if len(player_hand) == 1 else f'Your {idx+1} hand win!')
					player_money += bet * 2
			else:
				if score < 22:
					print('You win!' if len(player_hand) == 1 else f'Your {idx+1} hand win!')
					player_money += bet * 2
				else:
					print('You lose!' if len(player_hand) == 1 else f'Your {idx+1} hand lose!')

		input()

	elif p_score == 21 and d_score != 21:
		print_screen(dealer_hand, player_hand, player_money, bets, bid, is_dealer=False)
		input('You win!')
		player_money += floor(bid * 2.5)
	elif p_score == 21 and d_score == 21:
		print_screen(dealer_hand, player_hand, player_money, bets, bid, is_dealer=False)
		input('Draw!')
		player_money += bid
	else:
		print_screen(dealer_hand, player_hand, player_money, bets, bid, is_dealer=False)
		input('You lose!')

input('Game over!')
