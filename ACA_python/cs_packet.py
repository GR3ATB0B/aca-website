print("Which problem would you like to run?")
print("1. Vending Machine")
print("2. Fitness Rep Counter")
print("3. Locker PIN")
print("4. Music Playlist")
print("5. Scrambled Eggs Checker")
print("6. Restaurant Tip Calculator")
print("7. Step Tracker")
print("8. Movie Voting")
print("9. Personal Finance / Budget")
choice = input("Enter a number (1-9): ")

if choice == "1":
    # Problem 1
    balance = 0
    while balance < 150:
        coins = int(input("Insert coins (in cents): "))
        balance = balance + coins
        if balance < 150:
            print("You still need " + str(150 - balance) + " cents.")
    if balance > 150:
        print("Enjoy your snack!")
        print("Change owed: " + str(balance - 150) + " cents.")
    if balance == 150:
        print("Enjoy your snack!")
        print("Change owed: 0")

elif choice == "2":
    # Problem 2
    goal = int(input("How many reps is your goal? "))
    reps = 0
    while reps < goal:
        input("Press enter to log a rep.")
        reps = reps + 1
        print("Reps done: " + str(reps) + "/" + str(goal))
    print("Set complete! Great work.")

elif choice == "3":
    # Problem 3
    correct_pin = "4821"
    guess = ""
    attempts = 0
    while attempts < 3 and guess != correct_pin:
        guess = input("Enter PIN: ")
        if guess != correct_pin:
            attempts = attempts + 1
            print("Incorrect. You have " + str(3 - attempts) + " attempt(s) remaining.")
    if guess == correct_pin:
        print("Access granted.")
    else:
        print("Account locked. Too many failed attempts.")

elif choice == "4":
    # Problem 4
    songs = []
    answer = ""
    while answer.lower() != "done":
        answer = input("Add a song (or type 'done' to finish): ")
        if answer.lower() != "done":
            songs.append(answer)
    if len(songs) == 0:
        print("No songs added.")
    else:
        for i in range(len(songs)):
            print(str(i + 1) + ". " + songs[i])

elif choice == "5":
    # Problem 5
    fridge = []
    ingredient = ""
    while ingredient.lower() != "done":
        ingredient = input("Enter an ingredient (or 'done' to finish): ")
        if ingredient.lower() != "done":
            fridge.append(ingredient.lower())
    needed = ["eggs", "butter", "milk"]
    for item in needed:
        if item in fridge:
            print(item + " ... HAVE IT")
        else:
            print(item + " ... MISSING")
    if "eggs" in fridge and "butter" in fridge and "milk" in fridge:
        print("You can make scrambled eggs!")
    else:
        print("You are missing ingredients.")

elif choice == "6":
    # Problem 6
    prices = []
    price = 0
    while price != -1:
        price = float(input("Enter a meal price (or -1 to finish): "))
        if price != -1:
            prices.append(price)
    total = 0
    for p in prices:
        total = total + p
    print("Table total: $" + str(round(total, 2)))
    tip_rates = [0.10, 0.15, 0.18, 0.20]
    for rate in tip_rates:
        tip = total * rate
        final = total + tip
        print(str(int(rate * 100)) + "% tip: $" + str(round(tip, 2)) + " tip  ->  $" + str(round(final, 2)) + " total")

elif choice == "7":
    # Problem 7
    steps = []
    while len(steps) < 7:
        count = int(input("Enter steps for day " + str(len(steps) + 1) + ": "))
        steps.append(count)
    best = steps[0]
    best_day = 0
    for i in range(len(steps)):
        if steps[i] > best:
            best = steps[i]
            best_day = i
    for i in range(7):
        day_num = i + 1
        step_count = steps[i]
        if step_count >= 10000:
            print("Day " + str(day_num) + ": " + str(step_count) + " steps  --  Goal met!")
        else:
            diff = 10000 - step_count
            print("Day " + str(day_num) + ": " + str(step_count) + " steps  --  " + str(diff) + " steps short")
    print("Best day: Day " + str(best_day + 1) + " with " + str(best) + " steps.")

elif choice == "8":
    # Problem 8
    movies = ["Inception", "Clueless", "Parasite", "Get Out"]
    votes = [0, 0, 0, 0]
    for i in range(4):
        print(str(i + 1) + ". " + movies[i])
    answer = 1
    while answer != 0:
        answer = int(input("Enter a number 1-4 to vote, or 0 to close voting: "))
        if answer == 0:
            break
        if answer == 1 or answer == 2 or answer == 3 or answer == 4:
            votes[answer - 1] = votes[answer - 1] + 1
        else:
            print("Invalid choice.")
    for i in range(4):
        print(movies[i] + ": " + str(votes[i]) + " vote" + ("s" if votes[i] != 1 else ""))
    highest = votes[0]
    for v in votes:
        if v > highest:
            highest = v
    top = []
    for i in range(4):
        if votes[i] == highest:
            top.append(movies[i])
    if len(top) == 1:
        print("Winner: " + top[0])
    else:
        print("It's a tie!")

elif choice == "9":
    # Problem 9
    budget = float(input("What is your total budget? $"))
    limit = float(input("What is your per-item spending limit? $"))
    names = []
    costs = []
    item_name = ""
    while item_name.lower() != "done":
        item_name = input("Item name (or 'done' to finish): ")
        if item_name.lower() != "done":
            item_cost = float(input("Cost of that item: $"))
            names.append(item_name)
            costs.append(item_cost)
    total = 0
    for c in costs:
        total = total + c
    for i in range(len(names)):
        pct = round((costs[i] / total) * 100, 1)
        print(str(i + 1) + ". " + names[i] + " - $" + str(round(costs[i], 2)) + " (" + str(pct) + "% of total)")
        if costs[i] > limit:
            print("  ^ This item exceeded your per-item limit.")
    if total > budget:
        over = round(total - budget, 2)
        print("Over budget by $" + str(over) + ".")
    else:
        remaining = round(budget - total, 2)
        print("Under budget, $" + str(remaining) + " remaining.")

else:
    print("Invalid choice.")