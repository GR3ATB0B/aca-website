def welcome():
    age = input("What is your age? ")
    name = input("What is your name? ") 
    major = input("What is your major? ")
    return age, name, major

def names():
    namelist = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown"]
    name_a = []
    for name in namelist:
        if name.startswith("A"):
            name_a.append(name)
    return name_a
    
def grade_avgs():
    sam = [90, 85, 92]
    william = [78, 82, 88]
    bob = [85, 90, 80]
    alice = [92, 95, 88]
    all_grades = [sam, william, bob, alice]
    all_avg = []
    for grades in all_grades:
        avg = sum(grades) / len(grades)
        all_avg.append(avg)
        for avg in all_avg:
            sum(avg) / len(avg)
            big_avg =+ avg

    return all_avg


age, name, major = welcome()
print (f"Hello {name}, you are {age} years old and your major is {major}. Welcome to UC!")
name_a = names()
print(f"Names that start with 'A': {name_a}")
avg = grade_avgs()
print(f"Grade averages calculated for all students is {all_avg}.")