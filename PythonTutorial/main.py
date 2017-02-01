"""
 (this is my simple docstring)

 Python 3.4 Programming Tutorials
 56 videos by thenewboston on YouTube
 https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAcbMi1sH6oAMk4JHw91mC_

 Paul A. Beata
 Started first video in mid-Decemeber 2016
 Completed all videos on 12/31/2016

 Future Goals:
 1. Address all the warnings in the PyCharm IDE
 2. Move all the import and from statements to the front
 3. Practice (first learn) how to move classes and functions to separate files

"""

print("\nLesson 1 -- installing Python")

# open the Python IDLE (the Python shell)
print(3 + 4)

print("\nLesson 2 -- numbers")

# numbers
print("numbers")
print(3 * 20)
print(12 / 4)
print(8 + 2 * 10)
print((8 + 2) * 10)
print(18 / 4)
print(18 // 4)  # rounds the result down to nearest whole number
print(18 % 4)   # gives remainder using the modulus funtions
print(5 * 5 * 5)
print(5 ** 3)   # "5 to the power of 3"

# variables
print("variables")
myVal = 2
print(20 + myVal)
yourVal = 18
print(myVal + yourVal)

print("\nLesson 3 - strings")
# double vs single quotes
print("This is one example's string.")
# escaping a character
print('he says, "why do you use Python?"')
print('where\'d you come from?')
# use the raw strings for file paths! notice the "r"
print(r'C:\home\PaulA\PyCharm\newFolder')
firstName = "Paul"
print(firstName + "Beata")
print(firstName + "won")
print(firstName * 4)

print("\nLesson 4 -- slicing up strings")

myName = "Paul A. Beata"
print(myName[:])
print(myName[0])
print(myName[5])
print(myName[-1])
print(myName[-3])
print(myName[2:6])
print(myName[:6])
# get length of a string
print(len("aldfkalsfnasldn"))
print(len(myName))

print("\nLesson 5 -- lists")

players = [29, 58, 66, 71, 87]
print(players)
print(players[2])
players[2] = 68
print(players[2])
print(players + [90, 91, 98])
new_players = players + [90, 91, 98]
print(new_players)
players.append(1)
print(players)
print(players[:2])
players[:2] = [20, 30]
print(players)
players[:2] = []
print(players)
# clear out your list of players
players[:] = []
print(players)

print("\nLesson 6 -- installing PyCharm")

print("hello world! pycharm works hooray")

print("\nLesson 7 -- if elif else")

age = 13

if age < 21:
    print("no beer for you!")

name = "Lucia"

if name is "Lucy":
    print("Hi Lucy!")
elif name is "Lucia":
    print("Hi Lucias!")
elif name is "Paul":
    print("Hi Master!")
else:
    print("Hello guest, please sign up!")

print("\nLesson 8 -- for")

foods = ['bacon', 'beef', 'tuna', 'ham', 'beer']

for f in foods:
    print(f)
    print(len(f))

# loop through only a portion of the list
for f in foods[:2]:
    print(f)
    print(len(f))

print("\nLesson 9 -- range and while")

for x in range(10):
    print("paul is looping")

for y in range(5, 12):
    print(y)

for z in range(10, 40, 5):
    print(z)

print("while loop")
check = 5
while check < 10:
    print(check)
    check += 1

print("\nLesson 10 " + "-- comments and break")
print(10, "Paul", 10)
magicNo = 26
# this program finds a magic number
'''
this is a comment block
'''
for n in range(101):
    if n is magicNo:
        print(n, "is the magic number!")
        break
    else:
        print(n)

maxVal = 101
denom = 4

for i in range(maxVal):
    r = i % denom
    if r is 0:
        print(i, "is a multiple of", denom, "and", i / denom)

print("\nLesson 11 -- continue")

numbersTaken = [2, 5, 12, 13, 17]
print("Here are the numbers that are still available:")

for n in range(1, 20):
    if n in numbersTaken:
        continue
    print(n)


print(" ")
print("Lesson 12 -- functions")


def my_func():
    print("called the function")

my_func()
my_func()
my_func()


def bitcoin_to_usd(btc):
    amount = btc * 527
    print(btc, "bitcoin in usd is", amount)

my_func()
bitcoin_to_usd(3.85)
bitcoin_to_usd(1.20)

print("\nLesson 13 -- return values")


def allowed_dating_age(my_age):
    girls_age = (my_age / 2) + 7
    return girls_age

age_limit = allowed_dating_age(27)
print("the allowed age is", age_limit)
age_limit = allowed_dating_age(49)
print("the allowed age is", age_limit)

for age in range(15, 61):
    print(age, "is allowed to date", allowed_dating_age(age))


print("\nLesson 14 -- default values for arguments")


def get_gender(sex='unknown'):
    if sex is 'm':
        sex = "male"
    elif sex is 'f':
        sex = "female"
    print(sex)

get_gender('m')
get_gender('f')
get_gender()


print("\nLesson 15 -- variable scope")
a = 7823


def fun1():
    a = 223
    print(a)


def fun2():
    print(a)

fun1()
fun2()


print("\nLesson 16 -- keyword arguments")


def sentence(name="paul", action="ate", item="pizza"):
    print(name, action, item)

sentence()
sentence("Lucia", "was", "happy")
sentence(item="mad")
sentence(item="turkey")


print("\nLesson 17 -- flexible number of arguments")


def add_numbers(*args):
    total = 0
    for a in args:
        total += a
    print(total)

add_numbers(3)
add_numbers(3, 32)
add_numbers(3, 43, 543, 44, 2323)


print("")
print("Lesson 18 -- unpacking arguments")

def health_calculator(age, apples, cigs):
    answer = (100 - age) + (apples * 3.5) - (cigs * 2)
    print("health computed as", answer)

paul_data = [27, 20, 0]
health_calculator(paul_data[0], paul_data[1], paul_data[2])
health_calculator(*paul_data)


print("")
print("Lesson 19 -- Walmart and sets")

# sets can't have duplicates like lists do!

groceries = {'cereal', 'milk', 'beer', 'starcrunch', 'lotion', 'beer', 'tape'}
print(groceries)

if 'milk' in groceries:
    print("you already have milk!")
else:
    print("you need milk!")


print("")
print("Lesson 20 -- dictionary")

classmates = {'Paul': ' goes to UF', 'Lucia': ' wants to be Dr', 'Jason': ' studies hard'}
print(classmates)
print(classmates['Jason'])

for k, v in classmates.items():
    print(k + v)


print("")
print("Lesson 21 -- modules")

import test_func
import random

test_func.my_program()
x = random.randrange(1, 1000)
print(x)


print("")
print("Lesson 22 -- download an image from the web")

import urllib.request

def download_web_image(url):
    name = random.randrange(1, 1000)
    full_name = str(name) + ".jpg"
    urllib.request.urlretrieve(url, full_name)

download_web_image("http://www.rotoworld.com/images/photos/NFL/GB/NFL_Rodgers5_300.jpg")
print("imaged downloaded!")

print("")
print("Lesson 23 -- how to read and write files")

fw = open('sample.txt', 'w')
fw.write('hello world to a file...\n')
fw.write('...and this is line #2\n')
fw.close()

fr = open('sample.txt', 'r')
text = fr.read()
print(text)
fr.close()


print("")
print("Lesson 24 -- downloading files from the web")

# another way to import a module:
from urllib import request

goog_url = 'http://chart.finance.yahoo.com/table.csv?s=GOOG&a=10&b=29&c=2016&d=11&e=29&f=2016&g=d&ignore=.csv'

def download_stock_data(csv_url):
    response = request.urlopen(csv_url)
    # read the data from the url you are pointing to; all text stored in variable csv:
    csv = response.read()
    csv_str = str(csv)
    lines = csv_str.split("\\n")
    # use 'r' (for raw) before a file pass in order to provide an address here
    dest_url = r'goog.csv'
    fx = open(dest_url, 'w')
    for line in lines:
        fx.write(line + "\n")
    fx .close()

download_stock_data(goog_url)
print("GOOG stock data downloaded!")




# CREATE A SIMPLE WEB CRAWLER

print("")
print("Lesson 25/26/27 -- how to build a simple web crawler")

import requests
from bs4 import BeautifulSoup

def trade_spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'https://thenewboston.com/search.php?type=1&sort=pop&page=' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        # ORIGINAL: soup = BeautifulSoup(plain_text)
        soup = BeautifulSoup(plain_text, "html.parser")
        for link in soup.findAll('a', {'class': 'user-name'}):
            href = 'https://thenewboston.com/' + link.get('href')
            title = link.string
            # print(href)
            # print(title)
            get_single_item_data(href)
        page += 1

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for item_name in soup.findAll('h1', {'class': 'no-margin inline'}):
        print(item_name.string)
    for link in soup.findAll('a'):
        href = 'https://thenewboston.com/' + link.get('href')
        print(href)

# COMMENTED OUT THE TRADE SPIDER SO THAT IT DOESN'T SLOW DOWN PROGRAM
# trade_spider(1)


print("")
print("Lesson 28 -- you are the only exception")
# syntax error vs an exception (like ValueError: entering a string when expecting an int)

'''
# COMMENTED THIS BLOCK OUT BECAUSE IT CAUSES POTENTIALLY UNREACHABLE CODE

yourInput = int(input("what's your favorite number?\n"))
print(yourInput)

while True:
    try:
        number = int(input("what's your favorite number? please enter a number only \n"))
        print(100/number)
        print("you entered the number", number)
        break
    except ValueError:
        print("***make sure you enter a number only")
    except ZeroDivisionError:
        print("***don't enter zero please")
    except:
        break
        # this is NOT recommended 99% of the time
    finally:
        # execute this code NO MATTER WHAT using finally
        print("input loop complete")
'''


# HALF-WAY POINT OF THE LESSONS!


print("")
print("Lesson 29 -- classes and objects")


class Enemy:
    life = 3

    def attack(self):
        print("ouch!")
        self.life -= 1

    def checkLife(self):
        if self.life <= 0:
            print("I am dead")
        else:
            print("I have", str(self.life), "life left!")

# create an Enemy object to test this
enemy1 = Enemy()
enemy2 = Enemy()

enemy1.attack()
enemy1.attack()

enemy1.checkLife()
enemy2.checkLife()


print("")
print("Lesson 30 -- init")


class Test:

    def __init__(self):
        print("***Test Initialized***")

    def check(self):
        print("I am running the test.")

math = Test()
math.check()


class Warrior:

    def __init__(self, x):
        self.energy = x

    def get_energy(self):
        print(self.energy)

sith = Warrior(20)
stormtrooper = Warrior(2)

sith.get_energy()
stormtrooper.get_energy()


print("")
print("Lesson 31 -- class vs instance variable")


class Girl:
    gender = 'female'
    # every Girl object will have the gender of female

    def __init__(self, name):
        self.name = name
        # the name is unique to each object

L = Girl("Lucia")
R = Girl("Rachel")
print(L.gender)
print(R.gender)
print(L.name)
print(R.name)


print("")
print("Lesson 32 -- inheritance")


class Parent:

    def print_last_name(self):
        print("Beata")

# in the parentheses, put the class that you want to inherit from!
class Child(Parent):

    def __init__(self, inName):
        self.name = inName

    def print_first_name(self):
        print(self.name)

    def print_last_name(self):
        print("BATMAN")
        # this overrides the inherited last name!

p = Child("Paul")
p.print_first_name()
p.print_last_name()


print("")
print("Lesson 33 -- multiple inheritance")


class Mario():
    def move(self):
        print("I am moving!")

class Shroom():
    def eat_shroom(self):
        print("Now I am big!")

# inherit from the two classes above
# (this way we don't have to re-write all those functions)
class BigMario(Mario, Shroom):
    pass

bm = BigMario()
bm.move()
bm.eat_shroom()


print("")
print("Lesson 34 -- threading")


# what is a thread? why are they useful?
# it is good for messaging
import threading

class MyMessenger(threading.Thread):
    def run(self):
        # we must have this special method for threads
        for _ in range(10):
            # use the _ in place of a variable like i if you don't need it
            print(threading.current_thread().getName())
            # we can give every thread a name

# can now allow multiple objects to run simultaneously
T1 = MyMessenger(name="sender")
T2 = MyMessenger(name="recver")
T1.start()
T2.start()


print("")
print("Lesson 35/36/37 -- word frequency counter")


import requests
from bs4 import BeautifulSoup
import operator

def start(url):
    word_list = []
    # connect to the url and use it as just plain TEXT
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, "html.parser")
    for post_text in soup.findAll('a', {'class': 'user-name'}):
        content = post_text.string
        words = content.lower().split()
        for each_word in words:
            # print(each_word)
            word_list.append(each_word)
    clean_up_list(word_list)

