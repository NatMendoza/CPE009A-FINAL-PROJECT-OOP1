while True:
    print("MacroTracker")

    print("1. Add Food")
    print("2. View History")
    print("3. BMI Check")
    print("4. Exit")

    choice = input("> ")

    if choice == "1":
        food = input("Food: ")
        calories = float(input("Calories: "))
        print("Added:", food, calories)

    elif choice == "2":
        print("No history system yet")

    elif choice == "3":
        w = float(input("Weight: "))
        h = float(input("Height: "))
        bmi = w / (h*h)
        print("BMI:", bmi)

    elif choice == "4":
        break
