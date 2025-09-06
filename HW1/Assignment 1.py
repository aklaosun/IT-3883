# Program Name: Assignment1.py
# Course: IT3883/Section W01
# Student Name: Ayomide Laosun
# Assignment Number: 1
# Due Date: 9/5/2025
# Purpose: This program implements a text-based menu that allows the user to append to an input buffer, clear it, display its contents, or exit the program.
# List Specific resources used to complete the assignment:  https://docs.python.org/3/library/functions.html

input_buffer = ""

while True:
    # Display menu options to the user
    print("\n--- Text Buffer Menu ---")
    print("1. Append data to the input buffer")
    print("2. Clear the input buffer")
    print("3. Display the input buffer")
    print("4. Exit the program")

    # Prompt user for a choice
    choice = input("Please enter your choice (1-4): ")

    # Check user's input and perform corresponding action
    if choice == "1":
        # Append user input to the buffer

        user_input = input("Enter the text to append: ")
        input_buffer += user_input  # Concatenate input
        print("Data appended to buffer.")

    elif choice == "2":
        # Clear the buffer by reassigning an empty string
        input_buffer = ""
        print("Buffer cleared.")

    elif choice == "3":
        # Display current content of buffer
        if input_buffer:
            print("Current buffer content:")
            print(input_buffer)
        else:
            print("Buffer is empty.")

    elif choice == "4":
        # Exit the program
        print("Exiting program. The End.")
        break

    else:
        # Invalid input
        print("Invalid choice. Please enter a number between 1 and 4.")