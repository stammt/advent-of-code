# input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
# lines = list(map(lambda x: x.strip(), input.splitlines()))

import time


f = open('input/input-day4.txt', 'r')
lines = f.readlines()


def part1():
    totalScore = 0
    for line in lines:
        winnersList, yoursList = map(lambda x: x.strip().split(), line.split(': ')[1].split(' | '))
        winnersSet = set(map(lambda x: int(x), winnersList))
        yoursSet = set(map(lambda x: int(x), yoursList))
        yourWinners = set(filter(lambda x: x in winnersSet, yoursSet))
        cardScore = 0 if yourWinners == set() else 2 ** (len(yourWinners) - 1)
        totalScore += cardScore
        print(f'Winners {winnersSet}, yours {yoursSet}, yourWinners: {yourWinners}: score: {cardScore}')

    print(f'Total score: {totalScore}')


def part2():
    cardCounts = [1 for line in lines]
    for i in range(0, len(lines)):
        line = lines[i]
        winnersList, yoursList = map(lambda x: x.strip().split(), line.split(': ')[1].split(' | '))
        winnersSet = set(map(lambda x: int(x), winnersList))
        yoursSet = set(map(lambda x: int(x), yoursList))

        winnerCount = len(set(filter(lambda x: x in winnersSet, yoursSet)))
        # print(f'Card {i} has {winnerCount} winners')
        if winnerCount > 0:
            cardCount = cardCounts[i]
            for x in range(i+1, min(len(lines), i+1+winnerCount)):
                cardCounts[x] = cardCounts[x] + cardCount
        
    # get the total count of cards
    totalCards = sum(cardCounts)
    print(f'Total cards: {totalCards}')


start = time.perf_counter()
part2()
end = time.perf_counter()
print(f'Took {(end - start) * 1000}ms ')