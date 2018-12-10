print("Welcome to the Guess game!")
print("The rules are simple: you should guess an integer from 1 to 100.")
print("For that, just input the number you want.")
print("After every guess we will inform you about your success (or fail ;) ).")

from random import randint as rand

ans = rand(1, 100)
errors = 0
tries = 0
len = 99

while True:
    s = input("Please enter the number: ")
    tries += 1
    if not(s.isnumeric()):
        print("You can use only digits!")
        errors += 1
        continue
    n = int(s)
    if n < 1 or n > 100:
        print("OUT OF BOUNDS!")
        errors += 1
        continue
    if n == ans:
        print(f"You guessed! And it took {tries} guesses!")
        break
    if tries - errors == 1:
        len = abs(n - ans)
        if len <= 10:
            print("WARM!")
        else:
            print("COLD!")
    else:
        if abs(n - ans) > len:
            print("COLDER!")
        elif abs(n - ans) < len:
            print("WARMER!")
        else:
            print("Hm... Nothing changed actually")
        len = abs(n - ans)
