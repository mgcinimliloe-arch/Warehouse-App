# School database storage
students = {}  # Key: full name, Value: {'class': class_name}
teachers = {}  # Key: full name, Value: {'subject': subject, 'classes': [class1, class2, ...]}
homeroom_teachers = {}  # Key: full name, Value: {'class': class_name}
class_students = {}  # Key: class_name, Value: list of student full names
class_homeroom = {}  # Key: class_name, Value: homeroom teacher full name


def main_menu():
    print("\nWelcome to the School Database!")
    print("Available commands:")
    print(" - create")
    print(" - manage")
    print(" - end")


def create_user():
    while True:
        print("\nWho would you like to create? (student, teacher, homeroom teacher, end)")
        user_type = input("Enter user type: ").strip().lower()

        if user_type == 'student':
            first = input("Enter student's first name: ").strip()
            last = input("Enter student's last name: ").strip()
            class_name = input("Enter class name (e.g., 3C): ").strip().upper()
            full_name = f"{first} {last}"
            students[full_name] = {'class': class_name}
            class_students.setdefault(class_name, []).append(full_name)
            print(f"Student {full_name} added to class {class_name}.")

        elif user_type == 'teacher':
            first = input("Enter teacher's first name: ").strip()
            last = input("Enter teacher's last name: ").strip()
            subject = input("Enter subject they teach: ").strip()
            print("Enter names of the classes they teach (press Enter on empty line to finish):")
            classes = []
            while True:
                cls = input("Class: ").strip().upper()
                if cls == "":
                    break
                classes.append(cls)
            full_name = f"{first} {last}"
            teachers[full_name] = {'subject': subject, 'classes': classes}
            print(f"Teacher {full_name} added, teaches {subject} to classes {', '.join(classes)}.")

        elif user_type == 'homeroom teacher':
            first = input("Enter homeroom teacher's first name: ").strip()
            last = input("Enter homeroom teacher's last name: ").strip()
            class_name = input("Enter class they lead: ").strip().upper()
            full_name = f"{first} {last}"
            homeroom_teachers[full_name] = {'class': class_name}
            class_homeroom[class_name] = full_name
            print(f"Homeroom teacher {full_name} assigned to class {class_name}.")

        elif user_type == 'end':
            return
        else:
            print("Invalid user type. Please enter student, teacher, homeroom teacher, or end.")


def manage_users():
    while True:
        print("\nWhat would you like to manage? (class, student, teacher, homeroom teacher, end)")
        option = input("Enter option: ").strip().lower()

        if option == 'class':
            class_name = input("Enter class name (e.g., 3C): ").strip().upper()
            print(f"\nClass {class_name}:")
            students_in_class = class_students.get(class_name, [])
            if students_in_class:
                print("Students:")
                for student in students_in_class:
                    print(f" - {student}")
            else:
                print("No students found in this class.")
            homeroom = class_homeroom.get(class_name)
            if homeroom:
                print(f"Homeroom teacher: {homeroom}")
            else:
                print("No homeroom teacher assigned to this class.")

        elif option == 'student':
            first = input("Enter student's first name: ").strip()
            last = input("Enter student's last name: ").strip()
            full_name = f"{first} {last}"
            student_data = students.get(full_name)
            if student_data:
                class_name = student_data['class']
                print(f"\nStudent {full_name} is in class {class_name}.")
                print("Teachers for this class:")
                found = False
                for teacher, data in teachers.items():
                    if class_name in data['classes']:
                        print(f" - {teacher} ({data['subject']})")
                        found = True
                if not found:
                    print("No teachers assigned to this class yet.")
            else:
                print("Student not found.")

        elif option == 'teacher':
            first = input("Enter teacher's first name: ").strip()
            last = input("Enter teacher's last name: ").strip()
            full_name = f"{first} {last}"
            teacher_data = teachers.get(full_name)
            if teacher_data:
                print(f"\nTeacher {full_name} teaches {teacher_data['subject']} to:")
                for cls in teacher_data['classes']:
                    print(f" - {cls}")
            else:
                print("Teacher not found.")

        elif option == 'homeroom teacher':
            first = input("Enter homeroom teacher's first name: ").strip()
            last = input("Enter homeroom teacher's last name: ").strip()
            full_name = f"{first} {last}"
            data = homeroom_teachers.get(full_name)
            if data:
                class_name = data['class']
                print(f"\nHomeroom teacher {full_name} leads class {class_name}.")
                students_in_class = class_students.get(class_name, [])
                if students_in_class:
                    print("Students:")
                    for student in students_in_class:
                        print(f" - {student}")
                else:
                    print("No students found in this class.")
            else:
                print("Homeroom teacher not found.")

        elif option == 'end':
            return
        else:
            print("Invalid option. Please choose from class, student, teacher, homeroom teacher, or end.")


# Main loop
def main():
    while True:
        main_menu()
        command = input("Enter command: ").strip().lower()

        if command == 'create':
            create_user()
        elif command == 'manage':
            manage_users()
        elif command == 'end':
            print("Goodbye!")
            break
        else:
            print("Invalid command. Please enter create, manage, or end.")


if __name__ == "__main__":
    main()
