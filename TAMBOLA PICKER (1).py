import random

def tambola_picker():
    numbers = list(range(1, 91))  # Tambola numbers from 1 to 90
    drawn_numbers = []
    
    while numbers:
        input("Press Enter to draw a number...")
        drawn = random.choice(numbers)
        numbers.remove(drawn)
        drawn_numbers.append(drawn)
        print(f"Number drawn: {drawn}")
        print(f"Numbers drawn so far: {sorted(drawn_numbers)}")
        print(f"Remaining numbers: {len(numbers)}")
    
    print("All numbers have been drawn!")

if __name__ == "__main__":
    tambola_picker()
