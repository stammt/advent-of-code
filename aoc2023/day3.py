# input = """467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598.."""
# lines = input.splitlines()


f = open('input-day3.txt', 'r')
lines = f.readlines()

grid = [list(line.strip()) for line in lines]
print(grid)

# map of (x,y) of star to list of part numbers it is adjacent to
stars = {}


def isSymbol(c):
    return len(c) > 0 and c != '.' and not c.isdigit()

def checkSymbol(grid, x, y, number):
    c = grid[y][x]
    if isSymbol(c):
        pos = (x, y)
        if c == '*':
            if pos in stars:
                stars[pos].append(number)
            else:
                stars[pos] = [number]
        return True

def hasAdjacentSymbol(y, number, numberStart, numberEnd):
    startX = max(0, numberStart - 1)
    endX = min(len(line), numberEnd+2)
    result = False

    # crappy side-effect: if the symbol is a star, add the number to the map

    # Check line above
    if y > 0:
        for i in range(startX, endX):
            if checkSymbol(grid, i, y-1, number):
                result = True

    # Check before and after number
    for i in range(startX, endX):
        if checkSymbol(grid, i, y, number):
            result = True
        
    # Check line below
    if y < len(grid) - 1:
        for i in range(startX, endX):
            # print(f'Checking {y+1} {i} {grid[y+1][i]}')
            if checkSymbol(grid, i, y+1, number):
                result = True
            
    return result

# look for numbers, then inspect chars around the number
sum = 0
for y in range(len(grid)):
    line = grid[y]
    x = 0
    while (x < len(line)):
        if line[x].isdigit():
            numberStr = ''
            numberStart = x
            numberEnd = x
            while (x < len(line) and line[x].isdigit()):
                numberStr += line[x][0]
                numberEnd = x
                x+=1

            if len(numberStr) > 0:
                partNumber = int(numberStr)
                isPartNumber = hasAdjacentSymbol(y, number=partNumber, numberStart=numberStart, numberEnd=numberEnd)
                if y == len(grid) - 1 and not isPartNumber:
                    print(f'Found {partNumber} {isPartNumber} at {numberStart} - {numberEnd}, {y}')
                if isPartNumber:
                    sum += partNumber

        else:
            x+=1

# print(f'sum: {sum}')
#print(f'gears: {stars}')
gearSum = 0
for star in stars:
    numbers = stars[star]
    if len(numbers) == 2:
        gearSum += (numbers[0] * numbers[1])

print(f'gear sum {gearSum}')