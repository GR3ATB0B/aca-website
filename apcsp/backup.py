# Password Strength Checker
# Checks user-entered passwords against strength criteria
# and outputs a rating for each one.

import string

# -------------------------
# PROCEDURE DEFINITION
# Parameters: passwords (list), min_length (int)
# Uses sequencing, selection, and iteration
# -------------------------
def check_strength(passwords, min_length):
    results = []

    # ITERATION: loop through each password in the list
    for pwd in passwords:
        score = 0

        # SEQUENCING + SELECTION: check each criterion in order

        # Check 1: minimum length
        if len(pwd) >= min_length:
            score += 1

        # Check 2: contains at least one uppercase letter
        if any(c.isupper() for c in pwd):
            score += 1

        # Check 3: contains at least one lowercase letter
        if any(c.islower() for c in pwd):
            score += 1

        # Check 4: contains at least one digit
        if any(c.isdigit() for c in pwd):
            score += 1

        # Check 5: contains at least one special character
        if any(c in string.punctuation for c in pwd):
            score += 1

        # SELECTION: assign rating based on total score
        if score <= 1:
            rating = "Very Weak"
        elif score == 2:
            rating = "Weak"
        elif score == 3:
            rating = "Fair"
        elif score == 4:
            rating = "Strong"
        else:
            rating = "Very Strong"

        results.append((pwd, score, rating))

    return results


# -------------------------
# USER INPUT
# -------------------------
print("=" * 45)
print("       PASSWORD STRENGTH CHECKER")
print("=" * 45)

# Get minimum length preference from user
while True:
    try:
        min_length = int(input("\nEnter your minimum password length: "))
        if min_length > 0:
            break
        else:
            print("Please enter a number greater than 0.")
    except ValueError:
        print("Invalid input. Please enter a whole number.")

# Collect passwords into a list
passwords = []  # LIST to store all user-entered passwords

print("\nEnter passwords to check (type 'done' when finished):")

while True:
    pwd_input = input(f"  Password {len(passwords) + 1}: ")
    if pwd_input.lower() == "done":
        if len(passwords) == 0:
            print("Please enter at least one password.")
        else:
            break
    elif pwd_input == "":
        print("Password cannot be empty.")
    else:
        passwords.append(pwd_input)  # LIST being used: appending each password


# -------------------------
# PROCEDURE CALL
# -------------------------
results = check_strength(passwords, min_length)


# -------------------------
# OUTPUT
# -------------------------
print("\n" + "=" * 45)
print("              RESULTS")
print("=" * 45)
print(f"{'PASSWORD':<20} {'SCORE':<8} {'RATING'}")
print("-" * 45)

# ITERATION: loop through results list to display output
weak_count = 0
strong_count = 0

for pwd, score, rating in results:
    # Mask password for display (show first 2 chars + asterisks)
    masked = pwd[:2] + "*" * (len(pwd) - 2) if len(pwd) > 2 else "**"
    print(f"{masked:<20} {score}/5     {rating}")

    # SELECTION: tally weak vs strong for summary
    if score <= 2:
        weak_count += 1
    else:
        strong_count += 1

print("-" * 45)
print(f"\nTotal passwords checked : {len(passwords)}")
print(f"Strong or better        : {strong_count}")
print(f"Weak or worse           : {weak_count}")
print("\nTip: A strong password uses uppercase, lowercase,")
print("numbers, symbols, and meets your minimum length.")
print("=" * 45)