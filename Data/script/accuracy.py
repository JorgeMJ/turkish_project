'''
  This module creates a csv file in the form of '[FOLDER]_CALL_Accuracy_[DATE].csv'. This input file was created by the 
  cleanAll() function from the module cleanall.py. The output file is stored in the same folder as the input file is. 
  This module computes several accuracy measurements based on the 'compDialogue_key.corr' column of the imput file
  [FOLDER]_cleaned_ALL_Pilot_[DATE].csv.
'''
import os
import re
import pandas as pd
import glob
from datetime import datetime

def totals(df):

    ''' Gets the total number of answers for each measure and returns a dictionary. '''

    totals = {
	    'tB1AccTotal':    len(df.loc[(df['block']==1), 'compDialogue_key.corr'].values),
        'tB1AccOC':       len(df.loc[ (df['block']==1) & (df['itemType'] == 'OC'), 'compDialogue_key.corr' ].values),
        'tB1AccCC':       len(df.loc[ (df['block']==1) & (df['itemType'] == 'CC'), 'compDialogue_key.corr' ].values),
        'tB5AccTotal':    len(df.loc[(df['block']==5), 'compDialogue_key.corr'].values),
        'tB5AccOldTotal': len(df.loc[ (df['block']==5) & (df['group'].isin(['Res1a', 'Res1b', 'Res2'])),
            'compDialogue_key.corr' ].values),  
        'tB5AccNewTotal': len(df.loc[ (df['block']==5) & (df['group']== 'cPOST'), 'compDialogue_key.corr' ].values),
        'tB5AccTotalOC':  len(df.loc[ (df['block']==5) & (df['itemType'] == 'OC'), 'compDialogue_key.corr' ].values),  
        'tB5AccTotalCC':  len(df.loc[ (df['block']==5) & (df['itemType'] == 'CC'), 'compDialogue_key.corr' ].values),
        'tB5AccOldOC':    len(df.loc[ (df['block']==5) & (df['itemType'] == 'OC') & (df['group'].isin(['Res1a',
            'Res1b', 'Res2'])), 'compDialogue_key.corr' ].values),
        'tB5AccOldCC':    len(df.loc[ (df['block']==5) & (df['itemType'] == 'CC') & (df['group'].isin(['Res1a',
            'Res1b', 'Res2'])), 'compDialogue_key.corr' ].values),
        'tB5AccNewOC':    len(df.loc[ (df['block']==5) & (df['itemType'] == 'OC') & (df['group']== 'cPOST'),
            'compDialogue_key.corr' ].values),
        'tB5AccNewCC':    len(df.loc[ (df['block']==5) & (df['itemType'] == 'CC') & (df['group']== 'cPOST'),
            'compDialogue_key.corr' ].values)
    }

    return(totals)


def rightAnswers(df):

    ''' Gets the total number of right answers for each measure nd returns a dictionary. '''
    
    rights = {
        'rB1AccTotal':    len(df.loc[ (df['block']==1) & (df['compDialogue_key.corr']==1), 'compDialogue_key.corr' ].values),
        'rB1AccOC':       len(df.loc[ (df['block']==1) & (df['compDialogue_key.corr'] == 1) & (df['itemType'] == 'OC'),
            'compDialogue_key.corr'].values),
        'rB1AccCC':       len(df.loc[ (df['block']==1) & (df['compDialogue_key.corr'] == 1) & (df['itemType'] == 'CC'),
            'compDialogue_key.corr'].values),
        'rB5AccTotal':    len(df.loc[ (df['block']==5) & (df['compDialogue_key.corr'] == 1), 'compDialogue_key.corr'].values),
        'rB5AccOldTotal': len(df.loc[ (df['block']==5) & (df['compDialogue_key.corr'] == 1) &
            (df['group'].isin(['Res1a', 'Res1b', 'Res2'])), 'compDialogue_key.corr' ].values),
        'rB5AccNewTotal': len(df.loc[ (df['block']==5) & (df['compDialogue_key.corr'] == 1) & (df['group']=='cPOST'),
            'compDialogue_key.corr' ].values),
        'rB5AccTotalOC':  len(df.loc[ (df['block']==5) & (df['compDialogue_key.corr'] == 1) & (df['itemType'] == 'OC'),
            'compDialogue_key.corr'].values),
        'rB5AccTotalCC':  len(df.loc[ (df['block']==5) & (df['compDialogue_key.corr'] == 1) & (df['itemType'] == 'CC'),
            'compDialogue_key.corr'].values),
        'rB5AccOldOC':    len(df.loc[ (df['block']==5) & (df['compDialogue_key.corr'] == 1) & (df['itemType'] == 'OC') &
            (df['group'].isin(['Res1a', 'Res1b', 'Res2'])), 'compDialogue_key.corr'].values),
        'rB5AccOldCC':    len(df.loc[ (df['block']==5) & (df['compDialogue_key.corr'] == 1) & (df['itemType'] == 'CC') &
            (df['group'].isin(['Res1a', 'Res1b', 'Res2'])), 'compDialogue_key.corr'].values),
        'rB5AccNewOC':    len(df.loc[ (df['block']==5) & (df['compDialogue_key.corr'] == 1) & (df['itemType'] == 'OC') &
            (df['group']=='cPOST'), 'compDialogue_key.corr'].values),
        'rB5AccNewCC':    len(df.loc[ (df['block']==5) & (df['compDialogue_key.corr'] == 1) & (df['itemType'] == 'CC') &
         (df['group']=='cPOST'), 'compDialogue_key.corr'].values)
    }

    return(rights)


