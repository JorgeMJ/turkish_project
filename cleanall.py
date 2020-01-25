import pandas as pd             #managing spreadsheets
from datetime import datetime
import glob                     #read files
import os                       #interaction with the operating system (e.g. manage folders)
import platform                 #access to the platform


def cleanAll():

    '''  '''
    # Defines filepath (path) and fle names (patern) 
    path= 'F19Data/[A-Z]*[0-9][0-9][0-9]/'
    patern= '[0-9][0-9][0-9]*[0-9][0-9][0-9][0-9].csv'
 
    # Lists all files that matches 'patern' in the filepath 'path'
    files= glob.glob(path + patern) 
    
    # Creates an empty cleannedALL dataframe
    cleanedALL = pd.DataFrame()

    # Creates an empty masterlist dataframe
    masterlist = pd.DataFrame(columns=['participant id', 'condition', 'date collected', 'date cleaned',
          'raw file name'])#, 'cleaned file name'])


    # Creates a folder where the 'cleaned_ALL' file and 'master_list' file will be saved
    if not os.path.exists('cleaned_ALL'):
        os.mkdir('cleaned_ALL')


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
        masterlist.to_csv('cleaned_ALL/master_list.csv', index=False, encoding='utf-8-sig')
    except IOError as e:
        print(e)

    # Gets the current date
    currentdate = datetime.now().strftime('%b_%d_%Y')

    # Saves all cleaned dataframes in a csv file.
    try:
        cleanedALL.to_csv(f'cleaned_ALL/cleaned_ALL_Pilot_'+ currentdate +'.csv', index=False, encoding='utf-8-sig')
    except IOError as e:
        print(e)