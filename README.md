RUN INSTRUCTIONS:
The program is a simple, texted-based user interface that will promp the user for an input at certain points. Before prompting the user, the program will alawys print out all actions
that can be taken at that point and a corresponding number. To choose one of the presented options, type just the number corresponding to that option and submit it. Any other submissions
will result in the program ending or defaulting to the NO option in the case of a yes or no question (such as when being asked whether you would like to download your results). The exceptions
to this are when the user is doing an exact value search or a range search in which case they will be prompted to input either the exact value they are searching for or the bounds they would
like to search by.

EFFICIENCY ANALYSIS:
* Initialization of Database: After a CSV file is submitted, the program will iterate through the file and create an array of arrays containing the information. This process will reach each
  element once and therefore takes O(n) time to complete with n being the size of the CSV file. Hash tables are also being constructed with each element being put through my hash code
  function before being stored in a large array.

* Creation of Indexes: When the user prompts the program to index a field, the program will take all the values in the column associated with that field and construct a BTree. This process
  iterates through all values in a column and therefore has a linear time complexity.

* Queries: When performing an exact value search, the program will run the user's input through the hash code function to determine where in the hash table to look for exact matches. Then,
  it double checks every item found at that index to make sure that it does contain a field that matches the user's search. This is much faster than searching through all rows for a match and
  the time it takes to complete will only depend on how many items with a matching value the CSV file contains. When doing a range search, the code will iterate through the BTree associated with
  the field being searched and produce a list of all values that meet the criteria set by the bounds. This is also faster than searching through all values as the range of all values in a bound
  will be together within a BTree.

* Deletions: When the user chooses to delete the data they've searched for, the program runs a function that calls the remove function from the original file for each row of the searched data.
  This process has a worst case runtime of being exponential as the code could go through every row in the original file for each row in the searched data.

HASH FUNCTION:
The hash function utilizes each character in the input to generate the hash code. It multiplies it by a number that is constantly updating to ensure that similar data is parsed sufficiently
different. The generated code is then modulod by the size of the hash table, which is set to the next prime number greater than the number of rows in the original CSV file. This ensures that 
the result will be within an index in the array.

BTREE:
The BTree is standard aside from that each of the keys is a tuple. Index one is the row that is being sorted into the array, while index zero is the value within that row that the BTree is
looking at in order to sort it. This allows the BTree to be searched when doing a range search normally as well as returning the entire row associated with the data when that data is wanted.
This is utilized when doing the range search as when looking through the BTree, the program first determines whether the node qualifies based on the bounds specified. If it does, then 
returns the row associated with that value.

SEARCHABLE FIELDS:
The program determines searchable fields to be those that can be turned into a float via the float() function or one that can be if the first character is removed. This approach emphasized 
simplicity as it yielded predictable results that I could then test the rest of the program on.
