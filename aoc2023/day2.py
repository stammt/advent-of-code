# input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

# lines = input.splitlines()

f = open('input-day2.txt', 'r')
lines = f.readlines()


maxRed = 12
maxGreen = 13
maxBlue = 14
maxes = {'red': maxRed, 'green': maxGreen, 'blue': maxBlue}

def gameInfo(line):
    game, hands = line.split(':')
    gameNum = int(game.split(' ')[1])
    print(f'Game {gameNum}, hands {hands}')
    for hand in hands.split(';'):
        print(f'hand: {hand}')
        counts = hand.strip().split(', ')
        for count in counts:
            print(f'count: {count}')
            num, color = count.split(' ')
            max = maxes[color]
            if int(num) > max:
                return gameNum, False
    return gameNum, True

def gamePower(line):
    game, hands = line.split(':')
    gameNum = int(game.split(' ')[1])
    mins = {'red': 0, 'green': 0, 'blue': 0}
    print(f'Game {gameNum}, hands {hands}')
    for hand in hands.split(';'):
        print(f'hand: {hand}')
        counts = hand.strip().split(', ')
        for count in counts:
            print(f'count: {count}')
            num, color = count.split(' ')
            min = mins[color]
            if int(num) > min:
                mins[color] = int(num)
    print(f'minimums: {mins}')
    return mins['red'] * mins['green'] * mins['blue']

sum = 0
for line in lines:
    power = gamePower(line)
    print(f'{power} for {line}')
    sum += power
    # num, possible = gameInfo(line)
    # print(f'game {num} is {possible}')
    # if possible:
    #     sum += num

print(f'sum: {sum}')