def clean_up_list(word_list):
    clean_word_list = []
    for word in word_list:
        # treat each word in list as an individual word variable
        symbols = "!@#$%^&*_+|:\"<>{}[]()?~,./;'\-=`'"
        for j in range(0, len(symbols)):
            word = word.replace(symbols[j], "")
        if len(word) > 0:
            print(word)
            clean_word_list.append(word)
    create_dictionary(clean_word_list)

def create_dictionary(clean_word_list):
    word_count = {}
    for word in clean_word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    for key, value in sorted(word_count.items(), key=operator.itemgetter(1)):
        print(key, value)

start('https://thenewboston.com/search.php?type=1&sort=pop&page=3')


print("")
print("Lesson 38 -- unpack lists or tuples")


date, name, price = ['December 30, 2016', 'Beard Wax', 8.25]
print(name)

# now what if you have lists that you want to unpack to variables but they are different sizes
# (check out Python Cookbook for cool scripts)
def drop_first_and_last(grades):
    # grades will be our input list
    first, *middle, last = grades
    avg = sum(middle) / len(middle)
    print(avg)

drop_first_and_last([65, 76, 98, 54, 21])
drop_first_and_last([65, 76, 98, 54, 21, 54, 65, 99, 88, 78])


print("")
print("Lesson 39 -- zip")