def indexRightAnswers(d_total, d_rights):
	
    ''' Computes the indexes of accuracy fro each measure and returns a dictionary. '''

    idx = {
        'B1AccTotal':     d_rights['rB1AccTotal'] / d_total['tB1AccTotal'],
        'B1AccOC':        d_rights['rB1AccOC'] / d_total['tB1AccOC'],
        'B1AccCC':        d_rights['rB1AccCC'] / d_total['tB1AccCC'],
        'B5AccTotal':     d_rights['rB5AccTotal'] / d_total['tB5AccTotal'],
        'B5AccOldTotal':  d_rights['rB5AccOldTotal'] / d_total['tB5AccOldTotal'],
        'B5AccNewTotal':  d_rights['rB5AccNewTotal'] / d_total['tB5AccNewTotal'],
        'B5AccTotalOC':   d_rights['rB5AccTotalOC'] / d_total['tB5AccTotalOC'],
        'B5AccTotalCC':   d_rights['rB5AccTotalCC'] / d_total['tB5AccTotalCC'],
        'B5AccOldOC':     d_rights['rB5AccOldOC'] / d_total['tB5AccOldOC'],
        'B5AccOldCC':     d_rights['rB5AccOldCC'] / d_total['tB5AccOldCC'],
        'B5AccNewOC':     d_rights['rB5AccNewOC'] / d_total['tB5AccNewOC'],
        'B5AccNewCC':     d_rights['rB5AccNewCC'] / d_total['tB5AccNewCC']
    } 

    return(idx)


def selectFolder(pattern, flist):

    ''' Returns a list of the folders that match a given patter '''

    result = []
    for f in flist:
        if re.search(pattern, f):
            result.append(f)
    return result


def accuracy():

    ''' Reads the 'cleaned_ALL/cleaned_ALL_Pilot_[DATE].csv' file to perform different acccuracy indices
        on each participant and stores them in a nre file 'pilot_CALL_accuracy/Cleaned_Pilot_CALL_Accuracy.csv'. '''
 
    # Gets the list of folders containing the input [FOLDER]_cleaned_ALL_Pilot_[DATE].csv files.
    pattern = re.compile('[FS][0-9]{2}Data')
    f_list = os.listdir('../')
    folder_list = selectFolder(pattern, f_list)
    
    for folder in folder_list:
        # Creates dataframe to store accuracies
        dfacc = pd.DataFrame(columns=['participant', 'condition', 'B1AccTotal', 'B1AccOC',
           'B1AccCC', 'B5AccTotal','B5AccOldTotal', 'B5AccNewTotal', 'B5AccTotalOC', 'B5AccTotalCC',
           'B5AccOldOC','B5AccOldCC','B5AccNewOC', 'B5AccNewCC'])

        # Gets the 'cleaned_ALL_Pilot_[DATE].csv' file
        cleaned_file = glob.glob('../' + folder + '/[FS][0-9][0-9]Data_cleaned_ALL_Pilot_*.csv')
     
        # From cleaned_file gets the most recent.
        filename = max(cleaned_file, key=os.path.getctime)
        
        # Opens 'cleaned_ALL_Pilot_[DATE].csv' file. ***Looks for the leatest one (ctime)***
        try:
            dfclean = pd.read_csv(filename, encoding='utf-8-sig', header=0)
        except IOError as e:
            print(e)  
        
        # Makes a set holding all the participants
        participants =set(dfclean['participant'])
        
        for p in participants:
            # Takes the section of each participant p
            a = dfclean[dfclean['participant']==p]
            # Calculates the accuracy indeces and stores them in the 'acc' dic
            acc = indexRightAnswers(totals(a), rightAnswers(a))  
            #Adds 'participant' and 'condition'
            acc['participant'] = p
            acc['condition'] = a['condition'].iloc[0]
            # Adds new line to the dataframe 
            dfacc = dfacc.append(acc, ignore_index=True)

        # Gets the current date.
        currentdate = datetime.now().strftime('%b_%d_%Y_%H-%M-%S')

        # Save the dataframe in a csv file in the 'Pilot_CALL_accuracy' folder
        try:
            dfacc.to_csv(f'../'+ folder + '/' + folder + '_CALL_Accuracy_' + currentdate +'.csv', encoding='utf-8-sig', index=False)
        except IOError as e:
            print(e)

    


