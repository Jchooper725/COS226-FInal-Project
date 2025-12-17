'''
Created on Dec 10, 2025

@author: jacksonhooper
'''

import csv
import tkinter as tk
from tkinter import filedialog


#
# Will prompt the user for a CSV file and bring up their system's native file explorer system so they may submit one
#
def prompt_user_for_file():
    
    print("Submit CSV File:")
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
def fileSort():
    
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
# Calls fileSort to obtain CSV File. Currently just ensuring the list of lists is being created properly.
#
def main():
    
    inputFile = fileSort()
    
    print(inputFile[0])
    print(inputFile[1])
    print(inputFile[2])
    print(inputFile[3])
    print(inputFile[4])
        

if __name__ == '__main__':
    main()