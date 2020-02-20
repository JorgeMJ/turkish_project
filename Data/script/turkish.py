#!/usr/bin/env python

'''
- This program (turkish.py) accomplishes three things:

1. Creates new csv files containing selected columns from the original csv files found at the given filepath.
2. Creates a 'masterlist.csv' containing a register of the cleaned files in section 1.
3. Creates a file containing indexes of accuracy based on the files created in point 1.

- Assumptions:

1. It assumes the user will have Python 3 installed.
2. It assumes that the operating system is Windows, Mac or Linux. 

- Script:

There are three files in this program:
1. turkish.py: Main script. It call the functions from the other two modules/
2. cleanall.py: contains the functions to retrive the input files, clean them and generate the output clean files.
3. accuracy.py: contains the functions to compute the accuracy indeces from the clean files and output the result in
                a accuracy file. 

- File structure:

           {Root}
              |_ {F19Data}(*)
              |         |_ {BLUE025}
              |         |        |_ 025_BLUE_092419_2019_Nov_04_1514.csv
              |         |
              |         |_ {RED020}
              |         |        |_ 020_RED_092419_2019_Oct_29_1506.csv
              |         |
              |         |_ {TAN041}
              |                  |_ 041_TAN_092419_2019_Nov_26_1243.csv
              |
              |
              |_ {S20Data}(*)
              |         |_ {BLUE050}
              |         |        |_ 050_BLUE_092419_2019_Dec_09_1234.csv
              |         |
              |         |_ {RED049}
              |         |        |_ 049_RED_092419_2019_Dec_06_1115.csv
              |         |
              |         |_ {TAN048}
              |                  |_ 048_TAN_092419_2019_Dec_04_1237.csv
              |         
              |
              |_ {Data}
                   |
                   |_ {script}
                   |        |_ turkish.py
                   |        |_ cleanall.py
                   |        |_ accuracy.py
                   |      
                   |_ {F19Data}(**)
                   |        |_ F19Data_cleaned_ALL_Pilot_[DATE].csv
                   |        |_ F19Data_master_list.csv
                   |        |_ F19Data_CALL_Accuracy_[DATE].csv
                   |
                   |_ {S20Data}(**)
                            |_ S20Data_cleaned_ALL_Pilot_[DATE].csv
                            |_ S20Data_master_list.csv
                            |_ S20Data_CALL_Accuracy_[DATE].csv

          (*) Folders containing the input files
          (**) Folders created to contain the output files
            

- How to run the program:

Option 1: double click on the icon of the program (turkish.py)
Option 2: Command line. Go to the folder containg the program using the 'cd' command. Then, type 'py turkish.py'
          This option is more advantageous because if, for example, there is an error, it will show error related
          information in the command prompt. 
'''

from cleanall import cleanAll 
from accuracy import accuracy


def main():
	
    # Reads .csv files from input data folders.
    # Generated [FOLDER]_cleaned_ALL_Pilot_[DATE].csv and [FOLDER]_master_list.csv
    cleanAll()

    # Reads from [FOLDER]_cleaned_ALL_Pilot_[DATE].csv
    # Generates [FOLDER]_CALL_Accuracy_[DATE].csv
    accuracy()

if __name__ == "__main__":
	main()
