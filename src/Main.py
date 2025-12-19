'''
Created on Dec 10, 2025

@author: jacksonhooper
'''
import os
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
    
    num = "1234567890."
    return_str = ""
    
    for char in str:
        
        if char in num:
            
            return_str += char
    
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
def set_hash_and_index(file, index = None):
    
    #Multiplies by 1.5 to allow for sufficient space within hash table
    hash_tables = [None] * len(file[0])
    
    if index == None:
        
        index = []
    
        for i in range(len(hash_tables)):
            
            hash_tables[i] = add_hash_table(i, file)
    
            index.append([False, None])
            
    else:
        
        for i in range(len(hash_tables)):
            
            hash_tables[i] = add_hash_table(i, file)
            
            for i in range(len(index)):
                
                if index[i][0]:
                
                    index[i][1] = create_b_tree(i, file)
                
    
    return hash_tables, index

#
# Creates hash table for given column
#
def add_hash_table(column, file):
    
    hash_array = [None] * next_prime(int(len(file) * 1.5))
    
    for i in range(len(file)):
        
        if i != 0:
            
            if hash_array[hash_function(file[i][column], len(hash_array))] != None:
                
                hash_array[hash_function(file[i][column], len(hash_array))].append(file[i])
                
            else:
        
                hash_array[hash_function(file[i][column], len(hash_array))] = [file[i]]
    
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
    
    tree = BTree(10)
    counter = 0
    
    for row in file:
        
        if counter != 0:
        
            tree.insert([make_double(row[index]), row])
            
        counter += 1
        
    return tree

#
# Searches for the value specified and returns row in CSV where data is found
#
def exact_value_search(file, hash_tables):
    
    output_array = []
    
    user_input = input("What would you like to search?: ")

    user_hash = hash_function(user_input, next_prime(int(len(file) * 1.5)))
    
    for table in hash_tables:
        
        if table[user_hash] != None:
        
            for data in table[user_hash]:
                
                for i in range(len(data)):
                    
                    if data[i] == user_input: 
                        
                            output_array.append(data)
    
    if len(output_array) == 0:
        
        print("No results found.")
        return file
    
    else:
                            
        for j in range(len(output_array)):
            
            print(output_array[j])
        
        print_decision = input("Would you like to download your results?\n1 - Yes\n2 - No\n")
        
        if print_decision == "1":
            
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop, "exact_search_results.csv")
            export_csv(output_array, file_path)
            print("Download Complete\n")
        
        delete_decision = input("Would you like to delete this data from the database?\n1 - Yes\n2 - No\n")
        
        if delete_decision == "1":
            
            return delete_data(output_array, file)
            print("Deletion Complete\n")
            
        return file
#
# Method to export CSV file to desktop   
#
def export_csv(data, filename):

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

#
# Deletes data from all active databases. Returns new file
#
def delete_data(array, file):
    
    for data in array:
        
        try:
            
            file.remove(data)
            
        except:
            
            pass
            
    return file

