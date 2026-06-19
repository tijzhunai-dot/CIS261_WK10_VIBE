# Tijzhunai Johnson
# CIS261
# WK10 VIBE Coding - Student Grade Calculator

import os

DATA_FILE = "student_grades.txt"


def load_records(filename):
    records = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    continue
                name, student_id, test1, test2, test3, average, grade = parts
                try:
                    test1 = float(test1)
                    test2 = float(test2)
                    test3 = float(test3)
                    average = float(average)
                except ValueError:
                    continue
                records.append({
                    "name": name,
                    "id": student_id,
                    "test1": test1,
                    "test2": test2,
                    "test3": test3,
                    "average": average,
                    "grade": grade,
                })
    except FileNotFoundError:
        print(f"No existing data file found. Starting with an empty record list.")
    except OSError as error:
        print(f"Error loading records: {error}")
    return records


def save_records(filename, records):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in records:
                file.write(
                    f"{student['name']}|{student['id']}|{student['test1']:.2f}|"
                    f"{student['test2']:.2f}|{student['test3']:.2f}|{student['average']:.2f}|{student['grade']}\n"
                )
        print(f"Saved {len(records)} record(s) to {filename}.")
    except OSError as error:
        print(f"Error saving records: {error}")


def calculate_average(test1, test2, test3):
    return (test1 + test2 + test3) / 3


def determine_letter_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def get_input(prompt, allow_escape=True):
    value = input(prompt).strip()
    if allow_escape and (value.upper() == "ESC" or value == "\x1b"):
        return "ESC"
    return value


def input_float(prompt):
    while True:
        value = get_input(prompt)
        if value == "ESC":
            return value
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid score or type ESC to cancel.")


def add_student(records):
    print("\n" + "=" * 50)
    print("ADD NEW STUDENT")
    print("=" * 50)
    

    name = get_input("Student name: ")
    if name == "ESC":
        return

    student_id = get_input("Student ID: ")
    if student_id == "ESC":
        return

    scores = []
    for label in ["Test 1", "Test 2", "Test 3"]:
        score = input_float(f"{label} score: ")
        if score == "ESC":
            return
        if score < 0 or score > 100:
            print("Score must be between 0 and 100.")
            return
        scores.append(score)

    average = calculate_average(scores[0], scores[1], scores[2])
    grade = determine_letter_grade(average)
    student = {
        "name": name,
        "id": student_id,
        "test1": scores[0],
        "test2": scores[1],
        "test3": scores[2],
        "average": average,
        "grade": grade,
    }
    records.append(student)
    print(f"Student Added:{name} (ID: {student_id}) Average: {average:.2f} | Grade: {grade}")


def display_all_students(students):
    print("\n" + "=" * 50)
    print("ALL STUDENT RECORDS")
    print("=" * 50)
    if not students:
        print("\nNo student records available.")
        return

    print("\nStudent Records")
    header = f"{'Name':<20} {'ID':<12} {'Test1':>6} {'Test2':>6} {'Test3':>6} {'Avg':>7} {'Grade':>6}"
    print(header)
    print("-" * len(header))
    for student in students:
        print(
            f"{student['name']:<20} {student['id']:<12} {student['test1']:.2f} {student['test2']:.2f}"
            f"{student['test3']:.2f} {student['average']:.2f} {student['grade']:>6}"
        )
        print("=" * 50)
        print(f"total students: {len(students)}")

def search_student(students):
    print("\n" + "=" * 50)
    print("SEARCH STUDENT")
    print("=" * 50)
    if not students:
        print("\nNo student records available to search.")
        return

    search_name = get_input("Enter student name to search: ")
    if search_name == "ESC":
        return

    search_name_lower = search_name.lower()
    matches = [student for student in students if search_name_lower in student["name"].lower()]

    if not matches:
        print(f"No student found matching '{search_name}'.")
        return

    print(f"\nFound Student:")
    header = f"{'Name':<20}{'ID':<12} {'Test1':>6}{'Test2':>6} {'Test3':>6} {'Avg':>7} {'Grade':>6}"
    print(header)
    for student in matches:
        print(
            f"{student['name']:<20} {student['id']:<12} {student['test1']:.2f} {student['test2']:.2f}"
            f"{student['test3']:.2f} {student['average']:.2f} {student['grade']:>6}"
        )


def display_statistics(students):
    if not students:
        print("\nNo student records to calculate statistics.")
        return

    averages = [student["average"] for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)
    print("\nClass Statistics")
    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average:  {lowest:.2f}")
    print(f"Class average:   {class_average:.2f}")
    print("Grade distribution:")
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for student in students:
        grade_counts[student["grade"]] += 1
    for grade in ["A", "B", "C", "D", "F"]:
        print(f"  {grade}: {grade_counts[grade]}")

def main_menu():
    students = []
    records = []
    records = load_records(DATA_FILE)
    print("\n" + "=" * 50)
    print("WELCOME TO STUDENT GRADE CALCULATOR")
    print("=" * 50)


    while True:
        print("\n" + "=" * 50)
        print("\nSTUDENT GRADE CALCULATOR")
        print("=" * 50)
        print("1. ADD NEW STUDENT")
        print("2. Display All Students")
        print("3. Search Student by Name")
        print("4. Display Class Statistics")
        print("5. Save and Exit (or press ESC)")
        choice = get_input("Select an option (1-5) or press ESC to exit: ")

        if choice == "1":
            add_student(records)
        elif choice == "2":
            display_all_students(records)
        elif choice == "3":
            search_student(records)
        elif choice == "4":
            display_statistics(records)
        elif choice == "ESC" or choice == "5":
            save_records(DATA_FILE, records)
            print("\n" + "=" * 50)
            print("Thank you for using the Student Grade Calculator!")
            print("Exiting the program. Goodbye.")
            break
        else:
            print("Invalid selection. Please enter a number from 1 to 5 or type ESC.")


if __name__ == "__main__":
    main_menu()
