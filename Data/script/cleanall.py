'''
This module create as many output folders as input folders in teh form of A##Data. (e.g. F19Data) in each of these folders
the output files [FOLDER]_cleaned_ALL_Pilot_[DATE].csv and [FOLDER]_master_list.csv are stored.
The [FOLDER]_cleaned_ALL_Pilot_[DATE].csv contains selected and sumarized data from the input files found.
The [FOLDER]_master_list.csv is a list of the input files that have been processed identified by participant and
condition of the participant. 
'''
import pandas as pd            
from datetime import datetime
import glob                     
import os  
import re                     
import platform                 


def selectFolder(pattern, flist):

    ''' Returns a list of the folders that match a given patter '''

    result = []
    for f in flist:
        if re.search(pattern, f):
            result.append(f)
    return result


def cleanAll():

    ''' Reads the input csv files, selects the relevant information, saves it in a [FOLDER]_cleaned_ALL_Pilot_[DATE].csv.
        It also generates the [FOLDER]_master_list.csv '''

    # Defines filepaths to locate the relevant input files. 
    pattern= '/[A-Z]*[0-9][0-9][0-9]/[0-9][0-9][0-9]*[0-9][0-9][0-9][0-9].csv'
    
    # Creates a list of the folders containing the relevant input files.
    f_list = os.listdir('../../')
    folder_list = selectFolder('[FS][0-9]{2}Data', f_list)
    
    for folder in folder_list:
        # Creates an empty cleannedALL dataframe
        cleanedALL = pd.DataFrame()

        # Creates an empty masterlist dataframe
        masterlist = pd.DataFrame(columns=['participant id', 'condition', 'date collected', 'date cleaned',
            'raw file name'])

        # Creates a folder where the output files 'cleaned_ALL', 'master_list', and 'CALL_Accuracy' will be saved.
        if not os.path.exists('../' + folder):
            os.mkdir('../' + folder)

        # Lists all relevant input filespaths.
        files= glob.glob('../../' + folder + pattern) 

        ###  Creates the cleaned csv files  ####################################################################################
        ########################################################################################################################
        for filename in files:
            # Makes sure 'filename' can be opened.
            try:
                # Reads every file in the 'files' list. header=0 says that the first row is the columns names.
                df= pd.read_csv(filename, encoding='utf-8-sig', header=0)
            except IOError as e:
                print(e)

            # Takes the participant Id and the code (BLUE, RED or TAN)
            participantId= df.loc[1, 'participant']
            expName= df.loc[1, 'expName']

            if 'BLUE' in expName:
        	    condition = 'BLUE'
        	    code = 1
            elif 'TAN' in expName:
        	    condition = 'TAN'
        	    code = 2
            elif 'RED' in expName:
        	    condition = 'RED'
        	    code = 3
    

            # Takes only those rows that are block 1 or block 5
            dfblocks_1_5 = df.query('block == 1 | block == 5')

            # Selects columns
            dfout = dfblocks_1_5[['imageFileCaseLeft', 'imageFileCaseRight', 'correctAns', 'soundQuestions', 'soundAnswers', 'block',
                 'scaffoldLevel', 'construction', 'stimuliCode', 'nameCode', 'set', 'stemCode', 'group', 'itemType',
                 'distractorItem', 'objCase','relativeClause', 'subjSingPlur', 'objSingPlur', 'englishPhrase', 'turkishPhrase',
                 'englishNoun', 'turkishNom', 'turkishNounCase', 'grammar', 'gloss', 'verb', 'B1preCOMP.thisTrialN',
                 'B1preCOMP.thisIndex', 'B5postCOMP.thisTrialN', 'B5postCOMP.thisIndex', 'compDialogue_key.keys',
                 'compDialogue_key.corr', 'participant', 'expName']]
     
            # Adds column 'condition'. It will hold the 'code' (values 1, 2 or 3)
            dfout.insert(len(dfout.columns), 'condition', code, allow_duplicates=True)

            # Deletes 'expName' column ##CHECK CHAINING
            pd.options.mode.chained_assignment = None
            dfout.drop('expName', axis=1, inplace=True) 
                                                           
            # Adds columns 'thisTrialN' and 'thisIndex'
            dfout.insert(27, 'thisTrialN', 0, allow_duplicates=True)
            dfout.insert(28, 'thisIndex', 0, allow_duplicates=True)
       
            # Fills the columns 'thisTrialN' and 'thisIndex'
            dfout.loc[dfout['block']==1, 'thisTrialN']= dfout['B1preCOMP.thisTrialN'] 
            dfout.loc[dfout['block']==5, 'thisTrialN']= dfout['B5postCOMP.thisTrialN']
            dfout.loc[dfout['block']==1, 'thisIndex']= dfout['B1preCOMP.thisIndex'] 
            dfout.loc[dfout['block']==5, 'thisIndex']= dfout['B5postCOMP.thisIndex']

            # Deletes columns 'B1preCOMP.thisTrialN', 'B5postCOMP.thisTrialN', 'B1preCOMP.thisIndex' & 'B5postCOMP.thisIndex'
            dfout.drop(['B1preCOMP.thisTrialN', 'B5postCOMP.thisTrialN', 'B1preCOMP.thisIndex',
                'B5postCOMP.thisIndex'], axis=1, inplace=True)


        ###  Adds row to 'masterlist'  #####################################################################################
        ####################################################################################################################
      
            # Makes sure it is a Windows platform to collect the creation time of 'filename'
            if platform.system() == 'Windows':
                creationtime = os.path.getctime(filename)
            elif platform.system() == 'Darwin' or platform.system() == 'Linux':
                creationtime = os.stat(filename).st_birthtime
            else: 
                creationtime = os.path.getctime(filename)
                print('**Warning: This is not a recognized platform. The \'date collected\' of \
                    ' + filename + ' in \'masterlist.csv\' may not correspond to the creation time.')

            # Creates a new row for the masterlist
            newrow = {
                'participant id': participantId,
                'condition': code,
                'date collected': datetime.fromtimestamp( creationtime ).strftime('%b-%d-%Y'),
                'date cleaned': datetime.now().strftime('%b-%d-%Y'),
                'raw file name': filename
            }

            ##Append dataframes into Cleaned_ALL file
            cleanedALL = cleanedALL.append(dfout, ignore_index=True)

            # Adds the new row to the masterlist
            masterlist = masterlist.append(newrow, ignore_index=True)

        # Saves the master_list as csv
        try:
            masterlist.to_csv(f'../' + folder + '/' + folder + '_master_list.csv', index=False, encoding='utf-8-sig')
        except IOError as e:
            print(e)

        # Gets the current date
        currentdate = datetime.now().strftime('%b_%d_%Y_%H-%M-%S')

        # Saves all cleaned dataframes in a csv file.
        try:
            cleanedALL.to_csv(f'../' + folder + '/' + folder + '_cleaned_ALL_Pilot_'+ currentdate +'.csv', index=False, encoding='utf-8-sig')
        except IOError as e:
            print(e)
    