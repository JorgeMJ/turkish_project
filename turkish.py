#!/usr/bin/env python

'''
- This program (turkish.py) accomplishes three things:

1. Creates new csv files containing selected columns from the original csv files found at the given filepath.
2. Creates a csv file containing the information found in the created csv files of the previous section.
3. Creates a 'masterlist.csv' containing a register of the cleaned files in section 1.

- Assumptions:

1. It assumes the user will have Python 3 installed.
2. It assumes that the program (turkish.py) will be placed in the folder that contains the folders containing
   the original csv files.
3. It assumes that the operating system is Windows, Mac or Linux. 
4. The created csv files will be stored in the same folder as the program's one.

- How to run the program:

Option 1: double click on the icon of the program (turkish.py)
Option 2: Command line. Go to the folder containg the program using the 'cd' command. Then, type 'py turkish.py'
          This option is more advantageous because if, for example, there is an error, it will show error related
          information in the command prompt. 
'''

import cleanall 
import accuracy


def main():
	
    # Reads .csv files from 'F19Data/[FOLDER]
    # Generates the 'cleaned_ALL_Pilot_Mmm_dd_yyyy.csv'
    # Saves it in the 'cleaned_ALL' folder
    cleanall.cleanAll()

    # Reads from 'cleaned_ALL_Pilot_Mmm_dd_yyyy.csv'
    # Generates 'Cleaned_Pilot_CALL_Accuracy.csv'
    # Saves it in the 'Pilot_CALL_Accuracy' folder.
    accuracy.accuracy()


if __name__ == "__main__":
	main()
