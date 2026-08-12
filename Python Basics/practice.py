# Variable
'''
name = "Masud"
age = 22
print("Hello", name, "you are", age, "years old")
'''

# List
'''
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("The list of numbers:", numbers)
print("Sum of numbers:", sum(numbers))
print("Average of numbers:", sum(numbers)/len(numbers))
print("Maximum number:", max(numbers))
print("Minimum number:", min(numbers))
print("Length of numbers:", len(numbers))
print("Specific items:", numbers[2], numbers[5], numbers[8])
print("Negative indexing:", numbers[-1], numbers[-2], numbers[-3])
print("Slicing:", numbers[2:5], numbers[5:8], numbers[8:10])
print("Sorted list:", sorted(numbers))
print("Reversed list:", numbers[::-1])
'''

# Dictionary
'''
person = {
    "name": "Masud",
    "age": 25,
    "gender": "Male"
}
# Print Full Dictionary
print("Person Information: ", person)
# Accessing Dictionary Items
print("Person Name:", person["name"])
'''

# Function
'''
def great(name):
    # return "Hello " + name
    return f"Hello {name}"
result = great("Masud")
print(result)
'''

# Function with Type Hunting
'''
def user_info(name: str, age: int, village: str, isStudent: bool = True) -> str:
    return f"Name: {name}, Age: {age}, Village: {village}, Student: {isStudent}"

result = user_info("Masud", 25, "Dhaka")
print(result)
'''

# Loop & List Comprehension
numbers = [1, 2, 3, 4, 5]

# Loop
'''
for num in numbers:
    if num % 2 == 0:
        print(f"{num} is even")
    else:
        print(f"{num} is odd")
'''
'''
squares = []
for num in numbers:
    squares.append(num * 2)
print("Squares:", squares)
'''
'''
even_squares = []
for num in numbers:
    if(num % 2 == 0):
        even_squares.append(num **2)
print("Even Squares:", even_squares)
'''

# List Comprehension
'''
squares = [num * 2 for num in numbers]
print("Squares:", squares)
'''

even_squares = [num ** 2 for num in numbers if num % 2 == 0]
print("Even Squares:", even_squares)

'''
---- Comprehension Formula ----
[expression for item in iterable if condition]


---- Cover ----
1. Variable
2. List
3. Dictionary
4. Function
5. Type Hinting
6. Loop
7. List Comprehension

'''

