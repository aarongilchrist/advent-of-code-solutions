import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Cast each line into a tuple
hands = [tuple(input_string.split(' ')) for input_string in input_strings]

# Convert the bid to an int
hands = [(hand[0],int(hand[1])) for hand in hands]

# Define function to sort cards
# Ranking criterion is a list:

# For the first element -- a: 5 of a kind; b: 4 of a kind; c: full house; d: three of a kind; e: two pair; f: one pair; g: high card (all distinct)
# First get number of common cards held by grouping items in hand
# Remove jokers from string and itemise, raising largest value by difference between sum and 5 to represent moved jokers. Set value to [5] if 'JJJJJ'
itemise_hand = lambda hand: [n if index < len(set(hand.replace('J','')))-1 else n + hand.count('J') for index, n in enumerate(sorted([hand.count(card) for card in set(hand.replace('J',''))]))] if hand != 'JJJJJ' else [5]
# Classify hand according to above definition
classify_itemised = lambda itemised_hand: 'a' if itemised_hand == [5] else 'b' if itemised_hand == [1,4] else 'c' if itemised_hand == [2,3] else 'd' if itemised_hand == [1,1,3] else 'e' if itemised_hand == [1,2,2] else 'f' if itemised_hand == [1,1,1,2] else 'g'
classify_hand = lambda hand: classify_itemised(itemise_hand(hand))

# For the second and later elements the index of the card in order A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
card_ranks = ['A','K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
hand_to_card_ranks = lambda hand: [card_ranks.index(card) for card in list(hand)]

# Sort tuple of hands
card_sorting_function = lambda hand_tuple: [classify_hand(hand_tuple[0])] + hand_to_card_ranks(hand_tuple[0])

# Sort hands by this function
hands.sort(key = card_sorting_function)

# Get winnings for each hand
winnings = [(len(hands) - rank) * hand[1] for rank, hand in enumerate(hands)]

# Sum winnings
total_winnings = sum(winnings)

print(total_winnings)