
# from worksheet done on friday feb 13th 2026 
# basic python exercises
# expected output included at bottom of file in triple quotes


#1
print("hello, world!")

#2
age = 25
print(age)

#3
first_name = "Nash"
last_name = "Vogeltanz"
print(first_name)
print(last_name)

#4
x = 10
y = 5
print (x + y)

#5
print (x * y)
print (x / y)

#6
temp = 72
if temp > 65:
    print(temp, "is greater than 65")

#7
a = 8
b = 12
if a < b:
    print(a, "is less than", b)
if b == a:
    print(b, "is equal to", a)

#8
score = 85
if score >= 90:
    print(score,"is greater than or equal to 90")

#9
is_raining = True
if is_raining:
    print("It's raining outside!")

#10
has_ticket = True
has_id = False
if has_ticket and has_id:
    print("You can enter the event.")

#11
if has_ticket or has_id:
    print("You might be able to enter the event.")

#12        
is_closed = True
print(not is_closed)

#13
name = "Alice"
age = 30
print(name, "is", age, "years old.")

#14
print(f"{name} is {age} years old.")

#15
price = 19.99
quantity = 3
total = price * quantity
print(f"Total cost is {total}")

#16
radius = 5
area = 3.14 * radius ** 2
print(f"Area of the circle is {area}")

#17
celsius = 25
fahrenheit = (celsius * 9/5) + 32
print(f"{celsius}°C is {fahrenheit}°F")

#18
a = 15
b = 4
c = 2
result = a + b * c
print(f"The result of a + b * c is {result}")

#19
result = (a + b) * c
print(f"The result of (a + b) * c is {result}")

#20
is_weekend = True
is_sunny = True
if is_weekend and is_sunny:
    print("It's a great day for the beach!")

#21
age = 16   
has_license = True
if age >= 16 and has_license:
    print("You can drive a car.")

#22
hour = 14
if hour < 12:
    print("Good morning!")
elif 12 <= hour < 18:
    print("Good afternoon!")
else:
    print("Good evening!")  

#23
password = "secure123"
confirm_password = "secure123"
if password == confirm_password and len(password) >= 8:
    print("Password is valid.")

#24
x = 7
y = 14
z = 21
if x % y == 0 and x % z == 0:
    print(f"{x} is divisible by {y} and {z}")

#25
name = "Jordan"
greade = 88
is_passing = greade >= 60
improvement = 12
print(f"{name} scored {greade} (passing = {is_passing}) with improvement of {improvement} points")

"""""

# Expected Output:

hello, world!
25
Nash
Vogeltanz
15
50
2.0
72 is greater than 65
8 is less than 12
It's raining outside!
You might be able to enter the event.
False
Alice is 30 years old.
Alice is 30 years old.
Total cost is 59.97
Area of the circle is 78.5
25°C is 77.0°F
The result of a + b * c is 23
The result of (a + b) * c is 38
It's a great day for the beach!
You can drive a car.
Good afternoon!
Password is valid.
Jordan scored 88 (passing = True) with improvement of 12 points
"""""
