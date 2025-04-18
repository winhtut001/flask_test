import sqlite3

class Student:
    def __init__(self, no, student_id, name, nickname, major, faculty, mat241_score="N/A"):
        self.no = no
        self.student_id = student_id
        self.name = name
        self.nickname = nickname
        self.major = major
        self.faculty = faculty
        self.mat241_score = mat241_score

    def __str__(self):
        return f"| {self.no:<4} | {self.student_id:<7} | {self.name:<19} | {self.nickname:<10} | {self.major:<14} | {self.faculty:<9} | {self.mat241_score:<7} |"

class StudentManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.students = []

    def initialize_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                no INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE,
                name TEXT,
                nickname TEXT,
                major TEXT,
                faculty TEXT,
                mat241_score TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def load_data(self):
        self.students = []
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY student_id')
        rows = cursor.fetchall()
        for i, row in enumerate(rows, 1):
            self.students.append(Student(
                str(i),      # Use sequential number
                row[1],      # student_id
                row[2],      # name
                row[3],      # nickname
                row[4],      # major
                row[5],      # faculty
                row[6]       # mat241_score
            ))
        conn.close()

    def save_data(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students')
        for student in self.students:
            cursor.execute('''
                INSERT INTO students (student_id, name, nickname, major, faculty, mat241_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                student.student_id,
                student.name,
                student.nickname,
                student.major,
                student.faculty,
                student.mat241_score
            ))
        conn.commit()
        conn.close()

    def add_student(self, student_id, name, nickname, major, faculty, mat241_score="N/A"):
        new_no = str(len(self.students) + 1)
        new_student = Student(new_no, student_id, name, nickname, major, faculty, mat241_score)
        self.students.append(new_student)
        self.save_data()

    def update_student(self, student_id, name, nickname, major, faculty, mat241_score):
        for student in self.students:
            if student.student_id.lower() == student_id.lower():
                student.name = name
                student.nickname = nickname
                student.major = major
                student.faculty = faculty
                student.mat241_score = mat241_score
                self.save_data()
                return

    def delete_student(self, student_id):
        initial_length = len(self.students)
        self.students = [student for student in self.students if student.student_id.lower() != student_id.lower()]
        if len(self.students) < initial_length:
            self.save_data()

    def search_by_name(self, name):
        return [student for student in self.students if name.lower() in student.name.lower()]

    def search_by_id(self, student_id):
        return [student for student in self.students if student_id.lower() in student.student_id.lower()]

    def search_by_major(self, major):
        return [student for student in self.students if major.lower() in student.major.lower()]


def print_header():
    print("-" * 90)
    print("| No  | ID      | Name                 | Nickname   | Major          | Faculty   | MAT241  |")
    print("-" * 90)

# Simple in-memory storage for students
students = []
student_id_counter = 1

def get_all_students():
    return students

def add_student_record(name, age, grade):
    global student_id_counter
    student = {
        'id': student_id_counter,
        'name': name,
        'age': age,
        'grade': grade
    }
    students.append(student)
    student_id_counter += 1
    return student

if __name__ == "__main__":
    manager = StudentManager()
    
    while True:
        print("\n1. Add Student")
        print("2. List Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Search by Name")
        print("6. Search by ID")
        print("7. Search by Major")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            student_id = input("Enter Student ID: ")
            name = input("Enter Name: ")
            nickname = input("Enter Nickname: ")
            major = input("Enter Major: ")
            faculty = input("Enter Faculty: ")
            mat241_score = input("Enter MAT241 Score (or press Enter for N/A): ") or "N/A"
            manager.add_student(student_id, name, nickname, major, faculty, mat241_score)
            print("Student added successfully!")

        elif choice == "2":
            print_header()
            for student in manager.students:
                print(student)
            print("-" * 90)

        elif choice == "3":
            student_id = input("Enter Student ID to update: ")
            results = manager.search_by_id(student_id)
            if results:
                print("Current student information:")
                print_header()
                print(results[0])
                print("-" * 90)
                name = input("Enter new Name: ")
                nickname = input("Enter new Nickname: ")
                major = input("Enter new Major: ")
                faculty = input("Enter new Faculty: ")
                mat241_score = input("Enter new MAT241 Score (or press Enter for N/A): ") or "N/A"
                manager.update_student(student_id, name, nickname, major, faculty, mat241_score)
                print("Student updated successfully!")
            else:
                print("Student not found!")

        elif choice == "4":
            student_id = input("Enter Student ID to delete: ")
            results = manager.search_by_id(student_id)
            if results:
                print("Student to delete:")
                print_header()
                print(results[0])
                print("-" * 90)
                confirm = input("Are you sure you want to delete this student? (y/n): ")
                if confirm.lower() == 'y':
                    manager.delete_student(student_id)
                    print("Student deleted successfully!")
            else:
                print("Student not found!")

        elif choice == "5":
            search_name = input("Enter name to search: ")
            results = manager.search_by_name(search_name)
            if results:
                print_header()
                for student in results:
                    print(student)
                print("-" * 90)
            else:
                print("No students found with that name.")

        elif choice == "6":
            search_id = input("Enter ID to search: ")
            results = manager.search_by_id(search_id)
            if results:
                print_header()
                for student in results:
                    print(student)
                print("-" * 90)
            else:
                print("No students found with that ID.")

        elif choice == "7":
            search_major = input("Enter major to search: ")
            results = manager.search_by_major(search_major)
            if results:
                print_header()
                for student in results:
                    print(student)
                print("-" * 90)
            else:
                print("No students found in that major.")

        elif choice == "8":
            print("Goodbye!")
            break