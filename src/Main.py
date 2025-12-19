'''
Created on Dec 10, 2025

@author: jacksonhooper
'''
from BTree import BTree
import csv
import tkinter as tk
from tkinter import filedialog
from pickle import TRUE, FALSE


#
# Helper function to determine whether a field can be indexed or not
#
def check_double(s: str) -> bool:
    try:
        
        float(s)
        return True
    
    except ValueError:
        
        try:
            
            float(s[1:])
            return True
        
        except:
            
            return False

#
# Changes given string into a double for BTree implementation
#
def make_double(str):
    
    num = "1234567890"
    return_str = ""
    has_decimal = False
    
    for letter in str:
        
        if letter == ".":
            
            if not has_decimal:
                
                has_decimal = True
                return_str += "."
        
        elif letter in num:
            
            return_str += letter
    
    return float(return_str)


#
# Will prompt the user for a CSV file and bring up their system's native file explorer system so they may submit one
#
def prompt_user_for_file():
    
    print("Select a CSV File:")
    root = tk.Tk()
    root.withdraw() # Hide the main tkinter window
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    root.destroy() # Clean up the root window
    return file_path

#
# Calls prompt_user_for_file to obtain CSV file. Accounts for non-submissions and errors in reading the file
# Sorts the CSV file into a list of lists.
#
def file_organizer():
    
    selected_file = prompt_user_for_file()
    
    #Submitted a file
    if selected_file:
        
        print(f"Selected file: {selected_file}")
        
        try:
            
            # Reading CSV file and putting it into a list of lists
            with open(selected_file, 'r') as csvfile:
                
                reader = csv.reader(csvfile)
                
                rows = []
                column = []
                
                for row in reader:
                    
                    counter = 0
                    
                    while(counter < len(row)):
                    
                        column.append(row[counter])
                        
                        counter += 1
                    
                    rows.append(column)
                    column = []
                
                return rows
        
        # Catching errors in reading file. Helps with testing as well.        
        except Exception as e:
            
            print(f"Error reading file: {e}")
    
    # Did not submit a file      
    else:
        
        print("No file selected.")
        
#
# Prints all field headers along with their index to allow for choosing individual fields
#    
def print_fields(fields):
    
    if(len(fields) > 0):
        
        print("\nChoose a field:")
        
        for i in range(len(fields)):
            
            print(f"{i} - {fields[i]}")
        
        print(f"{i + 1} - QUIT PROGRAM")
        
    else:
        
        print("CSV File has no fields")

#
# Prints all base case options for the user
#
def print_user_options():
    
    print("\nChoose an Action:")
    print("1 - Create Index")
    print("2 - Exact Value Search")
    print("3 - Range Query")
    print("4 - Close Program")
    return input()

#
# Sets arrays that store states and locations of hash tables and index state for each column
#
def set_hash_and_index(file):
    
    
    hash = []
    index = []
    
    for i in range(len(file[0])):
        
        hash.append(create_hash_table(i, file))
        index.append([False, None])
    
    return hash, index

#
# Creates hash table for given column
#
def create_hash_table(column, file):
    
    #Multiplies by 1.5 to allow for sufficient space within hash table
    hash_array = [-1] * next_prime(int(len(file) * 1.5))
    
    for i in range(len(file)):
        
        if i != 0:
        
            hash_array[hash_function(str(file[i][column]), len(hash_array))] = file[i][column]
    
    return hash_array
  
#
# Returns next prime greater than given int
#  
def next_prime(n: int) -> int:
    
    def is_prime(x: int) -> bool:
        
        if(x < 2):      return False
        if(x == 2):     return True
        if(x % 2 == 0): return False
        
        for i in range(3, int(x ** 0.5) + 1, 2):
            
            if x % i == 0: return False
            
        return True

    candidate = n + 1
    while True:
        if is_prime(candidate):
            return candidate
        candidate += 1
        
#
# Utilizes my hash function from HW5 to create hash values
#
def hash_function(str, size):
    
    p = 53
    m = size
    hash_value = 0
    p_pow = 1
    
    for c in str:
        
        hash_value = (hash_value + (ord(c) + 1) * p_pow) % m
        p_pow = (p_pow * p) % m
        
    return int(hash_value);

#
# Creates a new index
#
def create_index(index_array, file):
    
    indexes_left = False
    valid_choices = []
    counter = 0;
    
    for bool in index_array:
        
        if not bool[0]:
            
            indexes_left = True
    
    
    if indexes_left:
    
        print("These fields are indexed:")
        
        for i in range(len(index_array)):
            
            if index_array[i][0]:
                
                print(f"{file[0][i]}")
                
        print("Which field would you like to index?")
        
        for i in range(len(file[0])):
            
            if not index_array[i][0]:
                
                if check_double(file[1][i]):
                    
                    valid_choices.append(str(i))
                    print(f"{i} - {file[0][i]}")
        
        user_index_choice = input()
        
        try:
            
            if valid_choices.index(user_index_choice) == -1:
                    
                print("Not a Valid Choice")
                return index_array
            
            else:
                    
                index_array[int(user_index_choice)] = [True, create_b_tree(int(user_index_choice), file)]
                return index_array
        
        except:
            
            print("Not a Valid Choice")
            return index_array
            
    
    else:
        
        print("All fields are indexed")
        return index_array


#
# Creates a b-tree
#
def create_b_tree(index, file):
    
    tree = BTree(5)
    counter = 0
    
    for row in file:
        
        if counter != 0:
        
            tree.insert(make_double(row[index]))
            
        counter += 1
        
    return tree
#
# Calls fileSort to obtain CSV File. Currently just ensuring the list of lists is being created properly.
#
def main():
    
    #prompts CSV file upload
    inputFile = file_organizer()
    
    #create hash tables and index array
    hash_tables, indexed_fields = set_hash_and_index(inputFile)
    
    #runs until user submits something that is not a 1 2 or 3
    while True:
        
        user_choice = print_user_options()
        
        if user_choice == "1":
        
            indexed_fields = create_index(indexed_fields, inputFile)
            
            for range in indexed_fields:
                print(range)
            
        if user_choice == "2":
        
            pass
        
        if user_choice == "3":
            
            pass
            
        if user_choice == "4":
            
            break
    
    
        

if __name__ == '__main__':
    main()