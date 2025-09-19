# Program Name: Assignment1.py
# Course: IT3883/Section W01
# Student Name: Ayomide Laosun
# Assignment Number: 2
# Due Date: 9/19/2025
# Purpose: This program implements a text-based menu that allows the user to append to an input buffer, clear it, display its contents, or exit the program.
# List Specific resources used to complete the assignment:
# Resources: Python official documentation (docs.python.org)

def read_student_data(filename: str):
    """Read student data from a file and return as list of tuples (name, average)."""
    student_averages = []

    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 7:
                    continue  # skip malformed lines

                name = parts[0]
                try:
                    scores = [float(score) for score in parts[1:]]
                except ValueError:
                    continue  # skip lines with invalid numbers

                average = sum(scores) / len(scores)
                student_averages.append((name, average))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

    return student_averages


def print_sorted_results(student_averages):
    """Print students and averages in descending order by grade."""
    sorted_students = sorted(student_averages, key=lambda x: x[1], reverse=True)

    for name, avg in sorted_students:
        print(f"{name} {avg:.2f}")


def main():
    filename = "Assignment2input.txt"
    student_averages = read_student_data(filename)

    if not student_averages:
        print("No valid student data found.")
        return

    print_sorted_results(student_averages)


if __name__ == "__main__":
    main()