
from pathlib import Path
from assets.metadata import google_update_year

debugLog = True
enableFileDeletion = False

#
#
#
#
def check_for_duplicates(searchFile, inputPath):

    for currentFile in inputPath.iterdir():               # loop thru files in directory
        if currentFile.is_dir():                          # do not act on folders
            check_for_duplicates(searchFile, currentFile) # recusive call for folders
        else:
            # do not check file against itself
            if not searchFile == currentFile:

                # define variables of interest
                searchFileName = searchFile.stem
                currentFileName = currentFile.stem
                searchFileSize = searchFile.stat().st_size
                currentFileSize = currentFile.stat().st_size

                # search for searchFile name in currentFile name
                if currentFileName.find(searchFileName) <= 0:
                    # check if files are the same size
                    if currentFileSize == searchFileSize:

                        if debugLog:
                            print()
                            print(f'            Search File: {searchFile.stem}')
                            print(f'       Search File Path: {searchFile}')
                            print(f'           Currnet File: {currentFile.stem}')
                            print(f'      Current File Path: {currentFile}')                    
                            print(f'***Duplicate file found: {currentFileName}')

                        if enableFileDeletion:
                            # delete duplicate file
                            currentFile.unlink()
                        
#
# This function calls itself, iterating thru
# all subfolders
# Place desired action in the "else:" statement
#
def file_iterator(inputPath):
    for file in inputPath.iterdir(): # loop thru files in directory
        if file.is_dir():            # do not act on folders
            file_iterator(file)      # recusive call for folders
        else:
                
            #################################################
            ### # update song year based on google search ###
            ### google_update_year(file)                  ###
            #################################################

            # delete duplicates
            check_for_duplicates(file, inputPath)
                  
#
#
#
#
#songPath = WindowsPath('E:/Music/Jaimito_Library/2000s/2000s_Slow/2000s_Slow_DONE')
songPath = Path('D:\Git\SongYearScraper\songs')

file_iterator(songPath)