firstNames = ['Paul', 'Lucia', 'Mayra']
lastNames = ['Beata', 'Reyes', 'Reyes']

fullNames = zip(firstNames, lastNames)
for a, b in fullNames:
    print(a, b)


print("")
print("Lesson 40 -- lambda")


# a lambda "function" has no "name"
answer = lambda a: a*7
print(answer(7))
# it is a small, quick, nameless function
# when would we ever use these? (see his button examples in Tkinter tutorials)


print("")
print("Lesson 41 -- min, max, and sorting dictionaries")


# this is a dictionary for our example (not sorted or anything)
stocks = {
    'GOOG': 520.54,
    'FB': 76.45,
    'YHOO': 39.28,
    'AMZN': 306.21,
    'AAPL': 99.76
}

# the one you pass in first will be what it is sorted by (key or value)
print(min(zip(stocks.values(), stocks.keys())))
print(max(zip(stocks.values(), stocks.keys())))
print(sorted(zip(stocks.values(), stocks.keys())))
print(sorted(zip(stocks.keys(), stocks.values())))

print("\nLesson 42 -- pillow")
# teased some photo manipulation functionality available in Python
from PIL import Image
# in 3.4 Pillow
# in 2.7 PIL
img = Image.open("bird.JPG")
print(img.size)
print(img.format)
# img.show()

