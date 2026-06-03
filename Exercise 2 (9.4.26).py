"""number = int(input("Enter a starting number: "))
while number > 0:
    print(number)
    number -= 1
print("Done")"""

"""for i in range(1, 31):
    if i % 3 == 0:
        print(i)"""

"""while True:
    user_input = input("Enter text: ")
    if user_input.lower() == "keluar":
        break
print("Input stopped")"""

"""number = 0
while number < 100:
    number += 1
    if number % 7 != 0:
        continue 
    print(number)"""

"""count = 0
while count < 5:
    print(count)
    count += 1
else:
    print("The loop ends")"""

"""for row in range(5):
    for col in range(3):
        print("*", end=" ")
    print()"""

"""positives = 0
negatives = 0
zeros = 0
print("Please enter 10 integers:")
for i in range(1, 11):
    num = int(input(f"Enter number {i}: "))
    if num > 0:
        positives += 1
    elif num < 0:
        negatives += 1
    else:
        zeros += 1
print("\n--- Results ---")
print(f"Positive numbers: {positives}")
print(f"Negative numbers: {negatives}")
print(f"Zeroes:           {zeros}")"""

"""num = int(input("enter a number: "))
for i in range (1, num + 1):
    if i % 2 == 0:
        print (i, "odd")
    else:
        print(i, "even")"""

count = 0
total = 0
greater_50 = 0

"""while True:
    num = int(input("Enter a number (-1 to stop): "))
    if num == -1:
        break
    count += 1
    total += num
    if num > 50:
        greater_50 += 1

print("Total valid inputs:", count)
print("Sum of inputs:", total)
print("Numbers greater than 50:", greater_50)"""

"""word = input("Enter a word: ")
vowels = 0
consonants = 0
for ch in word:
    if ch in "aeiou":
        vowels += 1
    else:
        consonants += 1
print("Vowels:", vowels)
print("Consonants:", consonants)"""

start = int(input("Start number: "))
end = int(input("End number: "))
for i in range(start, end + 1):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)








