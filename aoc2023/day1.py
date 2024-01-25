#inputx = """1abc2
#pqr3stu8vwx
#a1b2c3d4e5f
#treb7uchet
#"""
#xlines = input.splitlines()

f = open('input/input-day1.txt', 'r')
lines = f.readlines()

# input = """two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen"""
# lines = input.splitlines()
# print(lines)

numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def getdigit(s):
    if s[0].isdigit():
        return int(s[0])
    else:
        for i, word in enumerate(numbers):
            if s.startswith(word):
                return i+1
            
    return -1


sum = 0
for line in lines:
    digits = []
    for i in range(len(line)):
        subline = line[i:]
        d = getdigit(subline)
        #print(f'getdigit for {subline} returned {d}')
        if d > -1:
            digits.append(d)

#    digits = list(filter(lambda c: c.isdigit(), list(line)))
    print(digits)
    num = (10 * int(digits[0])) + int(digits[len(digits)-1])
    print(num)
    sum += num

print(f'final sum {sum}')