print("\nLesson 43 -- cropping images")
# from PIL import Image
myImg = Image.open("draxx.JPG")
print(myImg.size)
area = (100, 100, 200, 300)
cropped_img = myImg.crop(area)
# myImg.show()
# cropped_img.show()

print("\nLesson 44 -- combining images")
# from PIL import Image
bird = Image.open("bird.JPG")
draxx = Image.open("draxx.JPG")
pasteArea = (0, 0, 572, 256)
draxx.paste(bird, pasteArea)
# draxx.show()

print("\nLesson 45 -- getting individual channels")
# think of an image being a combination of red, green, and blue values separated into different channels
print(draxx.mode)
# mode should be RGB for typical images in your computer
R, G, B = draxx.split()
# this function returns a tuple which we saved as three channels (one for each primary color
# R.show()
# G.show()
# B.show()

print("\nLesson 46 -- merge effect")
# takes three individual channels that are merged into one image
new_img = Image.merge("RGB", (R, G, B))
# image mode was the first input
# new_img.show()
new_img2 = Image.merge("RGB", (B, G, R))
# new_img2.show()
'''
r1, g1, b1 = draxx.split()
r2, g2, b2 = bird.split()
new_img3 = Image.merge("RGB", (R, g2, B))
new_img3.show()
ERROR ON THIS LINE
Traceback (most recent call last):
  File "C:/Users/PaulA/PycharmProjects/YouTube/main.py", line 643, in <module>
    new_img3 = Image.merge("RGB", (R, g2, B))
  File r"C:Users\PaulA\AppData\Local\Programs\Python\Python35-32\lib\site-packages\PIL\Image.py", line 2414, in merge
    raise ValueError("size mismatch")
ValueError: size mismatch
'''

print("\nLesson 47 -- basic transformations")
bird = Image.open("bird.JPG")
square_bird = bird.resize((200,200))
flip_bird = bird.transpose(Image.FLIP_LEFT_RIGHT)
spin_bird = bird.transpose(Image.ROTATE_90)
# bird.show()
# square_bird.show()
# flip_bird.show()
# spin_bird.show()

print("\nLesson 48 -- modes and filters")
# most images are in RGB mode
# but sometimes you need another format (like when printing)
bird = Image.open("bird.JPG")
black_white = bird.convert("L")
# the L stands for luminent (i.e., B&W)
# black_white.show()
# print(black_white.mode)
from PIL import ImageFilter
draxx = Image.open("draxx.JPG")
blur = draxx.filter(ImageFilter.BLUR)
detail = draxx.filter(ImageFilter.DETAIL)
edges = draxx.filter(ImageFilter.FIND_EDGES)
# detail.show()
# edges.show()

