print("hello word")
name = "norang lal"
age = 23
count = 43

print(age)
print(name)
print(type(age))
print(type(name))

b = False
print(type(b))
print(not False)
# print(not True)
name= str(input("Enter Your Name :"))
print("Welcome :",name, len(name))

num = int(input("Enter A Number :"))
if(num % 2 == 0):
    print("This Number Is Even")
else:
    print("This Number is Odd")

a= int(input("Enter first number a :"))
b= int(input("Enter second number b :"))
c= int(input("Enter third number c :"))
d= int(input("Enter fouth number d :"))
if(a>b and a>c and a>d):
        print("a is greatest number")
elif(b>c and b>d):
        print("b is greatest number")
elif(c>d):
    print("c is greatest number")
else:
    print("d is greatest number")
    
movies = ["bahubali","magdhira","kanchna","the nun"]
print(movies)
print(movies[3])
print(len(movies))
tup= ("C","D","A","A","B","B","A")
print(tup.count("B"))

list=["C","D","A","A","B","B","A"]
list.sort()
print(list)
i=100
while i>=1:
   print(i)
   i-=1
n = 1000
i = 1
factorial = 1
for i in range (1, n+1):
    factorial = factorial * i
print("The factorial is :", factorial)

cities = ["delhi","mumbai","kolkata","chennai"]
heroes = ["ironman","thor","hulk","captain america"]

print("Cities List :", cities)
def printlen(list):
    print(len(list))

printlen(cities)
printlen(heroes)
def show(n):
        if(n==0):
            return
        print(n)
        show(n-1)

show(100)   

def calc_sum(a,b):
    sum = a + b
    print("The sum is :", sum)
    return sum

value =calc_sum(5,10)
print(value)