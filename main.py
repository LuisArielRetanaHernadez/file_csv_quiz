import os
import pandas as pd
from tabulate import tabulate
from itertools import chain

#! @Decoracts {error_handle} func: handle of errors 

def error_handle(func):
    def process_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as er:
            print(f"data of error: {func.__name__,}: {er}")
        except TypeError as err:
            print(f"type err: {func.__name__} --> {err}")
            raise
    return process_error

class FileCsv:
    
    all_csv = []

    #? @Params directory str: contains the directory where to host the files 

    @error_handle
    def __init__(self, directory:str = "") -> None:
        self.directory = directory    
    #? @Params {file_name} str: names of the files of directory (params optional)

    @error_handle
    def open_files(self) -> list:
        with os.scandir(self.directory) as entries:
            for entry in entries:
                if file_name == entry.name:
                    file = pd.read_csv(entry)
                    self.all_csv.append(file)
                    continue
                    
                file = pd.read_csv(entry)
                self.all_csv.append(file)

        return self.all_csv


class Student(FileCsv):

    #? @Attribute {list_student}: contains the list of student without redundances de names 
    #? @Attribute {higher_percentage}: contains the list of student with Accuracy more at value given 

    list_students = []
    higher_percentage = [[]];
    
    def __init__(self, directory:str = "") -> None:
        super().__init__(directory)
 
    def new_list_student(self) -> None:
        for name in self.all_csv:
           name_not_na = name["Last Name"].fillna("", inplace=False)
           names_completed = name["First Name"] + name_not_na 

           for name_student in names_completed:
                in_name = name_student not in chain.from_iterable(self.list_students)
                  
                if in_name:
                    student = [name_student, 0]
                    self.list_students.append(student)

    #? @Params { percentage }: the percentage of Accuracy to condation the student which has that percentage  or more
    @error_handle
    def major_successes(self, percentage:int = 70) -> list:
        n = 0
        for file_csv in self.all_csv:
            i = 0
            while i < len(file_csv):

                name_student = f"{file_csv['First Name'][i]} {file_csv['Last Name'][i]}"

                accuracy = file_csv["Accuracy"][i].replace("%", "")

                if int(accuracy) >= int(percentage):
                    self.higher_percentage[n].append([name_student, accuracy, n+1])
                i += 1
            self.higher_percentage.append([])
            n += 1
        return tabulate(self.higher_percentage[0], headers=["Name", "Accuracy", "No. Quiz"])

    #? @Params {amount}: the amount of winner to books 
    @error_handle
    def winner_quiz(self, amount:int = 2) -> list:
        
        for row_file in self.all_csv:
            row_file["Last Name"].fillna("", inplace=True)

            n = 0
            i = 0
            c = 0
            while n < len(self.list_students):
                name_student = row_file["First Name"][i] + row_file["Last Name"][i]
                in_name = name_student not in chain.from_iterable(self.list_students)
                
                if in_name:
                    if i == len(row_file) or len(row_file) == 1: break
                    i += 1
                if name_student == self.list_students[n][0]: 
                    self.list_students[n][1] += row_file["Score"][i] 
                    c += 1
                    if c == len(row_file):
                        break
                    n = 0
                    i += 1
                    continue

                n += 1
        self.list_students.sort(key=lambda x: x[1], reverse=True)
        if int(amount) <= 0: amount = 2
        return tabulate(self.list_students[0:int(amount)], headers=["Name", "Score"])

@error_handle
def main():
    option_menu = ""
    while option_menu != "4":
        print("Hello!, you want to know?")
        print("(1) the winners of the book")
        print("(2) the students with the highest success rates")
        print("(3) both")
        print("(4 o other) exit")

        option_menu = input("--> ")
        admin = Student("csv_quiz")
        admin.open_files()
        admin.new_list_student()
        if option_menu == "1":
            print("amount of winner")
            amount_winner = input("--> ")
            print(admin.winner_quiz(amount_winner))
        elif option_menu == "2":
            print("enter the percentage of accuracy ")
            percentage = input("--> ")
            print(admin.major_successes(int(percentage)))
        print("-----------------------------------")

main()          