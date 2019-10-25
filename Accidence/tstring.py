import cmath
import math
name = 'John'
age = 23
print('%s is %d years old.' % (name, age))
params = {'name': 'John', 'age': 23}
print('%(name)s is %(age)d years old' % params)

mylist = [1, 2, 3]
print("A list: %s" % mylist)

data = ('John', 'Doe', 55.34)
format_string = 'Hello %s %s. Your current balance is $%.2f.'
format_string2 = 'Hello %s %s. Your current balance is $%s.'

print(format_string % data)
print(format_string2 % data)

astring = 'Hello World!'
print(astring.index('o'))
print(astring.count('l'))
print(astring[3:7])

# [start:stop:step].
print(astring[3:10:2])

print(astring[-1])
print(astring[::-1])

print(astring.upper())
print(astring.lower())

print(astring.startswith('Hello'))
print(astring.endswith('asdf'))

print(astring.split())
print(astring.split(' '))

s = "Hey there! what should this string be?"
print('Length of s = %d' % len(s))

print("The first five characters are '%s'" % s[:5])  # Start to 5
print("The next five characters are '%s'" % s[5:10])  # 5 to 10
print("The thirteenth character is '%s'" % s[12])  # Just number 12
print("The characters with odd index are '%s'" % s[1::2])  # (0-based indexing)
print("The last five characters are '%s'" % s[-5:])  # 5th-from-last to end

name = "John"
if name in ["John", "Rick"]:
    print("Your name is either John or Rick.")

statement = True
another_statement = True
if statement == True: print('State True...')
if statement is True:
    print("statement True")
    pass
elif another_statement is True:  # else if
    print('another_statement is True')
    pass
else:
    print('All False...')
    pass

x = [1, 2, 3]
y = [1, 2, 3]
print(x == y)   # match the values of the variables
print(x is y)   # match the instances themselves

print(not False)
print((not False) == False)

primes = [2, 3, 4, 5]
for prime in primes:
    print(prime)

for x in range(5):
    print(x)

for x in range(3, 8, 2):
    print(x)

count = 0
while True:
    print(count)
    count += 1
    if count >= 5:
        break

for x in range(10):
    # Check if x is even
    if x % 2 == 0:
        continue
    print(x)

# sentence = input("Sentence: ")

# screen_width = 80
# text_width = len(sentence)
# box_width = text_width+6
# left_margin = (screen_width - box_width)

# print()
# print(" " * left_margin + "+" + "-" * (box_width - 2) + "+")
# print(" " * left_margin + " |" + " " * text_width + "  |")
# print(" " * left_margin + " | " + sentence + " |")
# print(" " * left_margin + " |" + " " * text_width + "  |")
# print(" " * left_margin + "+" + "-" * (box_width - 2) + "+")
# print()

lstring = list("Hello")
print("LString: ", lstring)
slstring = ''.join(lstring)
print(slstring)

names = ["Alice", "Beth", "Cecil", "Dee-Dee", "Earl"]
del names[2]
print(names)

name = list("Perl")
name[1:] = list('ython')
print(name)

numbers = [1, 5]
numbers[1:1] = [2, 3, 4]
print(numbers)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(numbers[-3:-1])
print(numbers[-3:])
print(numbers[:3])
print(numbers[:])

print(1/2)
print(1//2)
print(1 % 2)
print(2**3)
print(pow(2, 3))
print(100000000000000000000)
print(0xAF)
print(0o11)
print(abs(-10))
print(round(1./3))

print(math.floor(1.9))
print(math.sqrt(9))
# print(math.sqrt(-1))

print(cmath.sqrt(-1))

temp = 42
print("The temperature is " + repr(temp))

print("C:\\nowhere")
print("C:/nowhere" "/hi")
print(r"C:\nowhere")

from string import Template
s = Template("$x, glorious $x!")
print(s.substitute(x='slurm'))
s = Template("It's ${x}tastic!")
print(s.substitute(x='slurm'))
s = Template("Make $$ selling $x!")
print(s.substitute(x='slurm'))

s = Template("A $thing must never $action.")
d = {}
d['thing'] = 'gentleman'
d['action'] = 'show his socks'
print(s.substitute(d))
print(s.safe_substitute(d))

print("%.10f" % math.pi)
print("%.*s" % (5, "Guide van Rossum"))

print("%10.2f" % math.pi)
print("%010.4f" % math.pi)
print("%-10.2f" % math.pi)

# width = int(input("Please enter width: "))

# price_width = 10
# item_width = width - price_width

# header_format = "%-*s%*s"
# format = "%-*s%*.2f"

# print("=" * width)
# print(header_format % (item_width, "Item", price_width, "Price"))
# print("-" * width)
# print(format % (item_width, "Apples", price_width, 0.4))
# print(format % (item_width, "Pears", price_width, 0.5))
# print(format % (item_width, "Cantaloupes", price_width, 1.92))
# print(format % (item_width, "Dried Apricots (16 oz.)", price_width, 8))
# print(format % (item_width, "Prunes (4 lbs.)", price_width, 12))

# print("=" * width)

ststring = "that's all folks"
print(ststring.title())