#
# Performs the ranged search function
#
def range_search(indexed_fields, file):
    
    available_fields = []
    
    #gets the indexes of all fields that have been indexed already
    for i in range(len(indexed_fields)):
        
        if indexed_fields[i][0]:
        
            available_fields.append(i)
    
    print("Choose a field that has been indexed to search from:")
    
    if len(available_fields) == 0:
        
        print("No fields have been indexed yet.")
    
    else:
        
        for i in range(len(available_fields)):
            
            print(f"{i} - {file[0][available_fields[i]]}")
            
        column = int(input())

        try:
        
            if column < len(available_fields):
                
                btree = indexed_fields[available_fields[column]][1]
                
                print("How would you like to search?\n1 - Lower Bound\n2 - Upper Bound\n3 - Both")
                
                bound_choice = input()
                
                if bound_choice == "1":
                    
                    print("Submit your lower bound:")
                    
                    try:  
                        
                        lower_bound = make_double(input(""))
                    
                        matches = tree_lower_helper(btree.root, lower_bound)
                        
                        if len(matches) == 0:
        
                            print("No results found.")
                            return file
                        
                        for row in matches:
                            
                            print(row)
                            
                        print_decision = input("Would you like to download your results?\n1 - Yes\n2 - No\n")
        
                        if print_decision == "1":
                            
                            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                            file_path = os.path.join(desktop, "range_query_results.csv")
                            export_csv(matches, file_path)
                            print("Download Complete\n")
                        
                        delete_decision = input("Would you like to delete this data from the database?\n1 - Yes\n2 - No\n")
                        
                        if delete_decision == "1":
                            
                            print("Deletion Complete\n")
                            return delete_data(matches, file)
                            
                        return file
                        
                    except:
                        
                        print("Error in Bound")
                    
                
                elif bound_choice == "2":
                    
                    print("Submit your upper bound:")
                    
                    try:  
                        
                        upper_bound = make_double(input(""))
                    
                        matches = tree_upper_helper(btree.root, upper_bound)
                        
                        if len(matches) == 0:
        
                            print("No results found.")
                            return file
                        
                        for row in matches:
                            
                            print(row)
                            
                        print_decision = input("Would you like to download your results?\n1 - Yes\n2 - No\n")
        
                        if print_decision == "1":
                            
                            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                            file_path = os.path.join(desktop, "range_query_results.csv")
                            export_csv(matches, file_path)
                            print("Download Complete\n")
                        
                        delete_decision = input("Would you like to delete this data from the database?\n1 - Yes\n2 - No\n")
                        
                        if delete_decision == "1":
                            
                            print("Deletion Complete\n")
                            return delete_data(matches, file)
                            
                        return file
                        
                    except:
                        
                        print("Error in Bound")
                
                elif bound_choice == "3":
                    
                    try:  
                        
                        print("Submit your upper bound:")
                        
                        upper_bound = make_double(input(""))
                        
                        print("Submit your lower bound:")
                        
                        lower_bound = make_double(input(""))
                    
                        matches = tree_both_helper(btree.root, lower_bound, upper_bound)
                        
                        if len(matches) == 0:
        
                            print("No results found.")
                            return file
                        
                        for row in matches:
                            
                            print(row)
                            
                        print_decision = input("Would you like to download your results?\n1 - Yes\n2 - No\n")
        
                        if print_decision == "1":
                            
                            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                            file_path = os.path.join(desktop, "range_query_results.csv")
                            export_csv(matches, file_path)
                            print("Download Complete\n")
                        
                        delete_decision = input("Would you like to delete this data from the database?\n1 - Yes\n2 - No\n")
                        
                        if delete_decision == "1":
                            
                            print("Deletion Complete\n")
                            return delete_data(matches, file)
                            
                        return file
                        
                    except:
                        
                        print("Error in Bound")
                 

        except:
            
            return file


def tree_lower_helper(node, lower_bound, result=None):
    if result is None:
        result = []

    if node is None:
        return result

    # Check keys in this node
    for key in node.keys:
        if key[0] >= lower_bound:
            result.append(key[1])

    # Recurse into children
    for child in node.children:
        tree_lower_helper(child, lower_bound, result)

    return result

def tree_upper_helper(node, upper_bound, result=None):
    if result is None:
        result = []

    if node is None:
        return result

    # Check keys in this node
    for key in node.keys:
        if key[0] <= upper_bound:
            result.append(key[1])

    # Recurse into children
    for child in node.children:
        tree_upper_helper(child, upper_bound, result)

    return result

def tree_both_helper(node, lower_bound, upper_bound, result=None):
    if result is None:
        result = []

    if node is None:
        return result

    # Check keys in this node
    for key in node.keys:
        if lower_bound <= key[0] <= upper_bound:
            result.append(key[1])

    # Recurse into children
    for child in node.children:
        tree_both_helper(child, lower_bound, upper_bound, result)

    return result



#
# Calls fileSort to obtain CSV File. Currently just ensuring the list of lists is being created properly.
#
def main():
    
    #prompts CSV file upload
    inputFile = file_organizer()
    
    #create hash tables and index array
    hash_tables, indexed_fields = set_hash_and_index(inputFile)
    
    #
    # Runs until user submits something that is not a 1 2 or 3
    #
    while True:
        
        user_choice = print_user_options()
        
        if user_choice == "1":
        
            indexed_fields = create_index(indexed_fields, inputFile)
            
        elif user_choice == "2":
        
            inputFile = exact_value_search(inputFile, hash_tables)
            hash_tables, indexed_fields = set_hash_and_index(inputFile, indexed_fields)
        
        elif user_choice == "3":
            
            inputFile = range_search(indexed_fields, inputFile)
            hash_tables, indexed_fields = set_hash_and_index(inputFile, indexed_fields)
            
        else:
            
            break
    
    
        

if __name__ == '__main__':
    main()