print("\nLesson 49 -- struct")
# a way to take a type of data in Python and convert it to bytes
from struct import *
# store as bytes data; store 2 ints and 1 float
# pack(format, values)
packed_data = pack('iif', 6, 19, 4.73)
print(packed_data)
print(calcsize('i'))
print(calcsize('f'))
print(calcsize('iif'))
# how to convert back to normal data?
original_data = unpack('iif', packed_data)
print(original_data)
print(unpack('iif', b'\x06\x00\x00\x00\x13\x00\x00\x00)\\\x97@'))

print("\nLesson 50 -- map")
income = [10, 30, 75]


def double_money(dollars):
    return dollars * 2

new_income = list(map(double_money, income))
print(new_income)

print("\nLesson 51 -- bitwise operators")
# recommends watching his networking videos

# ---- Binary AND -----
a = 50          # 110010
b = 25          # 011001
c = a & b       # 010000
print(c)

# ---- Binary RIGHT SHIFT ----
x = 240         # 11110000
y = x >> 2      # 00111100
print(y)

# ---- Binary LEFT SHIFT ----
z = x << 2
print(z)

print("\nLesson 52 -- finding largest or smallest items")

import heapq

grades = [32, 43, 654, 34, 132, 66, 99, 532]
print(heapq.nlargest(3, grades))

new_stocks = [
    {'ticker': 'AAPL', 'price': 201},
    {'ticker': 'GOOG', 'price': 800},
    {'ticker': 'F', 'price': 54},
    {'ticker': 'MSFT', 'price': 313},
    {'ticker': 'TUNA', 'price': 68}
]

print(heapq.nsmallest(2, new_stocks, key=lambda stock: stock['price']))

print("\nLesson 53 -- dictionary calculations")

my_stocks = {
    'GOOG': 434,
    'AAPL': 325,
    'FB': 54,
    'AMZN': 623,
    'F': 32,
    'MSFT': 549
}

# this is wrong: it will return AAPL because it is sorting by the keys!
print(min(my_stocks))

# what we want to do is get:  (434, GOOG) (325, AAPL)
min_price = min(zip(my_stocks.values(), my_stocks.keys()))
print(min_price)

print("\nLesson 54 -- find most frequent items")

from collections import Counter

text = "We hope to one day become the world's leader in free, educational resources. We are constantly" \
       "discovering and adding more free content to the website everyday.  There is already an enormous " \
       "amount of resources online that can be accessed for free by anyone in the world, the main issue " \
       "right now is that very little of it is organized or structured in any way. We want to be the " \
       "solution to that problem."

# this will break a string into a list of words!
words = text.split()
# print(words)

counter = Counter(words)
# give the three most counted words in the list
top_three = counter.most_common(3)
print(top_three)

print("\nLesson 55 -- dictionary multiple key sort")

from operator import itemgetter

users = [
    {'fname': 'Paul', 'lname': 'Beata'},
    {'fname': 'Gianna', 'lname': 'Beata'},
    {'fname': 'PaulG', 'lname': 'Beata'},
    {'fname': 'Michelle', 'lname': 'Beata'},
    {'fname': 'Lucia', 'lname': 'Reyes'},
    {'fname': 'Mayra', 'lname': 'Reyes'},
    {'fname': 'Dario', 'lname': 'Reyes'},
    {'fname': 'LuciaH', 'lname': 'Reyes'},
]

# does not sort in TRUE alphabetical order
for x in sorted(users, key=itemgetter('fname')):
    print(x)

print('\n--- fixed fully sorted! ---')
for x in sorted(users, key=(itemgetter('fname', 'lname'))):
    print(x)

print('\n--- sort by lname ---')
for x in sorted(users, key=(itemgetter('lname', 'fname'))):
    print(x)

print("\nLesson 56 -- sorting custom objects")

from operator import attrgetter


class User:

    def __init__(self, x, y):
        self.name = x
        self.user_id = y

    # use this to print out an instance! format just one time
    def __repr__(self):
        return self.name + ":" + str(self.user_id)

new_users = [
    User('Paul', 1),
    User('Jason', 23),
    User('Ning', 11),
    User('Lucia', 99),
    User('Andy', 55),
    User('Juan', 43),
    User('Mayra', 13),
    User('Cassian', 9),
]

for user in new_users:
    print(user)

print('----')
# specify how to sort your data!
for user in sorted(new_users, key=attrgetter('name')):
    print(user)

print('----')
# specify how to sort your data!
for user in sorted(new_users, key=attrgetter('user_id')):
    print(user)  # prints out the data in order by user_id

print("\n\n ~ ~ CONGRATS YOU COMPLETED THENEWBOSTON PYTHON TUTORIAL ON YOUTUBE! ~ ~ \n")
