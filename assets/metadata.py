
from mutagen.easyid3 import EasyID3
import assets.search as mySearch

# list of ID3 tags of interest
listID3Tags = ['title',
               'artist',
               'albumartist',
               'genre'
               'bpm',
               'date']

#
# This function prints all ID3 tags of interest
#
# Input arg 'file' must be a .mp3 file
#
def get_song_info(file):
    print() # print empty line
    if file.name.endswith('.mp3'): 
        song  = EasyID3(file)
        print(f"           File Name: {file.name}")
        print(f"               Title: {song.get('title')}")
        print(f"Contributing Artists: {song.get('artist')}")
        print(f"        Album Artist: {song.get('albumartist')}")
        print(f"               Genre: {song.get('genre')}")
        print(f"       Beats per min: {song.get('bpm')}")
        print(f"                Year: {song.get('date')}")

#
# This function attempts to change ID3 data
#
# Input arg 'file' must be a .mp3 file
# Input arg 'tag' must be on listID3Tags
# Input arg 'value' must be a string
#
def set_ID3_data(file, tag, value):

    # file must be an .mp3
    if file.name.endswith('.mp3'):

        print()                    # print empty line

        if tag not in listID3Tags: # ensure tag is on list
            print(f"The string '{tag}' is not a valid input.")
            return                 # leave function if invlaid tag

        if not isinstance(value, str): # encsure value is a string
            print(f"The value '{str(value)}' is not a string.")
            return
        
        song  = EasyID3(file)
        print(file.name)
        print(f"Old {tag}: {song.get(tag)}")
        song[tag] = value
        song.save()
        print(f"New {tag}: {song.get(tag)}")

    else:
        print(f'File "{file.name}" is not an .mp3 file.')    

#
# This funciton googles the file name and sets the
# release year result to the Year ID3 for the .mp3 file
#
# Input arg 'file' must be a pathlib Path
#
def google_update_year(file):

    # file must be an .mp3
    if file.name.endswith('.mp3'):

        # get filename without extension
        strQuery = file.stem
        # get date of song
        result = mySearch.google('date', strQuery)
        # write date to metadata
        if result != "None": set_ID3_data(file, 'date', result)

    else:
        print(f'File "{file.name}" is not an .mp3 file.')