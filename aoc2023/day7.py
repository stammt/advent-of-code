import aoc_utils
from enum import IntEnum
import numpy
from functools import cmp_to_key

testInput = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
input = aoc_utils.PuzzleInput('input-day7.txt', testInput)

lines = input.getInputLines(test=False)

class Rank(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6
    
# labels = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
labels = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
labels.reverse()

def getRank(cards) -> int:
    # build a histogram of card counts to figure out the type of hand
    counts = {}
    for c in cards:
        if (c in counts):
            counts[c] = counts[c] + 1
        else:
            counts[c] = 1

    if len({card:count for (card, count) in counts.items() if count == 5}) == 1:
        return Rank.FIVE_OF_A_KIND
    if len({card:count for (card, count) in counts.items() if count == 4}) == 1:
        return Rank.FOUR_OF_A_KIND
    if len(
        {card:count for (card, count) in counts.items() if count == 3}) == 1 and len(
        {card:count for (card, count) in counts.items() if count == 2}) == 1:
        return Rank.FULL_HOUSE
    if len(
        {card:count for (card, count) in counts.items() if count == 3}) == 1 and len(
        {card:count for (card, count) in counts.items() if count == 2}) == 0:
        return Rank.THREE_OF_A_KIND
    if len({card:count for (card, count) in counts.items() if count == 2}) == 2:
        return Rank.TWO_PAIR
    if len(
        {card:count for (card, count) in counts.items() if count == 2}) == 1 and len(
        {card:count for (card, count) in counts.items() if count == 1}) == 3:
        return Rank.ONE_PAIR
    if len({card:count for (card, count) in counts.items() if count == 1}) == 5:
        return Rank.HIGH_CARD

def compareBetRank(a, b) -> int:
    return compareRank(a[0], b[0])

# each param is (optimized, original) hand
def compareRank(a, b) -> int:
    myRank = getRank(a[0])
    otherRank = getRank(b[0])
    if (myRank > otherRank):
        return 1
    if (otherRank > myRank):
        return -1
    
    # fall back to checking the cards in order
    for i in range(len(a[1])):
        myCardRank = labels.index(a[1][i])
        otherCardRank = labels.index(b[1][i])
        if (myCardRank > otherCardRank):
            return 1
        if (otherCardRank > myCardRank):
            return -1
    
    return 0
        
def optimizeHand(cards):
    jokers = []
    for i in range(len(cards)):
        if (cards[i] == 'J'):
            jokers.append(i)

    if len(jokers) == 0:
        return (cards, cards)
    
    # If all 5 cards are jokers, return 5 Aces
    if (len(jokers) == 5):
        return ('AAAAA', cards)
    
    # If 4 cards are jokers, make them the same as the fifth card to make 5 of a kind
    if (len(jokers) == 4):
        other = list(filter(lambda x: x != 'J', cards))[0]
        return ('' + other + other + other + other + other, cards)
    
    # If 3 cards are jokers, pick the highest of the other two and make 4 of a kind
    if (len(jokers) == 3):
        others = list(filter(lambda x: x != 'J', cards))
        maxOther = labels[max(labels.index(others[0]), labels.index(others[1]))]
        cardsCopy = list(cards)
        for i in jokers:
            cardsCopy[i] = maxOther
        return (''.join(cardsCopy), cards)
    
    # Otherwise just brute force it, generate all possible hands and pick the one with
    # the highest rank.
    if (len(jokers) == 2):
        options = []
        for a in range(len(labels)):
            for b in range(len(labels)):
                option = list(cards)
                option[jokers[0]] = labels[a]
                option[jokers[1]] = labels[b]
                options.append((''.join(option), cards))
        sortedOptions = sorted(options, key=cmp_to_key(compareRank))
        return sortedOptions[len(sortedOptions) - 1]    

    if (len(jokers) == 1):
        options = []
        for a in range(len(labels)):
            option = list(cards)
            option[jokers[0]] = labels[a]
            options.append((''.join(option), cards))
        sortedOptions = sorted(options, key=cmp_to_key(compareRank))
        # print(f' options for 1 joker {cards}: {options} : sorted to {sortedOptions}')
        return sortedOptions[len(sortedOptions) - 1]    



def part1(lines):
    hands = []
    for line in lines:
        cards, bid = line.split()
        # hand = Hand(cards)
        hands.append((cards, bid))
        # print(f'{cards} has rank {hand.getRank()} with bid {int(bid)}: {hand.getRank() * int(bid)}')

    sortedHands = sorted(hands, key=cmp_to_key(compareBetRank))
    print(f'Sorted: {sortedHands}')

    winnings = 0
    handCount = len(sortedHands)
    for i in range(handCount):
        print(f'adding {i+1} * {int(sortedHands[i][1])}: {((i+1) * int(sortedHands[i][1]))}')
        winnings = winnings + ((i+1) * int(sortedHands[i][1]))
    print(f'Winnings: {winnings}')

def part2(lines):
    hands = []
    for line in lines:
        cards, bid = line.split()
        optimized = optimizeHand(cards)
        print(f'optimized: {optimized}')
        hands.append((optimized, bid))

    sortedHands = sorted(hands, key=cmp_to_key(compareBetRank))
    print(f'Sorted: {sortedHands}')

    winnings = 0
    handCount = len(sortedHands)
    for i in range(handCount):
        print(f'adding {sortedHands[i][0]} {i+1} * {int(sortedHands[i][1])}: {((i+1) * int(sortedHands[i][1]))}')
        winnings = winnings + ((i+1) * int(sortedHands[i][1]))
    print(f'Winnings: {winnings}')

part2(lines)