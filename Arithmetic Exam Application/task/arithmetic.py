import random

count = 0
correct = 0

expression = ()


def generate(new):
    global expression, count, result, level, correct, level_description
    if new:
        if level == 1:
            expression = str(random.randint(2, 9)), random.choice(['*', '+', '-']), str(random.randint(2, 9))
            count += 1
            level_description = '1 - simple operations with numbers 2-9'
            if expression[1] == '*':
                result = int(expression[0]) * int(expression[2])
            elif expression[1] == '+':
                result = int(expression[0]) + int(expression[2])
            elif expression[1] == '-':
                result = int(expression[0]) - int(expression[2])
            print(' '.join(expression))
        elif level == 2:
            expression = random.randint(11, 29)
            count += 1
            level_description = '2 - integral squares of 11-29'
            result = expression * expression
            print(expression)
        else:
            print('Incorrect format.')
    num = input()
    try:
        if result == int(num):
            print('Right!')
            correct += 1
        else:
            print('Wrong!')
    except ValueError:
        print('Incorrect format.')
        generate(False)


print('Which level do you want? Enter a number:\n'
      '1 - simple operations with numbers 2-9\n'
      '2 - integral squares of 11-29')
level = int(input())
while count < 5:
    generate(True)
print(f'Your mark is {correct}/{count}. Would you like to save the result? Enter yes or no')
option = input().lower()
if option != 'yes' and option != 'y':
    print(option)
    exit()
print('What is your name?')
name = input()

with open('results.txt', 'a') as file:
    file.write(f'{name.capitalize()}: {correct}/{count} in level {level} ({level_description}).')
print('The results are saved in \"results.txt\".')
