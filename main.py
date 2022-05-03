import os
import pandas as pd
from tabulate import tabulate
from itertools import chain

"""
    ! @Decoracts {error_handle} func: handle of errors 
"""
def error_handle(func):
    def process_error(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as er:
            raise Exception(f"error type data. {er}")
        return result
    return process_error



class FileCsv:
    
    all_csv = []

    """ 
        ? @Params {directory} str: contains the directory where to host the files 
    """
    @error_handle
    def __init__(self, directory:str = "") -> None:
        self.directory = directory
    
    """
        ? @Params {file_name} str: names of the files of directory (params optional)

        ! @Function {open_files} func: open the files to read and host in the "list_cvs = []" return self.all_csv
    """
    def open_files(self, file_name:str = "") -> list:
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

    list_students = []
    
    def __init__(self, directory) -> None:
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
        print(tabulate(self.list_students[0:amount], headers=["Name", "Score"]))


luis = Student("csv_quiz")

luis.open_files()
luis.new_list_student()

print(luis.winner_quiz(1))
                