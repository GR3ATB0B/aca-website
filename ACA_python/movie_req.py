movies = [
    {"title": "Up", "mood": "emotional", "genre": "adventure", "age": "all", "length": "short"},
    {"title": "Soul", "mood": "thoughtful", "genre": "drama", "age": "older", "length": "short"},
    {"title": "Inside Out", "mood": "emotional", "genre": "drama", "age": "all", "length": "short"},
    {"title": "Coco", "mood": "emotional", "genre": "adventure", "age": "all", "length": "short"},
    {"title": "The Incredibles", "mood": "fun", "genre": "action", "age": "all", "length": "long"},
    {"title": "Incredibles 2", "mood": "fun", "genre": "action", "age": "all", "length": "long"},
    {"title": "Finding Nemo", "mood": "fun", "genre": "adventure", "age": "all", "length": "short"},
    {"title": "Finding Dory", "mood": "fun", "genre": "adventure", "age": "all", "length": "short"},
    {"title": "WALL-E", "mood": "thoughtful", "genre": "adventure", "age": "all", "length": "short"},
    {"title": "Ratatouille", "mood": "fun", "genre": "drama", "age": "all", "length": "long"},
    {"title": "Monsters, Inc.", "mood": "fun", "genre": "adventure", "age": "all", "length": "short"},
    {"title": "Toy Story", "mood": "fun", "genre": "adventure", "age": "all", "length": "short"},
    {"title": "Toy Story 3", "mood": "emotional", "genre": "adventure", "age": "all", "length": "short"},
    {"title": "Brave", "mood": "fun", "genre": "action", "age": "all", "length": "short"},
    {"title": "Turning Red", "mood": "fun", "genre": "drama", "age": "older", "length": "short"},
    {"title": "Luca", "mood": "fun", "genre": "adventure", "age": "all", "length": "short"},
]

def ask(question, options):
    print(f"\n{question}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Pick a number from the list.")

print("\n🎬 Pixar Movie Night — let's find you something to watch.\n")

mood = ask("How are you feeling?", ["fun", "emotional", "thoughtful"])
genre = ask("What kind of story?", ["adventure", "action", "drama"])
length = ask("How much time do you have?", ["short (under 2 hrs)", "long (2+ hrs)"])
length = "short" if length.startswith("short") else "long"

matches = [m for m in movies if m["mood"] == mood and m["genre"] == genre and m["length"] == length]

if not matches:
    matches = [m for m in movies if m["mood"] == mood]

if not matches:
    matches = movies

import random
pick = random.choice(matches)

print(f"\n✅ You should watch: {pick['title']}\n")